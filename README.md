# Event-Driven API Wrapper

A robust Python wrapper that listens to RabbitMQ messages and triggers API calls based on received events. This wrapper provides reliable message handling with automatic retries, error handling, and message acknowledgment.

## Features

- 🐰 RabbitMQ message consumption with automatic connection management
- 🔄 Automatic reconnection with configurable retries
- ✅ Message acknowledgment to ensure reliable message processing
- 🚀 HTTP API integration with timeout handling
- 🛡️ Comprehensive error handling and logging
- 💪 Durable queue support for message persistence

## Prerequisites

- Python 3.6+
- RabbitMQ Server
- Required Python packages (see Installation section)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/event-driven-wrapper.git
cd event-driven-wrapper
```

2. Install the required packages:
```bash
pip install pika requests
```

## Usage

```python
from event_wrapper import EventDrivenWrapper

# Configure your settings
rabbitmq_url = "amqp://guest:guest@localhost:5672/"
queue_name = "event_queue"
api_endpoint = "https://your-api-endpoint.com/path"

# Initialize and start the wrapper
wrapper = EventDrivenWrapper(rabbitmq_url, queue_name, api_endpoint)
wrapper.start_listening()
```

### Configuration Parameters

- `rabbitmq_url`: The URL for your RabbitMQ server
- `queue_name`: The name of the queue to consume messages from
- `api_endpoint`: The endpoint where messages will be forwarded

## Message Format

The wrapper expects messages in JSON format. For example:

```json
{
    "event_type": "user_action",
    "data": {
        "user_id": "123",
        "action": "login"
    }
}
```

## Error Handling

The wrapper includes several error handling mechanisms:

- Connection retry logic with configurable attempts and delay
- Message parsing error handling
- API call error handling with timeout
- Graceful shutdown on keyboard interrupt

## Development and Testing

For testing purposes, you can use the provided example configuration:

```python
rabbitmq_url = "amqp://guest:guest@localhost:5672/"
queue_name = "event_queue"
api_endpoint = "https://httpbin.org/post"  # Test endpoint
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- RabbitMQ team for their excellent messaging system
- Pika library developers for the Python RabbitMQ client
- Requests library team for the HTTP client library
