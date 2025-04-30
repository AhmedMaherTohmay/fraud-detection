import mlflow
import numpy as np
from src.config import MODEL_NAME

class FraudPredictor:
    """Wrapper for fraud detection model with score transformation."""
    
    def __init__(self, model_name=MODEL_NAME, stage="Production"):
        """Initialize predictor with MLflow model.
        
        Args:
            model_name: Name of registered MLflow model
            stage: Model stage (Production/Staging/None)
        """
        mlflow.set_tracking_uri("file:./mlruns")
        self.model = mlflow.sklearn.load_model(
            f"models:/{model_name}/{stage}"
        )

    def transform_scores(self, scores):
        """Transform anomaly scores to 0-100 probability-like scale.
        
        Args:
            scores: Raw anomaly scores from model
            
        Returns:
            Scores scaled to 0-100 range
        """
        shifted = -scores  # Convert to positive where higher = more anomalous
        min_score = np.min(shifted)
        max_score = np.max(shifted)
        return 100 * (shifted - min_score) / (max_score - min_score + 1e-10)

    def predict(self, features):
        """Predict fraud probability for given features.
        
        Args:
            features: DataFrame with transaction features
            
        Returns:
            Array of fraud probabilities (0-100)
        """
        scores = self.model.decision_function(features)
        return self.transform_scores(scores)

# Example usage
if __name__ == "__main__":
    print("Testing FraudPredictor...")
    predictor = FraudPredictor()
    
    # Mock data - in practice you'd use real features
    mock_features = np.random.rand(1, 10)  
    print(f"Sample prediction: {predictor.predict(mock_features)}")