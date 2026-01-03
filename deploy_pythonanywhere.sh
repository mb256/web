#!/bin/bash
# Deployment script for PythonAnywhere
# Run this script on PythonAnywhere after pulling from GitHub

set -e  # Exit on error

echo "========================================="
echo "PythonAnywhere Deployment Script"
echo "========================================="

# Navigate to project directory
cd ~/web

# Pull latest changes from GitHub
echo "Pulling latest changes from GitHub..."
git pull origin main

# Install/Update dependencies
echo "Installing dependencies..."
pip install --user -r requirements.txt

# Navigate to Django project
cd web

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "Running database migrations..."
python manage.py migrate

echo "========================================="
echo "Deployment completed successfully!"
echo "Don't forget to reload your web app from PythonAnywhere dashboard"
echo "========================================="
