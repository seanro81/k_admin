import asyncio

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import (
    KafkaError,
    ConsumerStoppedError,
    IllegalStateError,
    RecordTooLargeError,
    UnsupportedVersionError)

from ssl import create_default_context, Purpose, CERT_NONE, CERT_REQUIRED, CERT_OPTIONAL, TLSVersion
import logging
from dotenv import load_dotenv

load_dotenv()

TOPIC_NAME = 'test_topic_ssl_connect'
KAFKA_SERVERS = 'localhost:9096,localhost:9093,localhost:9092'

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,
                    datefmt="%H:%M:%S")


def create_ssl_context():
    ssl_context = create_default_context(Purpose.SERVER_AUTH)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = CERT_NONE
    ssl_context.load_cert_chain(certfile='ca.crt', keyfile='ca.key')
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
                                        ssl_context=cntx,
                                        sasl_plain_username='consumer',
                                        sasl_plain_password='test123'
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


async def send_and_consume():
    try:
        cntx = create_ssl_context()
        logging.info("Инициализация коннекта - отправка сообщений")
        producer = AIOKafkaProducer(client_id='producer_tst',
                                    bootstrap_servers=KAFKA_SERVERS,
                                    security_protocol='SSL',
                                    ssl_context=cntx,
                                    sasl_plain_username='consumer',
                                    sasl_plain_password='test123'
                                    )
        await producer.start()
        res = await producer.send_and_wait(topic=TOPIC_NAME, value='test message'.encode('utf-8'))
        logging.info(str(res))
        await producer.stop()

        await asyncio.sleep(3)

        aio_consumer, start = await kafka_init()
        async for msg in aio_consumer:
            logging.info(f"KAFKA GET NEW MESSAGE:{msg.value}")
    except Exception as ex:
        logging.error(f"KAFKA ERROR - {str(ex)}")


asyncio.run(send_and_consume())
