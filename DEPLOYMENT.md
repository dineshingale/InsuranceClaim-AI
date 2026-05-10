# Deployment Guide for Render.com

## Prerequisites
- GitHub account
- Render account (free tier available at render.com)
- Your code pushed to GitHub

## Step 1: Prepare Your Repository

The project is now ready for deployment. Ensure your code is pushed to GitHub:

```bash
git add .
git commit -m "Prepare fraud detection API for Render deployment"
git push origin main
```

## Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. Go to [render.com](https://render.com)
2. Sign in with your GitHub account
3. Click "New +" → "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect and use `render.yaml`
6. Click "Deploy"

### Option B: Using Procfile

1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Choose Python 3.11 as runtime
5. Set build command: `pip install -r requirements.txt`
6. Set start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables (optional):
   - `ENV`: `production`
   - `CORS_ORIGINS`: `*` (or restrict to your app domains)
8. Click "Deploy"

## Step 3: Configure Environment Variables

In Render Dashboard → Your Service → Environment:

```
ENV=production
CORS_ORIGINS=*
```

Optional:
```
MODEL_PATH=models/trained_brain.pkl
```

## Step 4: Test Your Deployment

Once deployed, Render will give you a URL (e.g., `https://insurance-fraud-detector.onrender.com`)

### Test with curl:
```bash
curl -X POST "https://insurance-fraud-detector.onrender.com/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "amount": 2500,
    "tenure": 2,
    "description": "Emergency room visit",
    "date_of_incident": "2024-05-10"
  }'
```

### Test Health Endpoint:
```bash
curl https://insurance-fraud-detector.onrender.com/api/health
```

### View API Documentation:
```
https://insurance-fraud-detector.onrender.com/docs
```

## Step 5: Integration with Other Apps

Other applications can now call your API:

```python
import requests

API_URL = "https://your-service.onrender.com"

def check_fraud(customer_id, amount, tenure, description):
    response = requests.post(
        f"{API_URL}/api/predict",
        json={
            "customer_id": customer_id,
            "amount": amount,
            "tenure": tenure,
            "description": description,
            "date_of_incident": "2024-05-10"
        }
    )
    return response.json()

# Usage
result = check_fraud("CUST123", 5000, 3, "Car accident claim")
print(f"Fraud Risk: {result['fraud_risk']}")
print(f"Authenticity: {result['authenticity_score']}/9")
```

## Monitoring

- **Logs**: View in Render Dashboard → Service → Logs
- **Health Check**: `/api/health` endpoint monitors service status
- **Metrics**: Free tier includes basic metrics in Render Dashboard

## Troubleshooting

### Service won't start
- Check logs in Render Dashboard
- Ensure `models/trained_brain.pkl` exists
- Verify Python version is 3.11+

### Model not loading
- Confirm file path is correct: `models/trained_brain.pkl`
- Check file permissions

### CORS errors
- Update `CORS_ORIGINS` environment variable
- By default it's `*` (allow all)

### Port issues
- Port is automatically assigned by Render
- Don't specify port in Procfile/render.yaml (use `$PORT` variable)

## Costs

- **Free Tier**: Includes 750 hours/month (approximately 31 days)
- **Paid Tier**: Pay-as-you-go starting at $7/month
- See [render.com pricing](https://render.com/pricing) for details

## Continuous Deployment

After initial deployment:
1. Any push to GitHub's `main` branch will automatically redeploy
2. View deployment history in Render Dashboard
3. Rollback to previous versions if needed

---

**Your API is now live and ready to serve fraud detection predictions!** 🚀
