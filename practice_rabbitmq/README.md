# practice_rabbitmq
Created a fast-API application that would publish a simple message on a message queue in rabbitmq.  A core python processer.py that would listen to this message and append "World" to it, and publish the message on a different topic. Now fast API application has to listen to that processed message and return the processed message to client. 

 processor.py

The `processor.py` script is responsible for processing messages from the `input_queue` and publishing the processed messages to the `output_queue`. It acts as a worker that listens to incoming messages, processes them, and then forwards the processed messages to another queue.

Here's a step-by-step explanation of the `processor.py` code:

1. **Imports**: The script starts by importing the required module, `pika`, which is the RabbitMQ client library for Python. It provides functionalities to interact with RabbitMQ, such as connecting to the server, declaring queues, and sending/receiving messages.

2. **process_message() function**: This function is responsible for processing the message received from the `input_queue`. In this example, the processing involves appending the string "World" to the received message.

3. **on_message() function**: This is the callback function that will be invoked when a message is received from the `input_queue`. The function takes several parameters:
   - `channel`: The channel object that the message was received on.
   - `method_frame`: A method frame containing message metadata.
   - `header_frame`: A header frame containing message properties.
   - `body`: The message body, which contains the actual content.

   When a message arrives in the `input_queue`, this function is called. It extracts the message body, processes it using the `process_message()` function, and then publishes the processed message to the `output_queue`.

4. **main() function**: The main function sets up the connection, channel, and the `input_queue`. It then starts consuming messages from the `input_queue` by calling `channel.basic_consume()` and passing `on_message` as the callback function. This means that whenever a message is available in the `input_queue`, the `on_message()` function will be called to process it.

5. **if __name__ == '__main__':** The script checks whether it is being executed directly (as opposed to being imported as a module). If it is the main script being executed, it calls the `main()` function to start the message consumption and processing loop.

api.py 

The `api.py` script is the FastAPI application responsible for exposing two endpoints: one to publish messages to the `input_queue` and another to retrieve processed messages from the `output_queue`.

Here's a step-by-step explanation of the final `api.py` code:

1. **Imports**: The script starts by importing the required modules: `FastAPI`, `HTTPException`, `pika`, and `JSONResponse`. 
   - `FastAPI`: The FastAPI framework to build the API.
   - `HTTPException`: To raise custom HTTP exceptions with specific status codes and details.
   - `pika`: The RabbitMQ client library for Python to publish messages to the `input_queue`.
   - `JSONResponse`: To return JSON-formatted responses to the client.

2. **publish_to_queue() function**: This function is responsible for publishing messages to the `input_queue`. It uses `pika` to establish a connection to RabbitMQ and then publishes the message to the specified queue.

3. **get_processed_message_from_queue() function**: This function retrieves the processed message from the `output_queue`. It uses `pika` to establish a connection to RabbitMQ, gets the message from the queue, and returns it. If no message is available, it returns `None`.

4. **/publish_message/ Endpoint**: This is a POST endpoint with the route `/publish_message/`. When the client sends a POST request to this endpoint with a JSON payload containing the `"message"` key, the function `publish_message()` is executed. This function takes the message from the JSON payload and calls `publish_to_queue()` to publish the message to the `input_queue`. It returns a response to the client with a success message.

5. **/processed_message/ Endpoint**: This is a GET endpoint with the route `/processed_message/`. When the client sends a GET request to this endpoint, the function `get_processed_message()` is executed. This function calls `get_processed_message_from_queue()` to retrieve the processed message from the `output_queue`. If a processed message is available, it returns a JSON response with the processed message. If no processed message is available, it returns a JSON response with a message indicating that no messages are available.

6. **Running the FastAPI app**: Finally, the script runs the FastAPI app using the `uvicorn` server with the command `uvicorn app:app --reload`.

With this `api.py`, clients can send POST requests to `/publish_message/` with a JSON payload containing the message to publish to the `input_queue`. They can also send GET requests to `/processed_message/` to retrieve the processed message from the `output_queue`.

When the FastAPI application receives a message on `/publish_message/`, it publishes the message to the `input_queue`. The `processor.py` script, running separately, consumes messages from the `input_queue`, processes them, and publishes the processed messages to the `output_queue`. The FastAPI application can then fetch these processed messages from the `output_queue` in response to the client's GET request.
