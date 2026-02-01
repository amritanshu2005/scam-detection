# 🚀 Vercel Deployment Guide

## Fixed Deployment Issues

### Changes Made:
1. ✅ Created `vercel.json` configuration
2. ✅ Created `api/index.py` serverless function handler
3. ✅ Added Mangum adapter for FastAPI compatibility
4. ✅ Fixed static file serving for Vercel
5. ✅ Added error handling for serverless environment

## Deployment Steps

### 1. Install Vercel CLI (Optional)
```bash
npm i -g vercel
```

### 2. Deploy via Vercel Dashboard

1. **Go to:** https://vercel.com
2. **Import Project** from GitHub
3. **Select:** `amritanshu2005/scam-detection`
4. **Framework Preset:** Other
5. **Root Directory:** `./` (leave as is)
6. **Build Command:** Leave empty (Vercel auto-detects)
7. **Output Directory:** Leave empty
8. **Install Command:** `pip install -r requirements.txt`

### 3. Environment Variables

Add these in Vercel dashboard:
- `API_KEY`: Your secret API key
- `OPENAI_API_KEY`: (Optional) For enhanced AI

### 4. Deploy!

Click **Deploy** and wait for build to complete.

## File Structure for Vercel

```
honey-trap/
├── api/
│   └── index.py          # Vercel serverless function
├── static/              # Static files
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── main.py             # FastAPI app
├── vercel.json         # Vercel configuration
└── requirements.txt    # Dependencies
```

## How It Works

1. **Vercel** routes requests to `api/index.py`
2. **Mangum** adapts FastAPI for serverless
3. **FastAPI** handles all API routes
4. **Static files** served from `/static/` directory

## Testing After Deployment

### 1. Health Check
```
https://your-app.vercel.app/api/health
```

### 2. Test API
```bash
curl -X POST https://your-app.vercel.app/api/v1/message \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message"}'
```

### 3. Dashboard
```
https://your-app.vercel.app/
```

## Troubleshooting

### Error: Function Invocation Failed
- Check Vercel logs in dashboard
- Verify environment variables are set
- Check `requirements.txt` is correct

### Static Files Not Loading
- Verify `static/` directory exists
- Check file paths in HTML
- Ensure `vercel.json` routes are correct

### Import Errors
- Check all dependencies in `requirements.txt`
- Verify Python version (3.11)
- Check Vercel build logs

## Alternative: Deploy to Railway/Render

If Vercel continues to have issues, use:

**Railway (Recommended):**
- Better for Python/FastAPI
- No serverless limitations
- Easier configuration

**Render:**
- Similar to Railway
- Good Python support
- Free tier available

See `GITHUB_DEPLOYMENT.md` for Railway/Render instructions.

---

**Your code is now Vercel-ready!** 🎉

