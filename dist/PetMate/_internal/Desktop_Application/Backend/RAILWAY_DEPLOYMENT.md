# 🚂 Railway Deployment Guide for Your Django Backend

## Prerequisites
✅ Git installed on your computer
✅ GitHub account
✅ Railway account (sign up at https://railway.app with GitHub)

---

## 📦 Step 1: Prepare Your Backend Code

Your backend is now ready! I've already:
- ✅ Created Procfile in the correct location
- ✅ Created railway.json configuration
- ✅ Updated settings.py for production
- ✅ Created .env.example as a template

---

## 🔐 Step 2: Create Your .env File (DO NOT COMMIT THIS!)

1. Navigate to `Desktop_Application/Backend/`
2. Copy `.env.example` and rename it to `.env`
3. Fill in your actual credentials:

```env
SECRET_KEY=django-insecure-your-actual-secret-key-here
DEBUG=False

# Database (Railway will provide this - leave blank for now)
DB_NAME=railway
DB_USER=root
DB_PASSWORD=
DB_HOST=
DB_PORT=3306

# Email
EMAIL_HOST_USER=your-actual-email@gmail.com
EMAIL_HOST_PASSWORD=your-actual-app-password

# SMS
PHILSMS_API_KEY=your-actual-philsms-api-key
PHILSMS_SENDER_ID=PhilSms
```

---

## 📁 Step 3: Create .gitignore (Important!)

Create a `.gitignore` file in `Desktop_Application/Backend/`:

```gitignore
# Environment variables
.env
.env.local

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
env/
ENV/

# Django
*.log
db.sqlite3
db.sqlite3-journal
/staticfiles/
/media/

# IDE
.vscode/
.idea/
*.swp
*.swo
```

---

## 🌐 Step 4: Initialize Git Repository

Open terminal in `Desktop_Application/Backend/` and run:

```powershell
cd D:\Documents\AASCHOOL\CAPSTONE\test\pythonProject\Desktop_Application\Backend

# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Django backend for Railway deployment"
```

---

## 📤 Step 5: Push to GitHub

1. Go to https://github.com and create a new repository (e.g., `pet-clinic-backend`)
2. **DO NOT** initialize with README, .gitignore, or license
3. Copy the repository URL
4. In your terminal:

```powershell
# Add GitHub remote (replace with your actual repo URL)
git remote add origin https://github.com/YOUR_USERNAME/pet-clinic-backend.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## 🚂 Step 6: Deploy to Railway

### A. Create New Project

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub
5. Select your `pet-clinic-backend` repository
6. Railway will auto-detect it's a Django project!

### B. Add MySQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"MySQL"**
3. Wait for it to provision (takes ~30 seconds)

### C. Link Database to Django App

1. Click on your Django service
2. Go to **"Variables"** tab
3. Click **"+ New Variable"** and add:

```
SECRET_KEY = your-django-secret-key-here
DEBUG = False
DB_NAME = ${{MySQL.MYSQLDB_DATABASE}}
DB_USER = ${{MySQL.MYSQLDB_USER}}
DB_PASSWORD = ${{MySQL.MYSQLDB_PASSWORD}}
DB_HOST = ${{MySQL.MYSQLDB_HOST}}
DB_PORT = ${{MySQL.MYSQLDB_PORT}}
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password
PHILSMS_API_KEY = your-philsms-key
PHILSMS_SENDER_ID = PhilSms
```

**Note:** The `${{MySQL.XXX}}` syntax automatically references your MySQL database credentials!

### D. Deploy

1. Click **"Deploy"**
2. Wait for deployment (check logs for any errors)
3. Once deployed, go to **"Settings"** → **"Domains"**
4. Click **"Generate Domain"**
5. Copy your Railway URL (e.g., `pet-clinic-backend.up.railway.app`)

---

## ✅ Step 7: Verify Deployment

Test your backend:

```powershell
# Test API endpoint (replace with your Railway URL)
curl https://your-app.up.railway.app/api/
```

Or visit in browser:
- Admin panel: `https://your-app.up.railway.app/admin/`
- API: `https://your-app.up.railway.app/api/`

---

## 🖥️ Step 8: Update Desktop Application

Update your Desktop app's API client to use Railway URL:

In `Desktop_Application/Frontend/config.json` or API client:

```json
{
  "api_url": "https://your-app.up.railway.app"
}
```

---

## 🌐 Step 9: Update Web Application

In `Web-Applications/src/`:

Create or update API configuration:

```javascript
// src/config.js or wherever you define API URL
export const API_BASE_URL = 'https://your-app.up.railway.app';
```

Don't forget to add your web app's deployed URL to Railway environment variables:

```
FRONTEND_URL = https://your-web-app.vercel.app
```

---

## 🔧 Troubleshooting

### Problem: Build fails with "mysqlclient" error
**Solution:** Railway uses Nixpacks which handles this automatically. If issues persist, check the build logs.

### Problem: Static files not loading
**Solution:** Railway automatically runs `collectstatic`. Check `STATIC_ROOT` in settings.py.

### Problem: 500 Error
**Solution:** 
1. Check Railway logs: Click your service → "Logs"
2. Ensure all environment variables are set correctly
3. Check database connection

### Problem: CORS errors from frontend
**Solution:** Add your frontend domain to `CSRF_TRUSTED_ORIGINS` in Railway variables:
```
FRONTEND_URL = https://your-frontend-domain.com
```

---

## 📝 Important Notes

1. **Never commit `.env` file** - it contains secrets!
2. **Railway free tier** gives you 500 hours/month (enough for testing)
3. **Database backups** - Railway Pro includes automated backups
4. **Custom domain** - Can add in Railway settings (requires Pro plan)
5. **Logs** - Always check Railway logs for deployment issues

---

## 🎉 Success Checklist

- [ ] Backend deployed to Railway
- [ ] MySQL database connected
- [ ] Environment variables configured
- [ ] Admin panel accessible
- [ ] API endpoints working
- [ ] Desktop app connected to Railway backend
- [ ] Web app connected to Railway backend
- [ ] CORS configured for both apps

---

## 📞 Need Help?

If you encounter issues:
1. Check Railway logs (click your service → Logs)
2. Verify all environment variables are set
3. Test database connection
4. Check ALLOWED_HOSTS and CORS settings

Your backend is now centralized and both your desktop and web apps can connect to it! 🚀
