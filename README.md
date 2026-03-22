# web
Web Portal for personal info pages and other activity   

## Setup

Django based application managed by Poetry.

### Activate the virtual environment

```bash
eval $(poetry env activate)
```

> **Note:** If the virtualenv doesn't exist yet, Poetry will create it automatically on first activation.

### Install dependencies

```bash
poetry install
```

## Running locally

### Environment variables

| Variable | Description | Default |
|---|---|---|
| `DJANGO_DEBUG` | Enable Django debug mode | `0` (off) |

To enable debug mode locally:

```bash
export DJANGO_DEBUG=1
```

### Start the development server

Make sure the virtual environment is activated, then start the Django development server:

```bash
cd web
python manage.py runserver
```

The app will be available at **http://127.0.0.1:8000/**

> **Tip:** To bind to a different port, e.g. 8080: `python manage.py runserver 8080`
