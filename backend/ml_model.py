import os
import joblib
import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler

MODEL_PATH = "carbon_model.pkl"
SCALER_PATH = "carbon_scaler.pkl"

class CarbonMLModel:
    def __init__(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
            self.is_trained = True
        else:
            self.model = SGDRegressor(max_iter=1000, tol=1e-3, learning_rate='invscaling')
            self.scaler = StandardScaler()
            self.is_trained = False

    def _prepare_features(self, farm_size, tree_count):
        # Features: [farm_size, tree_count, farm_size*tree_count]
        return np.array([[farm_size, tree_count, farm_size * tree_count]])

    def predict(self, farm_size, tree_count):
        if not self.is_trained:
            # Fallback simple logic if no data has been provided
            return tree_count * 0.5 + farm_size * 0.1
        X = self._prepare_features(farm_size, tree_count)
        X_scaled = self.scaler.transform(X)
        return float(self.model.predict(X_scaled)[0])

    def partial_fit(self, farm_size, tree_count, actual_carbon_savings):
        X = self._prepare_features(farm_size, tree_count)
        y = np.array([actual_carbon_savings])

        if not self.is_trained:
            # StandardScaler needs at least 2 samples to compute variance.
            # We pad it with a dummy record close to the first one.
            X_init = np.vstack([X, X * 1.01])
            y_init = np.array([actual_carbon_savings, actual_carbon_savings * 1.01])
            self.scaler.partial_fit(X_init)
            X_scaled = self.scaler.transform(X_init)
            self.model.partial_fit(X_scaled, y_init)
            self.is_trained = True
        else:
            self.scaler.partial_fit(X)
            X_scaled = self.scaler.transform(X)
            self.model.partial_fit(X_scaled, y)

        # Save updated model
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)

# Global instance
ml_model = CarbonMLModel()
