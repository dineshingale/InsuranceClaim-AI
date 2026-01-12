# Intelligent Insurance Claim Processing & Fraud Guard

This application constitutes the **Smart Claims Processor**, a multi-modal AI system designed to streamline insurance claim processing. It combines **NLP (Natural Language Processing)** for text analysis with **Anomaly Detection** for numerical fraud detection.

## 🚀 Features

*   **Multi-Modal Analysis**: Fuses text (claim description) and structured data (amount, tenure).
*   **Stream A (NLP)**: Classifies claims into categories (Medical, Accident, Theft, etc.) and detects urgency.
*   **Stream B (Fraud Guard)**: Uses Isolation Forest to detect statistical anomalies in claim amounts relative to customer history.
*   **Fusion Layer**: Intelligent logic to make a final recommendation: Auto-Approve, Manual Review, or Investigation.
*   **Synthetic Data Generation**: Self-contained module to generate realistic dummy data for testing.

## 🛠️ Tech Stack

*   **Python 3.9+**
*   **Streamlit**: Interactive Dashboard.
*   **Scikit-Learn**: Machine Learning models (RandomForest, IsolationForest).
*   **Pandas & NumPy**: Data manipulation.
*   **Faker**: Synthetic data generation.

## 💻 Contribution Guide

Follow these steps to set up the project locally for development.

### 1. Prerequisites

Ensure you have the following installed:
*   [Python](https://www.python.org/downloads/) (Version 3.8 or higher)
*   [Git](https://git-scm.com/)

### 2. Clone the Repository

(If you haven't already because this is part of a monorepo)

```bash
git clone https://github.com/YOUR_USERNAME/my-app-monorepo.git
cd my-app-monorepo
```

### 3. Navigate to the App Directory

```bash
cd apps/smart-claims-processor/backend
```

### 4. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

**Windows:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

**Mac/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

Start the Streamlit dashboard:

```bash
streamlit run app.py
```

*   The app will automatically generate `insurance_claims.csv` (synthetic training data) on the first run.
*   The dashboard will open in your default browser at `http://localhost:8501`.

## 🧪 Testing

To test the data generation logic independently:

```bash
python src/data_generator.py
```

## 📂 Project Structure

```
smart-claims-processor/
├── src/
│   ├── data_generator.py    # Generates synthetic insurance data
├── app.py                   # Main Streamlit application & ML Logic
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
```
