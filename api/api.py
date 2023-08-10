from fastapi import FastAPI, HTTPException
import aio_pika
import logging
import asyncio,random

app = FastAPI()

async def publish_to_queue(queue_name: str, message: str):
    connection = await aio_pika.connect_robust(host="rabbitmq",port=5672)
    channel = await connection.channel()
    await channel.declare_queue(queue_name)
    await channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=queue_name 
    )
    await connection.close()


async def get_processed_message_from_queue(queue_name: str):
    connection = await aio_pika.connect_robust(host="rabbitmq",port=5672)
    channel = await connection.channel()
    queue = await channel.declare_queue(queue_name)
    try:
        message = await queue.get()
        logging.info("Message in output_queue: ",message)
        
        if message:
            processed_message = message.body.decode()
            await message.ack()  
        else:
            processed_message = None
        return True, processed_message  
    except Exception as e:
        logging.error("output queue exception block: "+str(e),exc_info=True)
        return False, None       
    await connection.close()
    
@app.post("/message/")
async def get_display_message(message:str):
    try:
        
        await publish_to_queue("input_queue", message)
        print({"message": f"{message} sent for processing"})
        processed_message = await get_processed_message_from_queue("output_queue")
        if processed_message[0]:
            return {"processed_message": processed_message[1]}
        else:
            return {"message": "No processed messages available"}
        
    except Exception as e:
        logging.error(str(e),exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
    



# @app.post("/process_message/")
# async def process_message(message: str):
#     try:
#         await publish_to_queue("input_queue", message)
#         return {"message": "Message sent for processing"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/processed_message/")
# async def get_processed_message():
#     processed_message = await get_processed_message_from_queue("output_queue")
#     if processed_message:
#         return {"processed_message": processed_message}
#     else:
#         return {"message": "No processed messages available"}


#just for practice tried to handle both get and post request using only 1 URL
# @app.post("/messages/")
# @app.get("/messages/")
# async def get_and_display_messages(request:Request):
#     if request.method == 'POST':
#         try:
#             request_body  = await request.json()
#             message = request_body.get('message')
#             await publish_to_queue("input_queue", message)
#             return {"message": "Message sent for processing"}
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=str(e))
        
#     elif request.method == 'GET':
#         processed_message = await get_processed_message_from_queue("output_queue")
#         if processed_message:
#             return {"processed_message": processed_message}
#         else:
#             return {"message": "No processed messages available"}




