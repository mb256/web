# Deployment Guide: Local Development → GitHub → PythonAnywhere

This guide explains how to develop locally using Poetry, push changes to GitHub, and deploy to PythonAnywhere.

## Prerequisites

- GitHub account
- PythonAnywhere account
- Git installed locally
- Poetry installed locally

## Initial Setup

### 1. Local Development Setup (Already Complete ✓)

Your project uses Poetry for dependency management:
- `pyproject.toml` - Poetry configuration
- `requirements.txt` - Generated for PythonAnywhere compatibility

### 2. GitHub Setup

If you haven't already pushed to GitHub:

```bash
# Add your GitHub repository as remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/your-repo.git

# Push your code
git add .
git commit -m "Initial commit"
git push -u origin main
```

### 3. PythonAnywhere Initial Setup

#### 3.1. Clone Repository on PythonAnywhere

1. Log into PythonAnywhere
2. Open a Bash console
3. Clone your repository:

```bash
cd ~
git clone https://github.com/yourusername/your-repo.git web
cd web
```

#### 3.2. Install Dependencies

```bash
pip3.10 install --user -r requirements.txt
```

#### 3.3. Configure Django Settings for Production

Create a production settings file or environment variables on PythonAnywhere.

**Important settings to update on PythonAnywhere:**

1. Set `DEBUG = False` in production
2. Add your PythonAnywhere domain to `ALLOWED_HOSTS`:
   ```python
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
   ```
3. Configure `STATIC_ROOT` and `STATIC_URL`:
   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = '/home/yourusername/web/web/staticfiles'
   ```

You can create a separate `settings_production.py` or use environment variables.

#### 3.4. Run Initial Migrations and Collect Static

```bash
cd ~/web/web
python manage.py migrate
python manage.py collectstatic
```

#### 3.5. Configure Web App on PythonAnywhere

1. Go to Web tab on PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Django wizard)
4. Select Python version (3.10 or later)
5. Configure WSGI file:

Click on WSGI configuration file link and replace contents with:

```python
import os
import sys

# Add your project directory to the sys.path
project_home = '/home/yourusername/web/web'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variable for Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

6. Configure static files:
   - URL: `/static/`
   - Directory: `/home/yourusername/web/web/staticfiles`

7. Click "Reload" button

## Daily Development Workflow

### Step 1: Develop Locally

```bash
# Make your changes
# Test locally with Poetry environment
cd /home/brouk/workspace/web/web
poetry run python manage.py runserver
```

### Step 2: Update Dependencies (if needed)

```bash
# If you add new packages with Poetry
poetry add package-name

# Update requirements.txt for PythonAnywhere
# (Since poetry export isn't available, manually update requirements.txt)
# Or use: poetry show --no-dev --tree
```

### Step 3: Commit and Push to GitHub

```bash
cd /home/brouk/workspace/web
git add .
git commit -m "Description of your changes"
git push origin main
```

### Step 4: Deploy to PythonAnywhere

Option A: **Using the deployment script (Recommended)**

```bash
# On PythonAnywhere Bash console
cd ~/web
chmod +x deploy_pythonanywhere.sh
./deploy_pythonanywhere.sh
```

Then go to Web tab and click **Reload** button.

Option B: **Manual deployment**

```bash
# On PythonAnywhere Bash console
cd ~/web
git pull origin main
pip3.10 install --user -r requirements.txt
cd web
python manage.py migrate
python manage.py collectstatic --noinput
```

Then go to Web tab and click **Reload** button.

## Managing Dependencies

### Adding a New Package Locally

```bash
poetry add package-name
# Manually add to requirements.txt for PythonAnywhere
echo "package-name>=version" >> requirements.txt
```

### Updating All Packages

```bash
poetry update
# Update requirements.txt accordingly
```

## Troubleshooting

### Issue: Module not found on PythonAnywhere
- Ensure package is in `requirements.txt`
- Run `pip3.10 install --user -r requirements.txt` on PythonAnywhere
- Check pip list: `pip3.10 list --user`

### Issue: Static files not loading
- Verify `STATIC_ROOT` in settings
- Run `python manage.py collectstatic`
- Check static files mapping in Web tab

### Issue: Database changes not reflected
- Run migrations: `python manage.py migrate`
- Check migrations exist: `python manage.py showmigrations`

### Issue: Changes not visible after deployment
- Ensure you clicked "Reload" in Web tab
- Check error logs in PythonAnywhere (Web tab → Log files)

## Security Checklist for Production

- [ ] Set `DEBUG = False` on PythonAnywhere
- [ ] Use environment variables for `SECRET_KEY`
- [ ] Add only your domain to `ALLOWED_HOSTS`
- [ ] Never commit `.env` files or sensitive credentials
- [ ] Use HTTPS (automatic on PythonAnywhere)
- [ ] Regularly update dependencies for security patches

## Quick Reference Commands

**Local (with Poetry):**
```bash
poetry install          # Install dependencies
poetry add <package>    # Add package
poetry run python ...   # Run Python with Poetry environment
git push origin main    # Push to GitHub
```

**PythonAnywhere:**
```bash
git pull origin main                      # Pull latest changes
pip3.10 install --user -r requirements.txt  # Install dependencies
python manage.py migrate                   # Run migrations
python manage.py collectstatic --noinput   # Collect static files
# Then: Reload web app from dashboard
```
