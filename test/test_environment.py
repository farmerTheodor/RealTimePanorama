
import kafka
import pytest


def test_environment():
    assert True

def test_kafka_server():
    consumer = kafka.KafkaConsumer('jpg_stream',group_id='panoramastream', bootstrap_servers=["127.0.0.1:9092"])
    for msg in consumer:
        print(msg)
        break
    assert True