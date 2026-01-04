import dlt
import os
import time
from dotenv import load_dotenv
from opensky import opensky

# Load environment variables from the .env file in the parent directory
load_dotenv("../.env")

def run_pipeline(continuous: bool = False, interval_seconds: int = 600):
    # Use credentials from environment variables
    client_id = os.getenv("OPENSKY_CLIENT_ID")
    client_secret = os.getenv("OPENSKY_CLIENT_SECRET")
    
    if not client_id or not client_secret:
        raise ValueError("OPENSKY_CLIENT_ID or OPENSKY_CLIENT_SECRET not found in environment variables")

    # Define the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="opensky_streaming",
        destination="filesystem",
        dataset_name="opensky_data",
    )

    while True:
        print(f"Starting pipeline run at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            load_info = pipeline.run(opensky(client_id=client_id, client_secret=client_secret))
            print(load_info)
        except Exception as e:
            print(f"Error during pipeline run: {e}")
            if not continuous:
                raise
        
        if not continuous:
            break
            
        print(f"Waiting for {interval_seconds} seconds before next run...")
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # Check for CONTINUOUS environment variable
    is_continuous = os.getenv("CONTINUOUS", "false").lower() == "true"
    interval = int(os.getenv("INTERVAL_SECONDS", "30")) # Reduced default for testing
    run_pipeline(continuous=is_continuous, interval_seconds=interval)
