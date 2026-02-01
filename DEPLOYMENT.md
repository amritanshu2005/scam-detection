# 🚀 Deployment Guide

Complete guide for deploying your Agentic Honey-Pot system to production.

## Prerequisites

- Python 3.11+
- API key for authentication
- (Optional) OpenAI API key for enhanced AI responses

## Quick Deploy Options

### 1. Railway (Recommended)

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   railway login
   ```

2. **Deploy:**
   ```bash
   railway init
   railway up
   ```

3. **Set Environment Variables:**
   - `API_KEY`: Your secret API key
   - `OPENAI_API_KEY`: (Optional) OpenAI API key

### 2. Render

1. **Connect GitHub Repository**
2. **Create New Web Service**
3. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment Variables:
     - `API_KEY`: Your secret API key
     - `OPENAI_API_KEY`: (Optional)

### 3. Heroku

1. **Install Heroku CLI:**
   ```bash
   heroku login
   ```

2. **Create App:**
   ```bash
   heroku create your-app-name
   ```

3. **Set Environment Variables:**
   ```bash
   heroku config:set API_KEY=your-secret-key
   heroku config:set OPENAI_API_KEY=your-openai-key
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

### 4. Docker Deployment

1. **Build Image:**
   ```bash
   docker build -t honey-trap .
   ```

2. **Run Container:**
   ```bash
   docker run -d -p 8000:8000 \
     -e API_KEY=your-secret-key \
     -e OPENAI_API_KEY=your-openai-key \
     --name honey-trap \
     honey-trap
   ```

### 5. AWS/GCP/Azure

#### AWS (Elastic Beanstalk)

1. **Install EB CLI:**
   ```bash
   pip install awsebcli
   ```

2. **Initialize:**
   ```bash
   eb init
   eb create
   ```

3. **Set Environment Variables:**
   ```bash
   eb setenv API_KEY=your-key OPENAI_API_KEY=your-key
   ```

#### Google Cloud Run

1. **Build and Push:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/honey-trap
   ```

2. **Deploy:**
   ```bash
   gcloud run deploy honey-trap \
     --image gcr.io/PROJECT_ID/honey-trap \
     --platform managed \
     --set-env-vars API_KEY=your-key
   ```

#### Azure App Service

1. **Install Azure CLI:**
   ```bash
   az login
   ```

2. **Create App:**
   ```bash
   az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name honey-trap --runtime "PYTHON:3.11"
   ```

3. **Set Environment Variables:**
   ```bash
   az webapp config appsettings set --resource-group myResourceGroup --name honey-trap --settings API_KEY=your-key
   ```

## Environment Variables

Required:
- `API_KEY`: Secret API key for authentication

Optional:
- `OPENAI_API_KEY`: OpenAI API key for enhanced AI responses
- `PORT`: Server port (default: 8000)
- `HOST`: Server host (default: 0.0.0.0)

## Production Checklist

- [ ] Set strong `API_KEY` in environment
- [ ] Enable HTTPS/SSL
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Set up database for conversation storage (optional)
- [ ] Configure CORS for your domain
- [ ] Set up backup and recovery
- [ ] Monitor performance metrics

## Monitoring

Access performance metrics:
```bash
curl -H "X-API-Key: your-key" https://your-domain.com/api/v1/metrics
```

## Scaling

For high traffic:
- Use Redis for conversation storage
- Deploy multiple instances behind load balancer
- Use database instead of in-memory storage
- Enable caching for static responses

## Security

1. **API Key Security:**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly

2. **HTTPS:**
   - Always use HTTPS in production
   - Configure SSL certificates

3. **Rate Limiting:**
   - Implement rate limiting middleware
   - Prevent abuse and DDoS

4. **Input Validation:**
   - All inputs are validated by Pydantic
   - Sanitize user inputs

## Troubleshooting

### Server Not Starting
- Check Python version (3.11+)
- Verify all dependencies installed
- Check port availability

### API Key Issues
- Verify environment variable is set
- Check API key matches in requests

### Performance Issues
- Check server resources
- Review logs for errors
- Monitor response times

## Support

For issues or questions:
- Check logs in `logs/` directory
- Review API documentation at `/docs`
- Check performance metrics at `/api/v1/metrics`

