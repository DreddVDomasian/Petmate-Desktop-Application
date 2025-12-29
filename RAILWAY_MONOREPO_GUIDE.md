# 🚂 Railway Deployment for Monorepo (Updated)

## Your Project Structure

Since your **entire project root** is one repository containing:
- `Desktop_Application/Backend/` (Django backend)
- `Desktop_Application/Frontend/` (PyQt desktop app)
- `Web-Applications/` (React web app)

Railway needs to know to build from the `Desktop_Application/Backend/` subdirectory.

---

## ✅ What I've Set Up for You

### 1. **railway.toml** (Root Directory)
Created at project root to tell Railway:
- Build from `Desktop_Application/Backend/`
- Use Python 3.11
- Run migrations and start gunicorn

### 2. **Fixed settings.py**
Fixed the syntax error where code got jumbled.

---

## 🚀 Deployment Steps for Monorepo

### Step 1: Make Sure You Have .env File

In `Desktop_Application/Backend/`, copy `.env.example` to `.env` and fill it:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=False
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
PHILSMS_API_KEY=your-philsms-key
PHILSMS_SENDER_ID=PhilSms
```

### Step 2: Commit Everything

From your project root:

```powershell
cd D:\Documents\AASCHOOL\CAPSTONE\test\pythonProject

# Check git status
git status

# Add all files (except .env which is in .gitignore)
git add .

# Commit
git commit -m "Prepare backend for Railway deployment"

# Push to your repository
git push origin main
```

### Step 3: Deploy to Railway

#### Option A: Deploy from GitHub

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Select your repository (the root one containing everything)
5. Railway will detect the `railway.toml` file and use it!

#### Option B: Deploy with Railway CLI (Alternative)

```powershell
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
cd D:\Documents\AASCHOOL\CAPSTONE\test\pythonProject
railway init

# Deploy
railway up
```

### Step 4: Add MySQL Database

1. In Railway dashboard, click **"+ New"**
2. Select **"Database"** → **"MySQL"**
3. Wait for provisioning

### Step 5: Configure Environment Variables

Click on your Django service → **Variables** tab:

```
SECRET_KEY = your-django-secret-key-here
DEBUG = False

# Database - Railway provides these automatically
DB_NAME = ${{MySQL.MYSQLDB_DATABASE}}
DB_USER = ${{MySQL.MYSQLDB_USER}}
DB_PASSWORD = ${{MySQL.MYSQLDB_PASSWORD}}
DB_HOST = ${{MySQL.MYSQLDB_HOST}}
DB_PORT = ${{MySQL.MYSQLDB_PORT}}

# Email
EMAIL_HOST_USER = your-email@gmail.com
EMAIL_HOST_PASSWORD = your-app-password

# SMS
PHILSMS_API_KEY = your-philsms-key
PHILSMS_SENDER_ID = PhilSms
```

### Step 6: Get Your Railway URL

1. Go to **Settings** → **Domains**
2. Click **"Generate Domain"**
3. Copy your URL (e.g., `your-app.up.railway.app`)

---

## 🔧 Important: Update Your Apps

### Desktop Application

Update `Desktop_Application/Frontend/Config/config.json` or wherever your API URL is:

```json
{
  "api_url": "https://your-app.up.railway.app"
}
```

### Web Application

Update `Web-Applications/src/` API configuration to point to Railway.

Then add your web app's deployed URL to Railway variables:

```
FRONTEND_URL = https://your-web-app.vercel.app
```

---

## 📝 Key Differences from Separate Repo

### ✅ Advantages of Monorepo:
- Single repository for all code
- Easier to manage versions
- One commit updates everything

### ⚠️ Things to Note:
- Railway builds from the root but uses `railway.toml` to know where your backend is
- Make sure `.gitignore` is in the Backend folder to protect `.env`
- The `railway.toml` file handles the subdirectory navigation

---

## 🧪 Test Your Deployment

```powershell
# Test API
curl https://your-app.up.railway.app/api/

# Or visit in browser
https://your-app.up.railway.app/admin/
```

---

## ❓ Troubleshooting

### Build fails?
Check Railway logs - click your service → "Logs" tab

### Can't find manage.py?
The `railway.toml` file should handle this with the `cd` command

### Database connection error?
Verify all DB environment variables are set correctly in Railway

### CORS errors?
Add your frontend domain to `FRONTEND_URL` variable in Railway

---

Your setup is ready! Just push to GitHub and deploy! 🚀
