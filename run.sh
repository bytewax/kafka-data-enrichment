# run redpanda
rpk container start

# build docker image
docker build . -t bytewax-dataflow

# run dataflow
docker run bytewax-dataflow