from confluent_kafka.admin import AdminClient, NewTopic


def create_topic(broker_list, topic_name, num_partitions, replication_factor):
    # Set up the AdminClient with the broker list
    admin_client = AdminClient({'bootstrap.servers': broker_list})

    # Check if the topic already exists
    existing_topics = admin_client.list_topics().topics
    if topic_name in existing_topics:
        print(f"Topic '{topic_name}' already exists.")
        return

    # Create a NewTopic object with the desired configuration
    new_topic = NewTopic(
        topic=topic_name,
        num_partitions=num_partitions,
        replication_factor=replication_factor
    )

    # Create the topic using the AdminClient
    admin_client.create_topics([new_topic])

    # Wait for the topic creation to complete (optional)
    admin_client.poll(timeout=5)

    print(
        f"Topic '{topic_name}' created successfully with {num_partitions} partitions and replication factor {replication_factor}.")


# Example usage
broker_list = '127.0.0.1:8098'
topic_name = 'your_topic'
num_partitions = 5  # Adjust as needed
replication_factor = 2  # Adjust as needed

create_topic(broker_list, topic_name, num_partitions, replication_factor)
