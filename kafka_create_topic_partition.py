from confluent_kafka.admin import AdminClient, NewTopic


def create_kafka_topic(bootstrap_servers, topic_name, partitions, replication_factor):
    admin_config = {'bootstrap.servers': bootstrap_servers}
    admin_client = AdminClient(admin_config)

    # Define the topic configuration
    topic_config = {
        'cleanup.policy': 'compact',
        'compression.type': 'lz4',
        'delete.retention.ms': '100',
        'file.delete.delay.ms': '100',
    }

    # Create a NewTopic instance
    new_topic = NewTopic(topic_name, num_partitions=partitions, replication_factor=replication_factor,
                         config=topic_config)

    # Create the topic
    admin_client.create_topics([new_topic])

    # There is no close method for AdminClient


def list_kafka_topics(bootstrap_servers):
    admin_config = {'bootstrap.servers': bootstrap_servers}
    admin_client = AdminClient(admin_config)

    # Fetch the list of topics
    topics_metadata = admin_client.list_topics().topics

    # Extract topic names
    topic_names = [topic for topic in topics_metadata]

    # Print the list of topics
    print("List of Kafka topics:")
    for topic_name in topic_names:
        print(topic_name)


if __name__ == '__main__':
    # Kafka bootstrap servers
    # Update with your actual Kafka broker address
    bootstrap_servers = 'localhost:9092'

    # Topic details
    topic_name = 'test'
    partitions = 3
    replication_factor = 1

    # Create the Kafka topic
    # create_kafka_topic(bootstrap_servers, topic_name,
    #                    partitions, replication_factor)

    # print(
    #     f"Kafka topic '{topic_name}' created with {partitions} partitions and replication factor {replication_factor}.")

    list_kafka_topics(bootstrap_servers)
