# OpenSky Network DLT Pipeline

This project ingest flight data from the OpenSky Network API using `dlthub`.

## Setup

1.  Add your OpenSky Network credentials to the `.env` file in the root directory:
    ```
    OPENSKY_CLIENT_ID=your_id
    OPENSKY_CLIENT_SECRET=your_secret
    ```
2.  Install dependencies:
    ```bash
    uv sync
    ```

## Running the Pipeline

You can run the pipeline locally:
```bash
uv run python opensky_pipeline.py
```

To run it in continuous mode:
```bash
CONTINUOUS=true INTERVAL_SECONDS=60 uv run python opensky_pipeline.py
```

## Docker

Build the image:
```bash
make dlthub-build
```

Run the container:
```bash
make dlthub-run
```
