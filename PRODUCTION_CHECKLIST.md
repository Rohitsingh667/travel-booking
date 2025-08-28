# Production Deployment Checklist

Use this checklist to ensure your Django Travel Booking app is properly configured for PythonAnywhere deployment.

## ✅ Pre-Deployment Checklist

### Code Preparation
- [ ] All code committed to version control (Git)
- [ ] No sensitive data in code (passwords, keys, etc.)
- [ ] Requirements.txt includes all dependencies
- [ ] Database migrations are up to date

### Security Configuration
- [ ] DEBUG = False in production
- [ ] Secure SECRET_KEY generated and set in environment variables
- [ ] ALLOWED_HOSTS configured for PythonAnywhere domain
- [ ] CSRF_TRUSTED_ORIGINS includes your domain
- [ ] Security middleware enabled (WhiteNoise, HTTPS, etc.)

### Database Setup
- [ ] MySQL database created on PythonAnywhere
- [ ] Database credentials set in environment variables
- [ ] Migrations run successfully
- [ ] Sample data loaded (optional)
- [ ] Admin superuser created

### Static Files
- [ ] WhiteNoise middleware added
- [ ] STATIC_ROOT configured
- [ ] collectstatic command run successfully
- [ ] Static files mapping set in PythonAnywhere web app

### Environment Variables
- [ ] SECRET_KEY set
- [ ] DEBUG set to 'false'
- [ ] ALLOWED_HOST set to your domain
- [ ] Database credentials configured
- [ ] All environment variables tested

## 🚀 Deployment Steps

1. **Upload Code**
   - [ ] Code uploaded via Git or file manager
   - [ ] Project in correct directory structure

2. **Virtual Environment**
   - [ ] Virtual environment created
   - [ ] Dependencies installed from requirements.txt

3. **Web App Configuration**
   - [ ] WSGI file configured correctly
   - [ ] Source code path set
   - [ ] Virtual environment path set
   - [ ] Static files mapping configured

4. **Database Operations**
   - [ ] Migrations applied
   - [ ] Static files collected
   - [ ] Superuser created
   - [ ] Sample data loaded

5. **Testing**
   - [ ] Home page loads without errors
   - [ ] User registration works
   - [ ] Login/logout functionality
   - [ ] Travel booking features
   - [ ] Admin panel accessible
   - [ ] Static files (CSS/JS) loading

## 🔍 Post-Deployment Verification

### Functionality Tests
- [ ] User can register new account
- [ ] User can login/logout
- [ ] Travel options display correctly
- [ ] Booking process works end-to-end
- [ ] User profile management
- [ ] Admin panel functions properly

### Performance Checks
- [ ] Page load times acceptable
- [ ] No console errors in browser
- [ ] Database queries optimized
- [ ] Static files compressed and cached

### Security Verification
- [ ] HTTPS working (if SSL enabled)
- [ ] No debug information exposed
- [ ] Admin panel secured
- [ ] User data protected

## 🐛 Troubleshooting Common Issues

### Application Won't Start
- Check WSGI configuration
- Verify virtual environment path
- Review error logs
- Ensure all dependencies installed

### Static Files Not Loading
- Run collectstatic command
- Check static files mapping
- Verify STATIC_ROOT path
- Test WhiteNoise middleware

### Database Errors
- Verify environment variables
- Check database credentials
- Ensure migrations are applied
- Test database connection

### 403/404 Errors
- Check ALLOWED_HOSTS setting
- Verify URL configuration
- Review CSRF settings
- Check file permissions

## 📋 Maintenance Tasks

### Regular Updates
- [ ] Update Django and dependencies
- [ ] Apply security patches
- [ ] Monitor error logs
- [ ] Backup database regularly

### Performance Monitoring
- [ ] Monitor resource usage
- [ ] Check database performance
- [ ] Review user activity logs
- [ ] Optimize slow queries

---

**✅ All checks completed? Your app is ready for production!**

Visit your deployed app at: `https://yourusername.pythonanywhere.com`
