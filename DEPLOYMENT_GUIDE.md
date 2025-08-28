# Django Travel Booking App - PythonAnywhere Deployment Guide

This guide will help you deploy your Django travel booking application to PythonAnywhere.

## Prerequisites

- PythonAnywhere account (free or paid)
- Basic knowledge of command line operations

## Step 1: Upload Your Code

### Option A: Using Git (Recommended)
1. Push your code to GitHub, GitLab, or Bitbucket
2. In PythonAnywhere console, clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

### Option B: Upload Files
1. Use PythonAnywhere's file manager to upload your project files
2. Extract them to your home directory: `/home/yourusername/`

## Step 2: Create Virtual Environment

In PythonAnywhere console:
```bash
cd /home/yourusername/your-project-name
python3.10 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Go to PythonAnywhere Dashboard
2. Click "Tasks" → "Environment variables"
3. Add these variables:

| Variable | Value | Description |
|----------|-------|-------------|
| `SECRET_KEY` | Generate using `python generate_secret_key.py` | Django secret key |
| `DEBUG` | `false` | Production mode |
| `ALLOWED_HOST` | `yourusername.pythonanywhere.com` | Your domain |
| `USE_MYSQL` | `true` | Use MySQL database |
| `DB_NAME` | `yourusername$travel_booking` | Database name |
| `DB_USER` | `yourusername` | Database user |
| `DB_PASSWORD` | `your_db_password` | Database password |
| `DB_HOST` | `yourusername.mysql.pythonanywhere-services.com` | Database host |

## Step 5: Database Setup

### Create MySQL Database
1. Go to "Databases" tab in PythonAnywhere dashboard
2. Create a new database: `yourusername$travel_booking`
3. Note the password for environment variables

### Run Migrations
In PythonAnywhere console:
```bash
cd /home/yourusername/your-project-name
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser  # Create admin user
python manage.py collectstatic --noinput
```

### Load Sample Data (Optional)
```bash
python manage.py loaddata booking/fixtures/sample_data.json
# Or run the management command:
python manage.py create_sample_data
```

## Step 6: Configure Web App

1. Go to "Web" tab in PythonAnywhere dashboard
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Configure the following:

### Source Code
- Source code: `/home/yourusername/your-project-name`

### Virtual Environment
- Virtualenv: `/home/yourusername/your-project-name/venv`

### WSGI Configuration File
Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/your-project-name'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Static Files
Set up static file mappings:
- URL: `/static/`
- Directory: `/home/yourusername/your-project-name/staticfiles/`

## Step 7: Test Your Deployment

1. Click "Reload" on your web app
2. Visit `https://yourusername.pythonanywhere.com`
3. Test key functionality:
   - User registration/login
   - Travel booking features
   - Admin panel: `https://yourusername.pythonanywhere.com/admin/`

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `python manage.py collectstatic --noinput`
   - Check static files mapping in web app configuration

2. **Database connection errors**
   - Verify environment variables are set correctly
   - Check database credentials and host

3. **Import errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

4. **CSRF errors**
   - Add your domain to `CSRF_TRUSTED_ORIGINS` in settings.py

### Error Logs
- Check error logs in PythonAnywhere dashboard under "Web" → "Log files"
- Server log: `/var/log/yourusername.pythonanywhere.com.server.log`
- Error log: `/var/log/yourusername.pythonanywhere.com.error.log`

## Production Best Practices

1. **Security**
   - Keep `DEBUG = False` in production
   - Use strong database passwords
   - Regularly update dependencies

2. **Performance**
   - Use MySQL database for better performance
   - Enable compression for static files
   - Monitor application performance

3. **Backups**
   - Regular database backups
   - Keep code in version control
   - Document configuration changes

## Updating Your Application

1. Pull latest changes (if using Git):
   ```bash
   cd /home/yourusername/your-project-name
   git pull origin main
   ```

2. Update dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. Reload web app in PythonAnywhere dashboard

## Support

- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Django Documentation**: https://docs.djangoproject.com/
- **Project Issues**: Check your repository's issue tracker

---

Your Django Travel Booking App should now be live at `https://yourusername.pythonanywhere.com`!
