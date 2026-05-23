# Insurance Fraud & Priority API

A two-stage ML system that validates claim authenticity, then calculates a priority score.

## 🛠 Tech Stack
- **Data:** BigQuery, SQL (CTEs), Pandas
- **Models:** XGBoost (Supervised)
- **API:** FastAPI, Uvicorn, Pydantic
- **Tracking:** Weights & Biases (W&B)


### 1. Start the API
Launch the local server:
```bash
uvicorn api.main:app --reload
```

### 3. Manual Testing
Navigate to `http://127.0.0` in your browser to use the built-in **Swagger UI** to test different scenarios (e.g., test a low-amount, high-tenure claim to see if it's marked as authentic).
