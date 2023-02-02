from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
from time import sleep

input_topic_name = "ip_address_by_country"
output_topic_name = "ip_address_by_location"
localhost_bootstrap_server = "localhost:9092"
producer = KafkaProducer(bootstrap_servers=[localhost_bootstrap_server])
admin = KafkaAdminClient(bootstrap_servers=[localhost_bootstrap_server])

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
    for line in open("ip_address_with_country.txt"):
        ip_address, country_raw = line.split(",")
        country = country_raw[:-1]
        producer.send(
            input_topic_name,
            key=f"{country}".encode("ascii"),
            value=f"{ip_address}".encode("ascii"),
        )
        sleep(0.1)
    print(f"input topic {output_topic_name} populated successfully")
except KafkaError:
    print("A kafka error occurred")
