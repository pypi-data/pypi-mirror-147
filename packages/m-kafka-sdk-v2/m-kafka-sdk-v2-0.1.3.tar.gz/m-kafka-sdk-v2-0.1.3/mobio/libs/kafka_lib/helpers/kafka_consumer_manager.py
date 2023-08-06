import json
from abc import abstractmethod
from datetime import datetime, timedelta
from confluent_kafka.cimpl import KafkaError, KafkaException, Consumer
from mobio.libs.kafka_lib import RequeueStatus, KAFKA_BOOTSTRAP
from mobio.libs.kafka_lib.models.mongo.requeue_consumer_model import (
    RequeueConsumerModel,
)
from time import time


class BaseKafkaConsumer:
    def __init__(
            self,
            topic_name: object,
            group_id: object,
            client_mongo,
            retryable=True,
            session_timeout_ms=15000,
            bootstrap_server=None,
            consumer_config=None
    ):
        config = {
                "bootstrap.servers": KAFKA_BOOTSTRAP if not bootstrap_server else bootstrap_server,
                "group.id": group_id,
                "auto.offset.reset": "latest",
                "session.timeout.ms": session_timeout_ms,
            }
        if consumer_config:
            config.update(consumer_config)
        c = Consumer(
            config
        )
        self.client_mongo = client_mongo
        self.retryable = retryable

        self.topic_name = topic_name
        try:
            c.subscribe([self.topic_name])
            print("consume %s is started" % self.topic_name)

            while True:
                msg = c.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        print(
                            "%% %s [%d] reached end at offset %d\n"
                            % (msg.topic(), msg.partition(), msg.offset())
                        )
                    elif msg.error():
                        raise KafkaException(msg.error())
                else:
                    try:
                        key = msg.key()
                        message = msg.value().decode("utf-8")
                        payload = json.loads(message)

                        start_time = time()

                        self.process(payload, key)
                        end_time = time()
                        print(
                            "end: {} with total time: '[{:.3f}s]".format(
                                self.topic_name, end_time - start_time
                            )
                        )
                    except Exception as e:
                        print(
                            "MessageQueue::run - topic: {} ERR: {}".format(
                                self.topic_name, e
                            )
                        )
        except RuntimeError as e:
            print("something unexpected happened: {}: {}".format(self.topic_name, e))
        finally:
            print("consumer is stopped")
            c.close()

    def process(self, data, key=None):
        count_err = 0
        try:
            if "count_err" in data:
                count_err = int(data.pop("count_err"))
            self.message_handle(data=data)
        except Exception as e:
            print("consumer::run - topic: {} ERR: {}".format(self.topic_name, e))
            if data and self.retryable:
                count_err += 1
                data_error = {
                    "topic": self.topic_name,
                    "key": key.decode("ascii") if key else key,
                    "data": data,
                    "error": str(e),
                    "count_err": count_err,
                    "next_run": datetime.utcnow() + timedelta(minutes=5 + count_err),
                    "status": RequeueStatus.ENABLE
                    if count_err <= 10
                    else RequeueStatus.DISABLE,
                }
                result = RequeueConsumerModel(self.client_mongo).insert(data=data_error)
                print("RequeueConsumerModel result: {}".format(result))

    @abstractmethod
    def message_handle(self, data):
        pass
