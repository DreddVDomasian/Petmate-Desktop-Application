# Railway Volume Setup for Image Storage

This guide shows how to set up persistent image storage on Railway using Volumes (no external services needed).

## What Railway Volumes Do

- **Persistent storage** that survives deployments and restarts
- Files stored in a Volume stay even when you redeploy or rebuild your container
- Perfect for user-uploaded images like the About section photo

## Setup Steps

### 1. Create a Volume in Railway

1. Go to your Railway project dashboard
2. Click on your backend service
3. Go to the **"Data"** or **"Variables"** tab and look for **"Volumes"**
4. Click **"New Volume"**
5. Configure:
   - **Mount Path**: `/data` (this is where Railway will attach the storage)
   - **Size**: Start with 1GB (you can increase later)
6. Click **"Add Volume"**

### 2. Add Environment Variable

In your Railway backend service, add this environment variable:

```
MEDIA_ROOT_PATH=/data/media
```

This tells Django to store uploaded files in the Volume instead of the container's ephemeral filesystem.

### 3. Deploy

Railway will automatically restart your service with the Volume attached. The backend will now:
- Store uploaded images in `/data/media/about/`
- Serve them via `/media/about/<filename>`
- Images persist across all deployments

## How It Works

1. **Desktop app** uploads image via POST to `/api/about/` with `image` file
2. **Backend** saves to `MEDIA_ROOT` (which is now `/data/media` on Railway)
3. **Database** stores the full URL: `https://your-backend.railway.app/media/about/image.jpg`
4. **Website** fetches `/api/about/` and displays the image from that URL

## Testing Locally

Run locally without volumes (uses `Desktop_Application/Backend/media/` folder):

```bash
cd Desktop_Application/Backend
python manage.py runserver
```

Upload a test image:

```bash
curl -X POST http://localhost:8000/api/about/ \
  -F "title=At PetMate Animal Clinic, we care for your pets" \
  -F "body=Full description here..." \
  -F "image=@/path/to/your/image.jpg"
```

Verify it saved:
```bash
curl http://localhost:8000/api/about/
```

## Image Quality

- Images are stored **as-is** (original quality)
- No compression or resizing happens on upload
- Browsers display the full-resolution image (you can control display size with CSS)

## Cost

Railway Volumes pricing:
- First 1GB: typically included in plan or ~$0.25/month
- Additional storage: ~$0.25/GB/month
- Much cheaper than external image CDN services for small projects

## Serving Images in Production

Django will serve media files automatically in development. For production on Railway, we're using Django to serve them (via the URL pattern in `myproject/urls.py`). For high-traffic sites, you'd typically use:
- Railway's CDN (if available)
- Or add Cloudflare in front of your Railway domain

## Troubleshooting

**Images disappear after deployment**
- Make sure the Volume is attached and `MEDIA_ROOT_PATH=/data/media` is set

**Can't access images**
- Check that `Desktop_Application/Backend/myproject/urls.py` includes the media URL pattern (already configured)
- Verify the image URL in the database matches the served path

**Volume full**
- Increase Volume size in Railway dashboard
- Clean up old images if needed

## Next Steps

Once this is working, you can add the desktop UI to let staff update the About section with a simple form (text fields + image picker).
