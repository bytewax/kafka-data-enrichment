import json
import requests
import os
import logging

from bytewax.dataflow import Dataflow
from bytewax import operators as op
from bytewax.connectors.kafka import KafkaSourceMessage, KafkaSinkMessage
from bytewax.connectors.kafka import operators as kop

logger = logging.getLogger(__name__)
logging.basicConfig(format=logging.BASIC_FORMAT, level=logging.WARNING)

flow = Dataflow("redpanda-enrichment")

REDPANDA_BROKER = os.getenv("REDPANDA_BROKER", "localhost:9092").split(";")
IN_TOPICS=["ip_address_by_country"]
OUT_TOPIC="ip_address_by_location"

kinp = kop.input("redpanda-in", flow, brokers=REDPANDA_BROKER, topics=IN_TOPICS)
# Inspect errors and crash
op.inspect("inspect-redpanda-errors", kinp.errs).then(op.raises, "redpanda-error")
op.inspect("inspect-redpanda-oks", kinp.oks)

def get_location(msg: KafkaSourceMessage) -> str:
    # decode our data in the same way we encoded in the utils.py script
    ip_address = msg.value.decode("ascii")
    response = requests.get(f"https://ipapi.co/{ip_address}/json/")
    response_json = response.json()
    location_data = {
        "ip": ip_address,
        "city": response_json.get("city"),
        "region": response_json.get("region"),
        "country_name": response_json.get("country_name"),
    }
    return KafkaSinkMessage(
                    key=msg.key, 
                    value=json.dumps(location_data).encode()
                    )


enriched_stream = op.map("enrich", kinp.oks, get_location)
op.inspect("inspect-enriched", enriched_stream)
kop.output("kafka-out", enriched_stream, brokers=REDPANDA_BROKER, topic=OUT_TOPIC)
