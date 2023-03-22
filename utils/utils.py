from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
from time import sleep
import os

REDPANDA_BROKER = os.getenv("REDPANDA_BROKER", "localhost:9092")

input_topic_name = "ip_address_by_country"
output_topic_name = "ip_address_by_location"
localhost_bootstrap_server = REDPANDA_BROKER
producer = None
while not producer:
    try:
        producer = Producer({"bootstrap.servers": localhost_bootstrap_server})
    except Exception as e:
        print(f"brokers not ready - {e}")
        sleep(0.1)
admin = AdminClient({"bootstrap.servers": localhost_bootstrap_server})

# Create input topic
try:
    input_topic = NewTopic(input_topic_name, num_partitions=20, replication_factor=1)
    admin.create_topics([input_topic])
    print(f"input topic {input_topic_name} created successfully")
except:
    print(f"Topic {input_topic_name} already exists")

# Create output topic
try:
    output_topic = NewTopic(output_topic_name, num_partitions=20, replication_factor=1)
    admin.create_topics([output_topic])
    print(f"output topic {output_topic_name} created successfully")
except:
    print(f"Topic {output_topic_name} already exists")

# Add data to input topic
try:
    for line in open("data/dataset.txt"):
        ip_address, country_raw = line.split(",")
        country = country_raw[:-1]
        producer.produce(
            input_topic_name,
            key=f"{country}".encode("ascii"),
            value=f"{ip_address}".encode("ascii"),
        )
        sleep(0.1)
    print(f"input topic {output_topic_name} populated successfully")
finally:
    producer.flush()
