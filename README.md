# Solace Message Producer

A Python application that sends configurable messages to a Solace topic with support for JSON and XML content generation.

## Features

- ✅ Send configurable number of messages to a Solace topic
- ✅ Customizable message size (in bytes)
- ✅ Configurable send rate (messages per second)
- ✅ Support for JSON and XML message formats
- ✅ Automatic content generation with random data
- ✅ Optional message display for debugging
- ✅ Progress tracking and performance summary
- ✅ Error handling and connection management

## Requirements

- Python 3.7 or higher
- Access to a Solace PubSub+ broker (local or cloud)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/stevena007/solace-message-producer.git
cd solace-message-producer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Command

```bash
python solace_producer.py --host <BROKER_HOST> --vpn <VPN_NAME> --username <USERNAME> \
  --topic <TOPIC_NAME> --count <NUM_MESSAGES> --size <MESSAGE_SIZE> --rate <SEND_RATE>
```

### Parameters

**Connection Parameters:**
- `--host`: Solace broker host (e.g., `tcp://localhost:55555` or `tcps://cloud-broker.solace.com:55443`)
- `--vpn`: Message VPN name
- `--username`: Username for authentication
- `--password`: Password for authentication (optional)

**Message Parameters:**
- `--topic`: Topic to publish messages to
- `--count`: Number of messages to send
- `--size`: Size of each message in bytes
- `--rate`: Send rate in messages per second
- `--type`: Message content type - `json` or `xml` (default: `json`)
- `--show`: Show each message being sent (optional flag)

### Examples

#### Send 100 JSON messages of 1KB each at 10 msg/sec
```bash
python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \
  --topic test/messages --count 100 --size 1024 --rate 10 --type json
```

#### Send 50 XML messages and display each one
```bash
python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \
  --topic test/messages --count 50 --size 512 --rate 5 --type xml --show
```

#### Send messages to a cloud broker with authentication
```bash
python solace_producer.py --host tcps://cloud.solace.com:55443 --vpn my-vpn \
  --username my-user --password my-password --topic production/data \
  --count 1000 --size 2048 --rate 50 --type json
```

#### High-volume testing (1000 messages at 100 msg/sec)
```bash
python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \
  --topic load/test --count 1000 --size 500 --rate 100 --type json
```

## Message Format

### JSON Format
Messages are generated with the following structure:
```json
{
  "timestamp": "2024-01-20T12:34:56.789",
  "messageId": "abc123def456",
  "data": "random content to fill message size..."
}
```

### XML Format
Messages are generated with the following structure:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<message>
    <timestamp>2024-01-20T12:34:56.789</timestamp>
    <messageId>abc123def456</messageId>
    <data>random content to fill message size...</data>
</message>
```

## Output

The application provides:
- Connection status
- Progress updates during sending
- Summary statistics including:
  - Total messages sent
  - Failed messages
  - Elapsed time
  - Actual send rate

## Setting Up a Local Solace Broker

For testing, you can run a local Solace PubSub+ broker using Docker:

```bash
docker run -d -p 55555:55555 -p 8080:8080 -p 8008:8008 -p 1883:1883 -p 8000:8000 -p 5672:5672 \
  --shm-size=2g --env username_admin_globalaccesslevel=admin --env username_admin_password=admin \
  --name=solace solace/solace-pubsub-standard:latest
```

Then use these connection parameters:
- Host: `tcp://localhost:55555`
- VPN: `default`
- Username: `default`
- Password: (leave empty)

## Error Handling

The application handles:
- Connection failures with clear error messages
- Publishing failures with detailed logging
- Keyboard interrupts (Ctrl+C) for graceful shutdown
- Parameter validation

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.