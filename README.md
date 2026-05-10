# Insurance Claims Fraud Detection API

A production-ready ML API for detecting insurance claim fraud, authenticity, and priority assessment using machine learning models.

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the server:**
```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

3. **Access the API:**
- API Documentation: http://localhost:8000/docs
- Health Check: http://localhost:8000/api/health
- Model Info: http://localhost:8000/api/model-info

## 📡 API Endpoints

### 1. Predict Claim (Fraud Detection)
**POST** `/api/predict`

Analyzes an insurance claim and returns fraud detection, authenticity score, and priority assessment.

**Request Body:**
```json
{
  "customer_id": "CUST123",
  "amount": 5000.50,
  "tenure": 3,
  "description": "Car accident on highway. Vehicle damage, medical emergency.",
  "date_of_incident": "2024-05-10"
}
```

**Response:**
```json
{
  "category": "Accident",
  "urgency": "High",
  "fraud_risk": "Low",
  "anomaly_score": -0.45,
  "authenticity_score": 8,
  "priority_score": 7,
  "rank_score": 56.0
}
```

**Response Fields:**
- **category**: Detected claim category (e.g., Health, Accident, Theft)
- **urgency**: Urgency level - "High", "Medium", or "Low"
- **fraud_risk**: "High" or "Low" - indicates likelihood of fraud
- **anomaly_score**: Raw anomaly detection score from the ML model
- **authenticity_score**: 1-9 scale (1=fraudulent, 9=authentic)
- **priority_score**: 1-9 scale for handling priority based on claim characteristics
- **rank_score**: Combined score (authenticity × priority) for prioritization

### 2. Health Check
**GET** `/api/health`

Checks if the service and model are loaded correctly.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 3. Model Information
**GET** `/api/model-info`

Returns metadata about the loaded ML model.

**Response:**
```json
{
  "loaded": true,
  "meta": {
    "timestamp": "2024-05-10 14:30:00",
    "training_count": 1000,
    "amount_map": { ... },
    "fraud_features": [ ... ]
  },
  "training_count": 1000
}
```

## 🔧 Deployment to Render

### Using render.yaml (Recommended)

1. **Push your code to GitHub:**
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

2. **Deploy on Render:**
   - Go to [render.com](https://render.com)
   - Create new service → "Build and deploy from Git"
   - Connect your GitHub repository
   - Select `render.yaml` as the configuration file
   - Deploy!

### Using Procfile

If using Procfile instead of render.yaml:
1. In Render dashboard, select "New Web Service"
2. Connect your GitHub repo
3. Set runtime to "Python 3.11"
4. Deploy - Render will automatically use the Procfile

### Environment Variables

Configure these on Render:
```
ENV=production
PORT=8000
CORS_ORIGINS=*,https://your-app.com
MODEL_PATH=models/churn_model.pkl
```

## 📦 Project Structure

```
InsuranceClaim-AI/
├── api/
│   ├── __init__.py
│   ├── main.py                  # FastAPI application entry point
│   └── router.py                # API endpoint definitions
├── src/
│   ├── __init__.py
│   ├── config.py                # Configuration management
│   ├── schemas.py               # Pydantic data models
│   ├── utils.py                 # Utility functions
│   └── ml_service.py            # ML model loading and prediction
├── models/
│   └── churn_model.pkl          # ⭐ Pre-trained ML model
├── data/
│   └── insurance_claims.csv     # Sample data
├── notebooks/                   # Jupyter notebooks (optional)
├── render.yaml                  # Render deployment config
├── Procfile                     # Procfile for deployment
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
└── README.md                    # This file
```

## 🤖 ML Model Details

The model uses an ensemble approach:

1. **NLP Classification:** Random Forest classifier on vectorized claim descriptions to categorize claims
2. **Anomaly Detection:** Isolation Forest to detect statistical anomalies based on:
   - Claim amount
   - Customer tenure
   - Amount ratio to policy type average
   - Tenure-based risk scoring

3. **Scoring System:**
   - **Authenticity**: Derived from anomaly detection (1-9 scale)
   - **Priority**: Based on urgency, amount, and tenure (1-9 scale)
   - **Rank Score**: Combined metric for intelligent triage

## 🔐 CORS Configuration

By default, the API accepts requests from any origin (`*`). For production, restrict CORS origins:

```python
# In main.py, modify CORS_ORIGINS environment variable
CORS_ORIGINS=your-app.com,other-app.com
```

## 📊 Example Usage from Another Application

```python
import requests

# Predict claim
response = requests.post(
    "https://your-api.render.com/api/predict",
    json={
        "customer_id": "CUST456",
        "amount": 3500.00,
        "tenure": 5,
        "description": "Medical emergency, hospitalization required",
        "date_of_incident": "2024-05-10"
    }
)

result = response.json()
print(f"Fraud Risk: {result['fraud_risk']}")
print(f"Authenticity Score: {result['authenticity_score']}")
print(f"Priority: {result['priority_score']}")
```

## 🧪 Testing

Test the deployed API:

```bash
curl -X POST "https://your-api.render.com/api/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "TEST001",
    "amount": 2500,
    "tenure": 2,
    "description": "Emergency room visit",
    "date_of_incident": "2024-05-10"
  }'
```

## 📝 Notes

- The pre-trained model (`trained_brain.pkl`) is already included in the repository
- The API expects the model file to exist at `models/trained_brain.pkl`
- For production, ensure the model file is properly versioned and backed up
- The API logs requests and predictions for monitoring
- Health check endpoint should be used for load balancer configuration

## 🛠️ Troubleshooting

**Model not loading:**
- Ensure `models/trained_brain.pkl` exists
- Check file permissions and path configuration

**CORS errors:**
- Update `CORS_ORIGINS` environment variable
- By default it's set to `*` (all origins)

**Port conflicts:**
- Ensure the PORT environment variable is properly set
- Default port is 8000

## 📄 License

This project is provided as-is for insurance claim processing tasks.

---

**Ready to deploy?** Push to GitHub and connect to Render for automatic deployments!