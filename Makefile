IMAGE_NAME=opensky-dlthub
CONTAINER_NAME=opensky-streaming
# Absolute path to the data directory for volume mounting
DATA_DIR=$(shell pwd)/data/opensky_data
DOTENV_PATH=$(shell pwd)/.env

.PHONY: dlthub-build dlthub-run dlthub-stop dlthub-logs dlthub-clean help

dlthub-build:
	docker build -t $(IMAGE_NAME) dlthub

dlthub-run:
	# Running in continuous mode by default
	# Using --env-file to pass keys from the root .env
	docker run -d \
		--name $(CONTAINER_NAME) \
		--env-file $(DOTENV_PATH) \
		-e CONTINUOUS=true \
		-e INTERVAL_SECONDS=30 \
		-e DESTINATION__FILESYSTEM__BUCKET_URL=file:///app/data/opensky_data \
		-v $(DATA_DIR):/app/data/opensky_data \
		$(IMAGE_NAME)

dlthub-stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

dlthub-logs:
	docker logs -f $(CONTAINER_NAME)

dlthub-clean:
	docker rmi $(IMAGE_NAME) || true

dlthub-help:
	@echo "Available commands:"
	@echo "  dlthub-build  - Build the docker image"
	@echo "  dlthub-run    - Run the container in continuous mode"
	@echo "  dlthub-stop   - Stop and remove the container"
	@echo "  dlthub-logs   - View container logs"
	@echo "  dlthub-clean  - Clean up the docker image"
