# Insurance Fraud & Priority API

A two-stage ML system that validates claim authenticity using **XGBoost** and **Isolation Forest**, then calculates a priority score.

## 🛠 Tech Stack
- **Data:** BigQuery, SQL (CTEs), Pandas
- **Models:** XGBoost (Supervised), Isolation Forest (Unsupervised)
- **API:** FastAPI, Uvicorn, Pydantic
- **Tracking:** Weights & Biases (W&B)

---

## 🚀 Training Procedure
1. **Cloud Setup:** Place your Google Cloud `credentials.json` in the root folder.
2. **Data Prep:** Ensure your claims data is in BigQuery. Update the table ID in `src/train.py`.
3. **Execution:** Run the training script:
   ```bash
   python src/train.py
   ```
   *This will fetch data from BigQuery, engineer features, train both models, log metrics to W&B, and save models to `/models`.*

---

## 🧪 Testing Procedure

### 1. Start the API
Launch the local server:
```bash
uvicorn api.main:app --reload
```

### 2. Run a Test Script
Create a `test_api.py` file to simulate a user request:
```python
import requests

url = "http://127.0.0"
sample_claim = {
    "amount": 45000.0,
    "tenure": 5,
    "description": "Urgent emergency engine fire, need immediate cash settlement."
}

response = requests.post(url, json=sample_claim)
print(response.json())
```

### 3. Manual Testing
Navigate to `http://127.0.0` in your browser to use the built-in **Swagger UI** to test different scenarios (e.g., test a low-amount, high-tenure claim to see if it's marked as authentic).
