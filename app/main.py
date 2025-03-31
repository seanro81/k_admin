import asyncio

from aiokafka import AIOKafkaConsumer,AIOKafkaProducer
from aiokafka.errors import (
                               KafkaError,
                               ConsumerStoppedError,
                               IllegalStateError,
                               RecordTooLargeError,
                               UnsupportedVersionError)

from ssl import create_default_context, Purpose, CERT_NONE,CERT_REQUIRED,CERT_OPTIONAL,TLSVersion
import logging
from dotenv import load_dotenv

load_dotenv()


TOPIC_NAME = 'test_topic_ssl_connect'
KAFKA_SERVERS = 'localhost:9094,localhost:9095,localhost:9096'

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def create_ssl_context():
    ssl_context = create_default_context(Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = CERT_NONE
    ssl_context.load_cert_chain(certfile='', keyfile='')
    return ssl_context


async def kafka_init():
    aio_consumer = None
    AIO_KAFKA_CONSUMER_START = False
    try:
        cntx = create_ssl_context()
        aio_consumer = AIOKafkaConsumer(TOPIC_NAME,
                                        bootstrap_servers=KAFKA_SERVERS,
                                        group_id='custom_metrics_consumer',
                                        enable_auto_commit=True,
                                        retry_backoff_ms=200,
                                        security_protocol='SSL',
                                        ssl_context=cntx
                                        )
        await aio_consumer.start()
        AIO_KAFKA_CONSUMER_START = True
    except (KafkaError, ConsumerStoppedError, IllegalStateError, RecordTooLargeError,
            UnsupportedVersionError) as ex:
        logging.error(f"KAFKA ERROR - {str(ex)}")
    finally:
        if aio_consumer and AIO_KAFKA_CONSUMER_START is False:
            await aio_consumer.stop()
            await asyncio.sleep(1)
    logging.info("KAFKA CONSUMER START")
    return aio_consumer, AIO_KAFKA_CONSUMER_START



""""
async def consumer():
    aio_consumer = None
    AIO_KAFKA_CONSUMER_START = False

    while not AIO_KAFKA_CONSUMER_START:
        aio_consumer, start = await kafka_init()
        AIO_KAFKA_CONSUMER_START = start

    while True:
        try:
            async for msg in aio_consumer:
                logging.info(f"KAFKA GET NEW MESSAGE:{msg.value}")
                orm = SimpleORM()
                message = msg.value.decode("utf-8")
                await orm.metrics_register(json_data=message, metric_id='all')
        except Exception as ex:
            logging.error(f"KAFKA ERROR - {str(ex)}")
"""
async def send_and_consume():
    producer = AIOKafkaProducer
