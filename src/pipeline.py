import os
import joblib
from xgboost import XGBClassifier
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV

class InsuranceModelPipeline:
    def __init__(self):
        self.xgb_pipeline = None
        self.iso_forest = None

    def build_supervised_pipeline(self):
        # dataset contains 753 authentic and 253 fraud, means 3 times less fraud
        # so, add weighting for fraud class with pipeline for XGBoost with Scaling
        self.xgb_pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('xgb', XGBClassifier(
                n_estimators=100,
                eval_metric='logloss',
                scale_pos_weight=3, # consider fraud 3X important
                random_state=42
            ))
        ])

    def train_fraud_model(self, X, y):
        # train XGBoost using cross-validation/tuning logic
        # simple tuning example using GridSearchCV
        param_grid = {
            'xgb__max_depth': [3, 5],
            'xgb__learning_rate': [0.01, 0.1]
        }
        
        grid_search = GridSearchCV(self.xgb_pipeline, param_grid, cv=3, scoring='f1')
        grid_search.fit(X, y)
        self.xgb_pipeline = grid_search.best_estimator_
        print(f"XGBoost Best Score: {grid_search.best_score_}")

        return self.xgb_pipeline

    def train_anomaly_model(self, X):
        # train isolation forest for outlier detection
        # isolation forest doesn't use labels (Unsupervised)
        self.iso_forest = IsolationForest(contamination=0.05, random_state=42)
        self.iso_forest.fit(X)

        return self.iso_forest

    def save_models(self, path_prefix="models/"):
        
        if not os.path.exists(path_prefix):
            os.makedirs(path_prefix)
            

        joblib.dump(self.xgb_pipeline, f"{path_prefix}fraud_xgb.pkl")
        joblib.dump(self.iso_forest, f"{path_prefix}anomaly_iso.pkl")
        print("Models exported to /models folder.")

# integration Note: 
# input X here will be from engineering.py 
# containing [amount, tenure, desc_length, claim_density, contains_red_flags]
