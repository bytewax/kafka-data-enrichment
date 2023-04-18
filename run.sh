# Start Redpanda
docker compose up -d

# Load Redpanda with data
python ./utils/utils.py

# Run the Dataflow
python -m bytewax.run dataflow:flow
