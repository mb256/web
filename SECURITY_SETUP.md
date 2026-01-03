# Setting Up Django: Local Development vs Production (PythonAnywhere)

## Overview of Django Security Settings

### SECRET_KEY
- **Purpose**: Cryptographic key for signing cookies, CSRF tokens, password reset links
- **Security Impact**: If leaked, attackers can forge sessions and bypass security
- **Rule**: NEVER commit production SECRET_KEY to Git

### DEBUG
- **Purpose**: Shows detailed error pages with stack traces
- **Local**: `True` - helpful for debugging
- **Production**: `False` - prevents exposing sensitive information to users

### ALLOWED_HOSTS
- **Purpose**: Prevents HTTP Host header attacks
- **Local**: `localhost`, `127.0.0.1`
- **Production**: Your actual domain(s)

## Local Development Setup

### 1. Project Structure
```
/home/brouk/workspace/web/
├── .env                    # Local environment variables (NOT in Git)
├── .env.example            # Template for .env (IS in Git)
├── .gitignore              # Ensures .env is not committed
├── pyproject.toml          # Poetry dependencies
├── requirements.txt        # For PythonAnywhere
└── web/
    └── mysite/
        └── settings.py     # Reads from environment variables
```

### 2. .env File (Local Development)
**File: `.env`** (This is NOT committed to Git)
```bash
DJANGO_SECRET_KEY=django-insecure-development-key
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=mbrouk.pythonanywhere.com,localhost,127.0.0.1
```

**How it works:**
- When you run locally, Django reads these values from `.env`
- `DEBUG=1` enables debug mode for development
- You can test with both localhost AND your production domain

### 3. settings.py - Universal Configuration
Your `settings.py` now automatically:
1. Loads `.env` if it exists (local development)
2. Falls back to environment variables (production)
3. Has safe defaults

```python
# Loads .env file in local development
env_file = BASE_DIR.parent / '.env'
if env_file.exists():
    # Read and load variables

# Read from environment (works in both local and production)
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-key')
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'
ALLOWED_HOSTS = [host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost').split(',')]
```

### 4. Running Locally
```bash
cd /home/brouk/workspace/web/web
poetry run python manage.py runserver

# The .env file is automatically loaded
# You'll see DEBUG mode enabled
# Server runs on localhost:8000
```

## Production Setup (PythonAnywhere)

### 1. Generate Production SECRET_KEY

**On PythonAnywhere Bash console:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy this key - you'll need it in the next step.

### 2. Set Environment Variables

You have two options:

#### Option A: In WSGI Configuration File (Recommended)
**File: `/var/www/mbrouk_pythonanywhere_com_wsgi.py`**

```python
import os
import sys

# Set environment variables BEFORE importing Django
os.environ['DJANGO_SECRET_KEY'] = 'your-generated-production-secret-key-here'
os.environ['DJANGO_DEBUG'] = '0'  # ALWAYS 0 in production
os.environ['DJANGO_ALLOWED_HOSTS'] = 'mbrouk.pythonanywhere.com'

# Add your project directory to sys.path
project_home = '/home/mbrouk/web/web'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# Import and run Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

#### Option B: Using .env File on PythonAnywhere
**Create `/home/mbrouk/web/.env` on PythonAnywhere:**
```bash
# SSH into PythonAnywhere
cd ~/web
nano .env
```

**Add (with your generated key):**
```bash
DJANGO_SECRET_KEY=your-generated-production-secret-key-here
DJANGO_DEBUG=0
DJANGO_ALLOWED_HOSTS=mbrouk.pythonanywhere.com
```

### 3. Static Files Configuration
Your `settings.py` already has:
```python
STATIC_ROOT = BASE_DIR.parent / 'staticfiles'
```

**On PythonAnywhere:**
```bash
cd ~/web/web
python manage.py collectstatic --noinput
```

**In PythonAnywhere Web tab:**
- URL: `/static/`
- Directory: `/home/mbrouk/web/staticfiles`

## Security Checklist Comparison

### Local Development ✓
- ✓ `.env` file with development settings
- ✓ `DEBUG=1` for detailed errors
- ✓ Development SECRET_KEY (OK for local)
- ✓ `.env` in `.gitignore`
- ✓ Works with localhost

### Production (PythonAnywhere) ✓
- ✓ Strong, unique SECRET_KEY
- ✓ `DEBUG=0` - no error details exposed
- ✓ ALLOWED_HOSTS = only your domain
- ✓ Environment variables NOT in Git
- ✓ HTTPS enabled (automatic on PythonAnywhere)

## Common Workflows

### Making Changes Locally
```bash
cd /home/brouk/workspace/web

# Edit code
# Test with: poetry run python web/manage.py runserver

# Commit and push
git add .
git commit -m "Your changes"
git push origin main
```

### Deploying to PythonAnywhere
```bash
# On PythonAnywhere
cd ~/web
./deploy_pythonanywhere.sh
# Then reload web app from dashboard
```

## Troubleshooting

### "SECRET_KEY not set"
**Local:** Ensure `.env` exists with `DJANGO_SECRET_KEY=...`
**Production:** Check WSGI file has `os.environ['DJANGO_SECRET_KEY'] = ...`

### "DEBUG should be False in production"
**Check WSGI file or .env:** `DJANGO_DEBUG=0` (zero, not letter O)

### "DisallowedHost error"
**Check:** `DJANGO_ALLOWED_HOSTS` includes your domain
**Local:** Can include multiple: `localhost,127.0.0.1,mbrouk.pythonanywhere.com`

### Changes not reflected
- Ensure you pushed to GitHub
- Ran `git pull` on PythonAnywhere
- Clicked "Reload" button in Web tab

## Key Differences Summary

| Setting | Local Development | Production (PythonAnywhere) |
|---------|------------------|----------------------------|
| **SECRET_KEY** | Development key in `.env` | Strong random key in WSGI or server `.env` |
| **DEBUG** | `1` (True) | `0` (False) |
| **ALLOWED_HOSTS** | `localhost,127.0.0.1` | `mbrouk.pythonanywhere.com` |
| **Config Location** | `.env` file (not in Git) | WSGI file or server `.env` (not in Git) |
| **Database** | SQLite local file | SQLite or PostgreSQL on server |
| **Static Files** | Served by runserver | Collected to STATIC_ROOT |

## Why This Approach?

1. **Single settings.py**: No need for separate files
2. **Environment-specific config**: Through environment variables
3. **Git-safe**: No secrets in version control
4. **Easy testing**: Can test production settings locally
5. **Standard practice**: Follows 12-factor app methodology
