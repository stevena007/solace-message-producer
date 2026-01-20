#!/usr/bin/env python3
"""Quick test of message generation without requiring a Solace broker."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from solace_producer import SolaceProducer

def test_message_generation():
    """Test the message generation functionality."""
    print("Testing Message Generation")
    print("=" * 80)
    
    # Create a producer instance (without connecting)
    producer = SolaceProducer(
        host="tcp://test:55555",
        vpn="test",
        username="test"
    )
    
    # Test JSON generation
    print("\n1. Testing JSON message generation (500 bytes):")
    print("-" * 80)
    json_msg = producer.generate_content("json", 500)
    print(json_msg)
    print(f"\nActual size: {len(json_msg)} bytes")
    
    # Test XML generation
    print("\n2. Testing XML message generation (500 bytes):")
    print("-" * 80)
    xml_msg = producer.generate_content("xml", 500)
    print(xml_msg)
    print(f"\nActual size: {len(xml_msg)} bytes")
    
    # Test larger message
    print("\n3. Testing larger JSON message (2048 bytes):")
    print("-" * 80)
    large_json = producer.generate_content("json", 2048)
    print(large_json[:200] + "...\n[truncated for display]")
    print(f"\nActual size: {len(large_json)} bytes")
    
    print("\n" + "=" * 80)
    print("✓ All message generation tests completed successfully!")
    print("=" * 80)

if __name__ == '__main__':
    test_message_generation()
