from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic

def create_topic(admin_client, topic_name, partitions):
    topic = NewTopic(topic_name, num_partitions=partitions, replication_factor=1)
    print("Creating topic", topic_name, "with", partitions, "partitions")
    admin_client.create_topics([topic])
    print("Topic", topic_name, "created")

def check_producer_connection(bootstrap_servers):
    print("aaaaaaaaaaa")
    try:
        conf = {'bootstrap.servers': bootstrap_servers}
        producer = Producer(conf)
        producer.list_topics(timeout=5)
        producer.flush()
        print(f"Producer connection to {bootstrap_servers} successful")
        return True
    except Exception as e:
        print(f"Producer connection failed: {e}")
        return False
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}')

# Configure the Kafka producer

cluster_ip = "127.0.0.1"
brokers_list = [
    # f"{cluster_ip}:9093",
    f"{cluster_ip}:8098",
]
print(brokers_list)
bootstrap_servers = ','.join(brokers_list)
# check_producer_connection(bootstrap_servers)

conf = {
    'bootstrap.servers': f'{bootstrap_servers}',
}
producer = Producer(conf)
# Produce a message to the 'test' topic
topic = 'testing'
key = 'key'
value = 'Hello, Kafka!'

producer.produce(topic, key=key, value=value, callback=delivery_report)
producer.flush()

admin = AdminClient({'bootstrap.servers': bootstrap_servers})
create_topic(admin, "USEEEEEEEEER", 3)


# # Wait for any outstanding messages to be delivered and delivery reports to be received
exit()
