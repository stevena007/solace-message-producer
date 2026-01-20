#!/bin/bash
# Demo script showing different usage scenarios

echo "========================================="
echo "Solace Message Producer - Demo"
echo "========================================="
echo ""
echo "This demo shows how to use the Solace Message Producer"
echo "Note: You need a running Solace broker to execute these commands"
echo ""

# Demo 1
echo "1. Send 10 small JSON messages with display enabled:"
echo "   python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \\"
echo "     --topic demo/test --count 10 --size 300 --rate 2 --type json --show"
echo ""

# Demo 2
echo "2. Send 50 XML messages at moderate rate:"
echo "   python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \\"
echo "     --topic demo/test --count 50 --size 512 --rate 10 --type xml"
echo ""

# Demo 3
echo "3. High-volume test with 1000 messages:"
echo "   python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \\"
echo "     --topic demo/load-test --count 1000 --size 1024 --rate 100 --type json"
echo ""

# Demo 4
echo "4. Large messages (5KB) at slower rate:"
echo "   python solace_producer.py --host tcp://localhost:55555 --vpn default --username default \\"
echo "     --topic demo/large --count 20 --size 5120 --rate 5 --type xml"
echo ""

echo "========================================="
echo "Setup Instructions:"
echo "========================================="
echo ""
echo "To run a local Solace broker with Docker:"
echo "docker run -d -p 55555:55555 -p 8080:8080 \\"
echo "  --shm-size=2g --env username_admin_globalaccesslevel=admin \\"
echo "  --name=solace solace/solace-pubsub-standard:latest"
echo ""
echo "Wait 60 seconds for the broker to start, then try the commands above!"
echo ""
