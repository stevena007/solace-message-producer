#!/usr/bin/env python3
"""
Solace Message Producer
A Python application that sends messages to a Solace topic with configurable parameters.
"""

import argparse
import json
import random
import string
import time
import sys
from typing import Optional
from datetime import datetime

from solace.messaging.messaging_service import MessagingService
from solace.messaging.resources.topic import Topic
from solace.messaging.publisher.direct_message_publisher import PublishFailureListener
from solace.messaging.config.solace_properties import (
    transport_layer_properties,
    service_properties,
    authentication_properties
)
from solace.messaging.config.transport_security_strategy import TLS


class MessagePublishFailureListener(PublishFailureListener):
    """Listener for handling publish failures."""
    
    def on_failed_publish(self, e: 'FailedPublishEvent'):
        print(f"Message publish failed: {e}")


class SolaceProducer:
    """Solace message producer with configurable parameters."""
    
    def __init__(self, host: str, vpn: str, username: str, password: Optional[str] = None):
        """Initialize the Solace producer.
        
        Args:
            host: Solace broker host (e.g., tcp://localhost:55555)
            vpn: Message VPN name
            username: Username for authentication
            password: Password for authentication (optional)
        """
        self.host = host
        self.vpn = vpn
        self.username = username
        self.password = password
        self.messaging_service = None
        self.publisher = None
    
    def connect(self):
        """Connect to the Solace broker."""
        broker_props = {
            transport_layer_properties.HOST: self.host,
            service_properties.VPN_NAME: self.vpn,
            authentication_properties.SCHEME_BASIC_USER_NAME: self.username,
        }
        
        if self.password:
            broker_props[authentication_properties.SCHEME_BASIC_PASSWORD] = self.password
        
        try:
            # Build and connect the messaging service
            self.messaging_service = MessagingService.builder().from_properties(broker_props).build()
            self.messaging_service.connect()
            print(f"✓ Connected to Solace broker at {self.host}")
            
            # Build and start the publisher
            self.publisher = self.messaging_service.create_direct_message_publisher_builder().build()
            self.publisher.set_publish_failure_listener(MessagePublishFailureListener())
            self.publisher.start()
            print(f"✓ Publisher started")
            
        except Exception as e:
            print(f"✗ Failed to connect to Solace broker: {e}")
            sys.exit(1)
    
    def disconnect(self):
        """Disconnect from the Solace broker."""
        if self.publisher:
            self.publisher.terminate()
            print("✓ Publisher terminated")
        
        if self.messaging_service:
            self.messaging_service.disconnect()
            print("✓ Disconnected from Solace broker")
    
    def generate_content(self, content_type: str, size: int) -> str:
        """Generate message content of specified type and size.
        
        Args:
            content_type: Type of content ('json' or 'xml')
            size: Target size in bytes
            
        Returns:
            Generated content as string
        """
        # Generate random text data to fill the message
        random_text = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=max(1, size - 200)))
        
        if content_type.lower() == 'json':
            data = {
                "timestamp": datetime.now().isoformat(),
                "messageId": ''.join(random.choices(string.ascii_letters + string.digits, k=16)),
                "data": random_text
            }
            content = json.dumps(data, indent=2)
        else:  # xml
            content = f"""<?xml version="1.0" encoding="UTF-8"?>
<message>
    <timestamp>{datetime.now().isoformat()}</timestamp>
    <messageId>{''.join(random.choices(string.ascii_letters + string.digits, k=16))}</messageId>
    <data>{random_text}</data>
</message>"""
        
        # Adjust size if needed
        if len(content) < size:
            padding = ' ' * (size - len(content))
            if content_type.lower() == 'json':
                data["padding"] = padding
                content = json.dumps(data, indent=2)
            else:
                content = content.replace('</message>', f'    <padding>{padding}</padding>\n</message>')
        elif len(content) > size:
            # Truncate if too large
            content = content[:size]
        
        return content
    
    def send_messages(
        self,
        topic_name: str,
        num_messages: int,
        message_size: int,
        content_type: str,
        rate: float,
        show_messages: bool = False
    ):
        """Send messages to the specified topic.
        
        Args:
            topic_name: Name of the topic to publish to
            num_messages: Number of messages to send
            message_size: Size of each message in bytes
            content_type: Type of content ('json' or 'xml')
            rate: Messages per second
            show_messages: Whether to display messages being sent
        """
        topic = Topic.of(topic_name)
        delay = 1.0 / rate if rate > 0 else 0
        
        print(f"\nSending {num_messages} messages to topic '{topic_name}'")
        print(f"Message size: {message_size} bytes")
        print(f"Content type: {content_type}")
        print(f"Send rate: {rate} msg/sec")
        print(f"Show messages: {show_messages}")
        print("-" * 80)
        
        sent_count = 0
        failed_count = 0
        start_time = time.time()
        
        for i in range(num_messages):
            try:
                # Generate message content
                content = self.generate_content(content_type, message_size)
                
                # Publish the message
                self.publisher.publish(destination=topic, message=content)
                sent_count += 1
                
                # Display message if requested
                if show_messages:
                    print(f"\n[Message {i + 1}/{num_messages}]")
                    print(content)
                    print("-" * 80)
                else:
                    # Show progress
                    if (i + 1) % max(1, num_messages // 10) == 0 or i == num_messages - 1:
                        print(f"Progress: {i + 1}/{num_messages} messages sent")
                
                # Rate control
                if delay > 0 and i < num_messages - 1:
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"✗ Failed to send message {i + 1}: {e}")
                failed_count += 1
        
        # Summary
        end_time = time.time()
        elapsed_time = end_time - start_time
        actual_rate = sent_count / elapsed_time if elapsed_time > 0 else 0
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Total messages sent: {sent_count}")
        print(f"Failed messages: {failed_count}")
        print(f"Elapsed time: {elapsed_time:.2f} seconds")
        print(f"Actual send rate: {actual_rate:.2f} msg/sec")
        print("=" * 80)


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description='Solace Message Producer - Send messages to a Solace topic',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Send 100 JSON messages of 1KB each at 10 msg/sec
  python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \\
    --topic test/topic --count 100 --size 1024 --rate 10 --type json

  # Send 50 XML messages and show each message
  python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \\
    --topic test/topic --count 50 --size 512 --rate 5 --type xml --show
        """
    )
    
    # Connection parameters
    parser.add_argument('--host', required=True,
                        help='Solace broker host (e.g., tcp://localhost:55555)')
    parser.add_argument('--vpn', required=True,
                        help='Message VPN name')
    parser.add_argument('--username', required=True,
                        help='Username for authentication')
    parser.add_argument('--password', default=None,
                        help='Password for authentication (optional)')
    
    # Message parameters
    parser.add_argument('--topic', required=True,
                        help='Topic to publish messages to')
    parser.add_argument('--count', type=int, required=True,
                        help='Number of messages to send')
    parser.add_argument('--size', type=int, required=True,
                        help='Size of each message in bytes')
    parser.add_argument('--rate', type=float, required=True,
                        help='Send rate in messages per second')
    parser.add_argument('--type', choices=['json', 'xml'], default='json',
                        help='Message content type (default: json)')
    parser.add_argument('--show', action='store_true',
                        help='Show each message being sent')
    
    args = parser.parse_args()
    
    # Validate parameters
    if args.count <= 0:
        print("Error: count must be greater than 0")
        sys.exit(1)
    
    if args.size <= 0:
        print("Error: size must be greater than 0")
        sys.exit(1)
    
    if args.rate <= 0:
        print("Error: rate must be greater than 0")
        sys.exit(1)
    
    # Create and run the producer
    producer = SolaceProducer(
        host=args.host,
        vpn=args.vpn,
        username=args.username,
        password=args.password
    )
    
    try:
        producer.connect()
        producer.send_messages(
            topic_name=args.topic,
            num_messages=args.count,
            message_size=args.size,
            content_type=args.type,
            rate=args.rate,
            show_messages=args.show
        )
    except KeyboardInterrupt:
        print("\n\n✗ Interrupted by user")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    finally:
        producer.disconnect()


if __name__ == '__main__':
    main()
