# Insurance Fraud & Priority API

A two-stage ML system that validates claim authenticity, then calculates a priority score.

## Tech Stack
- BigQuery, SQL (CTEs), Pandas
- XGBoost (Supervised)
- FastAPI, Uvicorn, Pydantic
- Weights & Biases (W&B)

## Business Problem Solved
Insurance fraud detection with 80%+ accuracy & claim prioritization by processing urgency (amount + customer tenure), reducing manual audit overhead and accelerating payouts for genuine claimants.

- Hybrid model approach (supervised + unsupervised fusion)
- 3:1 weighting (fraud is 25% of dataset, 753 legitimate vs 253 fraud)

## Scale
- FastAPI handling 500-1000 predictions/sec per instance
- Render/Heroku (render.yaml + Procfile) with auto-scaling
- <50ms per prediction
