from confluent_kafka.admin import AdminClient, NewTopic

server = "localhost"
ports = [8097, 8098, 8099]
# ports = [30097, 30098, 30099]
# ports = [30097]
list_of_brokers = [f"{server}:{port}" for port in ports]
kafka_bootstrap_servers = ",".join(list_of_brokers)

admin_config = {"bootstrap.servers": kafka_bootstrap_servers}


# def get_cluster_info():
#     admin_client = AdminClient(admin_config)
#
#     # Fetch metadata for all topics in the cluster
#     metadata = admin_client.list_topics(timeout=5)
#
#     topics = []
#     for topic, topic_metadata in metadata.topics.items():
#         print(f"Topic: {topic}")
#         print(f" Partitions: {list(topic_metadata.partitions.keys())} , len: {len(topic_metadata.partitions)}")
#         for partition, partition_metadata in topic_metadata.partitions.items():
#             print(f"    Partition: {partition}")
#             print(f"    Replicas: {partition_metadata.replicas}")
#             print(f"    Leader: {partition_metadata.leader}")
#
#         print("--------------------------------------------------------")
#     return topics


def get_cluster_info():
    admin_client = AdminClient(admin_config)
    metadata = admin_client.list_topics(timeout=5)

    topics = []
    for topic, topic_metadata in metadata.topics.items():
        partitions = [
            {
                "id": partition.id,
                "leader": partition.leader,
                "replicas": partition.replicas,
            }
            for partition in topic_metadata.partitions.values()
        ]

        topics.append({
            "topic": topic,
            "partitions": partitions
        })

    return topics


def create_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = AdminClient(admin_config)
    new_topic = NewTopic(topic_name, num_partitions=num_partitions, replication_factor=replication_factor)
    create_result = admin_client.create_topics([new_topic])
    for topic, future in create_result.items():
        try:
            future.result()
            print(f"Topic '{topic}' created successfully")
        except Exception as e:
            print(f"Failed to create topic '{topic}': {e}")


def delete_topic(topic_name):
    admin_client = AdminClient(admin_config)
    delete_result = admin_client.delete_topics([topic_name])
    for topic, future in delete_result.items():
        try:
            future.result()
            print(f"Topic '{topic}' deleted successfully")
        except Exception as e:
            print(f"Failed to delete topic '{topic}': {e}")


def delete_all_topics():
    admin_client = AdminClient(admin_config)
    metadata = admin_client.list_topics(timeout=5)
    exclude = ["__consumer_offsets"]
    topics = [topic for topic in metadata.topics if topic not in exclude]
    if not topics:
        print("No topics to delete")
        return
    delete_result = admin_client.delete_topics(topics)
    for topic, future in delete_result.items():
        try:
            future.result()
            print(f"Topic '{topic}' deleted successfully")
        except Exception as e:
            print(f"Failed to delete topic '{topic}': {e}")

def list_consumer_groups():
    admin_client = AdminClient(admin_config)
    return admin_client.list_consumer_groups()

def describe_consumer_groups(consumer_groups):
    admin_client = AdminClient(admin_config)
    for group in consumer_groups.valid:
        group_id = group.group_id
        group_metadata = admin_client.describe_consumer_groups([group_id])
        group_metadata = group_metadata[group_id].result()
        print(group_metadata)
        if group_metadata:
            print(f"Consumer Group: {group_id}")
            print(f"  State: {group.state}")
            print(f"  Coordinator: {group_metadata.coordinator}")
            print(f"  Members:")
            for member in group_metadata.members:
                print(f"    {member.member_id}: {member.client_id} ({member.host})")
        else:
            print(f"Failed to describe consumer group {group_id}")

# create_topic("astra", 5, 3)

cluster_info = get_cluster_info()
for topic_info in cluster_info:
    print(f"Topic: {topic_info['topic']}")
    for partition_info in topic_info['partitions']:
        print(
            f"  Partition {partition_info['id']}: Leader={partition_info['leader']}, Replicas-Brokers={partition_info['replicas']}")


# create_topic("emad", 5, 3)
# delete_all_topics()

# List consumer groups
admin_client = AdminClient(admin_config)
consumer_groups = admin_client.list_consumer_groups()
consumer_groups = consumer_groups.result()
describe_consumer_groups(consumer_groups)
