import json
import requests

from bytewax.dataflow import Dataflow
from bytewax.inputs import KafkaInputConfig
from bytewax.outputs import KafkaOutputConfig
from bytewax.execution import cluster_main

def get_location(data):
    key, value = data
    # decode our data in the same way we encoded in the utils.py script
    ip_address = value.decode("ascii")
    response = requests.get(f"https://ipapi.co/{ip_address}/json/")
    response_json = response.json()
    location_data = {
        "ip": ip_address,
        "city": response_json.get("city"),
        "region": response_json.get("region"),
        "country_name": response_json.get("country_name"),
    }
    return key, json.loads(location_data)


flow = Dataflow()
flow.input(
    step_id="ip_address",
    input_config=KafkaInputConfig(
        brokers=["localhost:9092"], topic="ip_address_by_country", tail=False
    ),
)
flow.map(get_location)
flow.capture(
    KafkaOutputConfig(brokers=["localhost:9092"], topic="ip_address_by_location")
)

if __name__ == "__main__":
    addresses = ["localhost:2101"]

    cluster_main(flow, addresses=addresses, proc_id=0, worker_count_per_proc=1)