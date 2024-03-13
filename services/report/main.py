import asyncio
from confluent_kafka.admin import AdminClient, NewTopic
from fastapi import FastAPI, Depends, HTTPException
from confluent_kafka import Producer, Consumer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

app = FastAPI()

list_of_brokers = ["localhost:8097", "localhost:8098", "localhost:8099"]
# list_of_brokers = ["172.27.0.2:30097"]
kafka_bootstrap_servers = ",".join(list_of_brokers)
print(kafka_bootstrap_servers)
admin_config = {"bootstrap.servers": kafka_bootstrap_servers}

kafka_topic = "your_topic"
loop = asyncio.get_event_loop()
list_of_consumers_actions = {}
topic_list_to_subscribe = []

def create_topic(topic_name, num_partitions, replication_factor):
    admin_client = AdminClient({'bootstrap.servers': kafka_bootstrap_servers})

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


@app.on_event("shutdown")
async def shutdown_event():
    if app.state.kafka_consumer:
        await app.state.kafka_consumer.stop()

    if app.state.kafka_producer:
        await app.state.kafka_producer.stop()


def get_kafka_producer():
    return AIOKafkaProducer(bootstrap_servers=kafka_bootstrap_servers)


async def shutdown_app():
    # Stop the Kafka consumer
    if hasattr(app.state, 'kafka_consumer'):
        await app.state.kafka_consumer.stop()

    # Stop the Kafka producer
    if hasattr(app.state, 'kafka_producer'):
        await app.state.kafka_producer.stop()

    # Close the FastAPI application
    print("Shutting down FastAPI server")
    loop = asyncio.get_event_loop()
    loop.stop()
def get_kafka_consumer():
    admin_client = AdminClient(admin_config)
    # Check if the topic already exists
    existing_topics = admin_client.list_topics().topics
    # Check topic_list_to_subscribe is same as existing_topics
    topic_missing = False
    for topic in topic_list_to_subscribe:
        if topic not in existing_topics:
            print(f"Topic '{topic}' does not exist.")
            topic_missing = True

    if topic_missing:
        raise Exception("Topic missing")

    return AIOKafkaConsumer(
        *topic_list_to_subscribe,
        loop=loop,
        bootstrap_servers=kafka_bootstrap_servers,
        group_id="my_consumer_group",
        client_id="femto_client"
    )


async def startup_event():
    kafka_producer = get_kafka_producer()
    print("Producer started")
    await kafka_producer.start()
    print("Producer Connected")
    app.state.kafka_producer = kafka_producer


    # Start Kafka consumer
    kafka_consumer = get_kafka_consumer()
    app.state.kafka_consumer = kafka_consumer
    asyncio.create_task(consume_message())


async def consume_message():
    consumer = app.state.kafka_consumer
    print(list_of_consumers_actions)
    print("Consumer started")
    try:
        await consumer.start()

    except Exception as e:
        print(e)
        return

    try:
        async for msg in consumer:
            key = msg.key.decode("utf-8")
            body = msg.value.decode("utf-8")
            topic = msg.topic
            if (topic, key) in list_of_consumers_actions:
                await list_of_consumers_actions[(topic, key)](key, msg)
            # print(f"Consumed message: {msg.topic} - {msg.partition} - {msg.offset} - {msg.key} - {msg.value}")
            # await msg.ack()
    finally:
        await consumer.stop()
        await app.state.kafka_producer.stop()


@app.get("/{topic}/{key}/{message}")
async def read_root(topic: str, key: str, message: str):
    await app.state.kafka_producer.send_and_wait(topic, key=key.encode("utf-8"), value=message.encode("utf-8"))
    return {"Message": f"To be sent to {topic} with key {key} and message {message}"}


def consumer_action(topic, action):
    def decorator(func):
        list_of_consumers_actions[(topic, action)] = func
        if topic not in topic_list_to_subscribe:
            topic_list_to_subscribe.append(topic)
        return func

    return decorator






@consumer_action(topic="astra", action="print")
async def print_message(key, msg):
    print(f"Consumed mesaasage: {msg.topic} - {msg.partition} - {msg.offset} - {msg.key} - {msg.value}")


@consumer_action(topic="emad", action="ping")
async def print_message(key, msg):
    print(f"Consumed priernt: {msg.topic} - {msg.partition} - {msg.offset} - {msg.key} - {msg.value}")




# @consumer_action(topic="marioNageh", action="ping")
# async def print_eeeee(key, msg):
#     print(f"Consumed priernt: {msg.topic} - {msg.partition} - {msg.offset} - {msg.key} - {msg.value}")

# create_topic("mario", 2, 2)
asyncio.create_task(startup_event())


# Compression
# ack
# https://kafka.apache.org/documentation/#topicconfigs