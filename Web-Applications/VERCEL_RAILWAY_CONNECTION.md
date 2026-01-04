# Connecting Vercel Frontend to Railway Backend

This guide explains how to connect your Vercel-deployed frontend to your Railway-deployed backend.

## ✅ Code Changes Completed

All necessary code changes have been made to your frontend to support environment-based API configuration:

1. **API Configuration Utility** (`src/config/api.js`)
   - Reads `VITE_API_URL` from environment variables
   - Provides `apiFetch()` wrapper that automatically handles credentials
   - Falls back to `http://localhost:8000` for local development

2. **Updated All Fetch Calls**
   - All components now use `apiFetch()` instead of raw `fetch()`
   - Credentials are automatically included in all requests

## 🚀 Deploy Steps

### Step 1: Set Environment Variable in Vercel

1. Go to your Vercel dashboard: https://vercel.com/dashboard
2. Select your project (e.g., `petmate-management`)
3. Go to **Settings** → **Environment Variables**
4. Add a new environment variable:
   - **Name:** `VITE_API_URL`
   - **Value:** `https://web-production-f564f.up.railway.app`
   - **Environment:** Select all (Production, Preview, Development)
5. Click **Save**

### Step 2: Redeploy Your Vercel Application

After adding the environment variable, you need to trigger a new deployment:

**Option A: Via Vercel Dashboard**
1. Go to **Deployments** tab
2. Click the three dots (...) on the latest deployment
3. Select **Redeploy**

**Option B: Via Git Push**
1. Make a small commit to your repository:
   ```bash
   git commit --allow-empty -m "Trigger redeployment with env vars"
   git push
   ```

### Step 3: Verify Backend CORS Settings

Your backend already has the correct CORS settings in `Desktop_Application/Backend/myproject/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    # ... other origins
    "https://web-production-f564f.up.railway.app",
    "https://petmate-management.vercel.app"  # ✅ Your Vercel domain
]

CORS_ALLOW_CREDENTIALS = True  # ✅ Required for cookies
```

If your Vercel domain is different, update this in your Railway backend and redeploy.

## 🧪 Testing the Connection

After redeployment:

1. Visit your Vercel site: `https://petmate-management.vercel.app`
2. Open browser DevTools (F12) → Console
3. Try to log in or sign up
4. Check the Network tab:
   - API requests should go to `https://web-production-f564f.up.railway.app/api/...`
   - Status codes should be 200 (success) or 400/401 (validation errors)
   - No CORS errors should appear

## 🔍 Troubleshooting

### Issue: API calls still go to localhost
- **Solution:** Clear your browser cache and hard reload (Ctrl+Shift+R)
- Verify the environment variable is set in Vercel dashboard

### Issue: CORS errors
- **Solution:** Check that your Vercel domain is in `CORS_ALLOWED_ORIGINS` in Railway backend
- Redeploy Railway backend after updating settings

### Issue: 500 errors from backend
- **Solution:** Check Railway logs in your Railway dashboard
- Verify database connection and all backend services are running

### Issue: Authentication not persisting
- **Solution:** Ensure `CORS_ALLOW_CREDENTIALS = True` in backend settings
- Check that cookies are being set (DevTools → Application → Cookies)

## 📝 Local Development

For local development:

1. Ensure `.env.local` exists with:
   ```
   VITE_API_URL=http://localhost:8000
   ```

2. Start your Django backend locally:
   ```bash
   cd Desktop_Application/Backend
   python manage.py runserver
   ```

3. Start your Vite frontend:
   ```bash
   cd Web-Applications
   npm run dev
   ```

## 🔐 Security Notes

- Never commit `.env.local` to git (already in .gitignore)
- Environment variables in Vercel are secure and encrypted
- Only `VITE_` prefixed variables are exposed to the browser

## 📚 Environment Variable Reference

| Environment | VITE_API_URL Value |
|-------------|-------------------|
| Local Dev   | `http://localhost:8000` |
| Vercel Prod | `https://web-production-f564f.up.railway.app` |

Your setup should now be complete! The frontend will automatically connect to the correct backend based on the environment.
