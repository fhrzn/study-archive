from fastapi import FastAPI, Request, Response
import asyncio
import logging
from rmq import PikaClient
import threading

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(name)s - %(message)s")
logger = logging.getLogger(__name__)


app = FastAPI()


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    # inspired from https://gist.github.com/dmfigol/3e7d5b84a16d076df02baa9f53271058
    asyncio.set_event_loop(loop)
    loop.run_forever()


@app.on_event("startup")
async def start_rmq():
    # start producer
    app.rmq_producer = PikaClient(queue_name="test.queue",
                                        exchange_name="test.exchange",
                                        conn_str="amqp://root:root@127.0.0.1:5672")
    await app.rmq_producer.start_producer()

    # start consumer in other thread
    app.rmq_consumer = PikaClient(queue_name="test.queue",
                                  exchange_name="test.exchange",
                                  conn_str="amqp://root:root@127.0.0.1:5672")
    
    app.consumer_loop = asyncio.new_event_loop()
    tloop = threading.Thread(target=start_background_loop, args=(app.consumer_loop,), daemon=True)
    tloop.start()

    _ = asyncio.run_coroutine_threadsafe(app.rmq_consumer.start_consumer(), app.consumer_loop)


@app.on_event("shutdown")
async def shutdown_rmq():
    await app.rmq_producer.disconnect()
    await app.rmq_consumer.disconnect()

    app.consumer_loop.stop()


@app.get("/")
def root(response: Response):
    response.status_code = 200
    logger.info("hit root endpoint")
    return {"status_code": 200, "message": "Hello!"}


@app.get("/send-message")
async def send_message(request: Request, response: Response):
    message = "Hello from RMQ producer!"
    response.status_code = 202
    logger.info("message sent")
    await request.app.rmq_producer.publish_message(message)
    return {"status_code": 202, "message": "Your message has been sent."}