import mlflow
from mlflow.tracking import MlflowClient
from config.config import MODEL_NAME

def promote_to_production(version: int):
    """Promote specified model version to production.
    
    Args:
        version: Model version number to promote
    """
    client = MlflowClient("file:./mlruns")
    client.transition_model_version_stage(
        name=MODEL_NAME,
        version=version,
        stage="Production",
        archive_existing_versions=True
    )
    print(f"Version {version} promoted to Production")

def list_models():
    """List all registered models and versions."""
    client = MlflowClient("file:./mlruns")
    for model in client.search_registered_models():
        print(f"Model: {model.name}")
        for version in model.latest_versions:
            print(f"  Version {version.version} ({version.current_stage})")

if __name__ == "__main__":
    print("Current registered models:")
    list_models()
    
    # Example promotion (uncomment to use)
    # promote_to_production(1)