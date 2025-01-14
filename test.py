import pika
import requests
import json
import sys
import time

class EventDrivenWrapper:
    def __init__(self, rabbitmq_url, queue_name, api_endpoint):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name
        self.api_endpoint = api_endpoint
        self.connection = None
        self.channel = None

    def on_message(self, channel, method_frame, header_frame, body):
        print(f"Received message: {body}")
        try:
            # Parse the message
            message = json.loads(body.decode('utf-8'))  # Decode bytes to string
            # Trigger the API call
            self.trigger_api(message)
        except json.JSONDecodeError as e:
            print(f"Failed to decode message: {e}")
        except Exception as e:
            print(f"Error processing message: {e}")
        finally:
            # Acknowledge the message
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)

    def trigger_api(self, message):
        try:
            response = requests.post(self.api_endpoint, json=message, timeout=10)  # Added timeout
            response.raise_for_status()  # Raise exception for bad status codes
            print("API call successful")
        except requests.RequestException as e:
            print(f"API call failed: {e}")

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)
            return True
        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            return False

    def start_listening(self):
        max_retries = 5
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                if not self.connect():
                    raise Exception("Failed to establish connection")

                self.channel.basic_consume(
                    queue=self.queue_name,
                    on_message_callback=self.on_message
                )
                print("Listening for messages...")
                self.channel.start_consuming()

            except KeyboardInterrupt:
                print("\nShutting down...")
                if self.connection and not self.connection.is_closed:
                    self.connection.close()
                sys.exit(0)

            except Exception as e:
                print(f"Error occurred: {e}")
                if self.connection and not self.connection.is_closed:
                    self.connection.close()
                
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Exiting...")
                    sys.exit(1)

if __name__ == "__main__":
    # For testing, you might want to use a public test AMQP server or local RabbitMQ instance
    rabbitmq_url = "amqp://guest:guest@localhost:5672/"
    queue_name = "event_queue"
    api_endpoint = "https://httpbin.org/post"  # Test endpoint

    wrapper = EventDrivenWrapper(rabbitmq_url, queue_name, api_endpoint)
    wrapper.start_listening()