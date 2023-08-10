import aio_pika
import asyncio,random

async def process_message(message: str):
    # Simulate a delay in processing
    print(f"Processing message : {message}")
    processing_time = random.randint(3,10)
    await asyncio.sleep(processing_time)
    print(f"Processed message : {message}")
    return f"{message} World"


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        body = message.body.decode()
        processed_message = await process_message(body)
        connection = await aio_pika.connect_robust(host="172.26.0.4",port=5672)
        channel = await connection.channel()
        await channel.declare_queue("output_queue")
        print(f"Sending processed message : {processed_message}")
        # Use the default exchange to publish the processed message to the output_queue
        await channel.default_exchange.publish(
            aio_pika.Message(body=processed_message.encode()),
            routing_key="output_queue"
        )
        print(f"Sent processed message : {processed_message}")
        await connection.close()


async def main():
    connection = await aio_pika.connect_robust(host="172.26.0.4",port=5672)
    channel = await connection.channel()
    input_queue = await channel.declare_queue("input_queue")
    await channel.set_qos(prefetch_count=1)
    await input_queue.consume(on_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
    # asyncio.run(main())
