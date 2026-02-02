# Vercel Deployment Guide

## Environment Variables Required

Before deploying, make sure to set these environment variables in your Vercel project settings:

1. Go to your Vercel project dashboard
2. Navigate to **Settings** > **Environment Variables**
3. Add the following variables:

```
API_KEY=your-secret-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
```

## How to Get Your Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Get API Key"
4. Copy the API key and add it to Vercel

## Deployment Steps

1. Push your code to GitHub:

   ```bash
   git add .
   git commit -m "Fix Vercel deployment configuration"
   git push origin main
   ```

2. Vercel will automatically detect the changes and redeploy

3. Once deployed, test your API at:
   - Homepage: `https://your-app.vercel.app/`
   - API endpoint: `https://your-app.vercel.app/api/v1/message`

## Testing the API

Use this curl command to test (replace with your actual API key):

```bash
curl -X POST https://your-app.vercel.app/api/v1/message \
  -H "Content-Type: application/json" \
  -H "x-api-key: your-api-key" \
  -d '{
    "sessionId": "test123",
    "message": {
      "sender": "scammer",
      "text": "Your account has been blocked! Send money urgently!",
      "timestamp": "2024-01-01T10:00:00Z"
    },
    "conversationHistory": []
  }'
```

## Troubleshooting

If you see errors:

1. **Check Environment Variables**: Make sure `GEMINI_API_KEY` is set in Vercel
2. **Check Logs**: Go to your Vercel deployment > Runtime Logs
3. **Redeploy**: Try triggering a new deployment from Vercel dashboard

## Key Changes Made

- ✅ Simplified `vercel.json` to use rewrites instead of builds
- ✅ Updated `api/index.py` to work as a serverless function
- ✅ Fixed static file handling in `main.py` with proper paths
- ✅ Added `.vercelignore` to exclude unnecessary files
- ✅ Removed Mangum dependency (not needed for Vercel Python runtime)
