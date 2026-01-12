# Smart Claims Processor (Full Stack)

This project contains the full-stack implementation of the **Smart Insurance Claim Processing & Fraud Guard** system.

## 📂 Project Structure

*   **`backend/`**: Python-based AI Core & Streamlit Dashboard.
    *   Contains the Multi-Modal AI Logic (NLP + Anomaly Detection).
    *   Runs the interactive Streamlit dashboards (Admin & User).
*   **`frontend/`**: React-based Web Interface.
    *   (Under Development) A modern web portal for submitting claims.

## 🚀 Getting Started

### Backend (AI & Dashboard)

1.  Navigate to `backend`:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    streamlit run app.py
    ```

### Frontend (React App)

1.  Navigate to `frontend`:
    ```bash
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Start the dev server:
    ```bash
    npm run dev
    ```

## 🤝 Workflow

*   **Backend**: Handles Data Generation, Model Training, and Claim Analysis.
*   **Frontend**: Provides a user-facing submission form (integrated via API in future steps).
