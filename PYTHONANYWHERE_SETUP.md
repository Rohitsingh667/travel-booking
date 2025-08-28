# Step-by-Step PythonAnywhere Deployment Guide

## Prerequisites
- PythonAnywhere account (free or paid)
- Your Django project files ready

---

## STEP 1: Prepare Your Code

### 1.1 Generate Secret Key
First, generate a secure secret key for production:

```bash
python generate_secret_key.py
```

**Copy the generated key** - you'll need it for environment variables.

### 1.2 Download Project Files
Since your repo isn't connected to git, you have two options:

**Option A: Download as ZIP**
- Download your project as a ZIP file
- Extract it locally

**Option B: Set up Git (Recommended)**
```bash
git init
git add .
git commit -m "Initial commit"
# Then push to GitHub/GitLab/Bitbucket
```

---

## STEP 2: Upload Code to PythonAnywhere

### 2.1 Login to PythonAnywhere
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Login to your account

### 2.2 Upload Your Code

**Method A: If you have Git repository**
1. Open a **Bash console** from your dashboard
2. Clone your repository:
```bash
git clone https://github.com/yourusername/your-repo.git travel_booking_app
cd travel_booking_app
```

**Method B: Manual file upload**
1. Go to **Files** tab in your dashboard
2. Navigate to `/home/yourusername/`
3. Create new folder: `travel_booking_app`
4. Upload all your project files to this folder
5. Or use the built-in editor to create files one by one

---

## STEP 3: Set Up Virtual Environment

### 3.1 Open Bash Console
From your PythonAnywhere dashboard, click **"New console"** → **"Bash"**

### 3.2 Create Virtual Environment
```bash
cd /home/yourusername/travel_booking_app
python3.10 -m venv venv
source venv/bin/activate
```

### 3.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If you get MySQL errors**, install this first:
```bash
pip install mysqlclient
```

---

## STEP 4: Configure Environment Variables

### 4.1 Go to Environment Variables
1. In your PythonAnywhere dashboard
2. Click **"Tasks"** → **"Environment variables"**

### 4.2 Add Required Variables
Add these environment variables one by one:

| Variable Name | Value | Example |
|---------------|-------|---------|
| `SECRET_KEY` | Your generated secret key | `django-insecure-abcd1234...` |
| `DEBUG` | `false` | `false` |
| `ALLOWED_HOST` | Your domain | `yourusername.pythonanywhere.com` |
| `USE_MYSQL` | `true` | `true` |
| `DB_NAME` | Database name | `yourusername$travelbooking` |
| `DB_USER` | Your username | `yourusername` |
| `DB_PASSWORD` | Database password | `your_db_password` |
| `DB_HOST` | Database host | `yourusername.mysql.pythonanywhere-services.com` |

**Replace `yourusername` with your actual PythonAnywhere username!**

---

## STEP 5: Create MySQL Database

### 5.1 Go to Databases Tab
1. Click **"Databases"** in your dashboard
2. Scroll down to **"Create database"**

### 5.2 Create Database
1. Database name: `yourusername$travelbooking`
   - Example: If your username is `john123`, name it: `john123$travelbooking`
2. Click **"Create"**
3. **Note the password** - you'll need it for environment variables

### 5.3 Update Environment Variables
Go back to Environment variables and set:
- `DB_PASSWORD` = the password from step 5.2

---

## STEP 6: Run Database Setup

### 6.1 Back to Bash Console
```bash
cd /home/yourusername/travel_booking_app
source venv/bin/activate
```

### 6.2 Test Database Connection
```bash
python manage.py check
```

### 6.3 Run Migrations
```bash
python manage.py migrate
```

### 6.4 Create Superuser
```bash
python manage.py createsuperuser
```
- Enter username, email, and password for admin access

### 6.5 Load Sample Data (Optional)
```bash
python manage.py create_sample_data
```

### 6.6 Collect Static Files
```bash
python manage.py collectstatic --noinput
```

---

## STEP 7: Configure Web App

### 7.1 Create Web App
1. Go to **"Web"** tab in dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**

### 7.2 Configure Source Code
In the **"Code"** section:
- **Source code**: `/home/yourusername/travel_booking_app`

### 7.3 Configure Virtual Environment
In the **"Virtualenv"** section:
- **Virtualenv**: `/home/yourusername/travel_booking_app/venv`

### 7.4 Configure WSGI File
1. Click on the **WSGI configuration file** link
2. **Delete all existing content**
3. **Replace with this code**:

```python
import os
import sys

# Add your project directory to the sys.path
path = '/home/yourusername/travel_booking_app'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_booking.settings')

# Import Django application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Important**: Replace `yourusername` with your actual username!

### 7.5 Configure Static Files
In the **"Static files"** section, add:
- **URL**: `/static/`
- **Directory**: `/home/yourusername/travel_booking_app/staticfiles/`

---

## STEP 8: Deploy and Test

### 8.1 Reload Web App
1. Scroll to top of **"Web"** tab
2. Click the big green **"Reload yourusername.pythonanywhere.com"** button

### 8.2 Test Your Website
1. Click on your domain link: `https://yourusername.pythonanywhere.com`
2. You should see your travel booking homepage!

### 8.3 Test Key Features
- **Homepage**: Should load without errors
- **Registration**: `https://yourusername.pythonanywhere.com/accounts/signup/`
- **Login**: `https://yourusername.pythonanywhere.com/accounts/login/`
- **Admin**: `https://yourusername.pythonanywhere.com/admin/`

---

## STEP 9: Troubleshooting

### 9.1 If Site Shows "Something went wrong"
1. Go to **"Web"** tab
2. Check **"Error log"** and **"Server log"**
3. Common fixes:
   - Check WSGI file path is correct
   - Verify environment variables are set
   - Ensure virtual environment path is correct

### 9.2 If Static Files Don't Load
```bash
# In bash console:
cd /home/yourusername/travel_booking_app
source venv/bin/activate
python manage.py collectstatic --noinput
```
Then reload the web app.

### 9.3 Database Connection Errors
- Double-check database name format: `yourusername$travelbooking`
- Verify database password in environment variables
- Check database host: `yourusername.mysql.pythonanywhere-services.com`

---

## STEP 10: Final Verification

### 10.1 Complete Feature Test
- [ ] Homepage loads
- [ ] User can register new account
- [ ] User can login/logout
- [ ] Travel options display
- [ ] Booking functionality works
- [ ] Admin panel accessible
- [ ] Static files (CSS) loading properly

### 10.2 Security Check
- [ ] DEBUG is set to `false`
- [ ] Admin panel requires login
- [ ] User data is protected

---

## 🎉 Success!

Your Django Travel Booking App is now live at:
**https://yourusername.pythonanywhere.com**

### Quick Reference URLs:
- **Homepage**: `https://yourusername.pythonanywhere.com/`
- **Register**: `https://yourusername.pythonanywhere.com/accounts/signup/`
- **Login**: `https://yourusername.pythonanywhere.com/accounts/login/`
- **Admin**: `https://yourusername.pythonanywhere.com/admin/`

### For Updates:
1. Upload new files or push to git
2. Run migrations if needed: `python manage.py migrate`
3. Collect static files: `python manage.py collectstatic --noinput`
4. Reload web app

---

## Need Help?
- **PythonAnywhere Help**: https://help.pythonanywhere.com/
- **Check error logs** in the Web tab
- **Test locally first** before deploying changes

Remember to replace `yourusername` with your actual PythonAnywhere username throughout this guide!
