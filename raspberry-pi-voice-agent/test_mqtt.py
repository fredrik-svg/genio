#!/usr/bin/env python3
"""
HiveMQ MQTT Connection Test Script
Testar anslutningen till HiveMQ Cloud broker
"""

import paho.mqtt.client as mqtt
import ssl
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.settings import (
    MQTT_BROKER, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD, MQTT_USE_TLS, MQTT_TOPIC
)

# Global variables for test
connection_successful = False
message_received = False
test_message = "Genio AI Test Message"

def on_connect(client, userdata, flags, rc):
    """Callback när anslutningen upprättas"""
    global connection_successful
    
    print("\n" + "="*60)
    if rc == 0:
        print("✅ MQTT Connection Successful!")
        connection_successful = True
        print(f"   Connected to: {MQTT_BROKER}:{MQTT_PORT}")
        print(f"   Client ID: {client._client_id.decode() if isinstance(client._client_id, bytes) else client._client_id}")
        
        # Subscribe to test topic
        test_topic = f"{MQTT_TOPIC}/test"
        client.subscribe(test_topic)
        print(f"   Subscribed to: {test_topic}")
        
        # Publish test message
        print(f"\n📤 Publishing test message...")
        client.publish(test_topic, test_message)
        print(f"   Topic: {test_topic}")
        print(f"   Message: '{test_message}'")
        
    else:
        print(f"❌ MQTT Connection Failed!")
        print(f"   Return code: {rc}")
        print("\n   Error codes:")
        print("   0: Connection successful")
        print("   1: Connection refused - incorrect protocol version")
        print("   2: Connection refused - invalid client identifier")
        print("   3: Connection refused - server unavailable")
        print("   4: Connection refused - bad username or password")
        print("   5: Connection refused - not authorised")
    print("="*60 + "\n")

def on_message(client, userdata, msg):
    """Callback när ett meddelande tas emot"""
    global message_received
    
    print("\n" + "="*60)
    print("📥 Message Received!")
    print(f"   Topic: {msg.topic}")
    print(f"   Payload: {msg.payload.decode()}")
    print(f"   QoS: {msg.qos}")
    print("="*60 + "\n")
    
    if msg.payload.decode() == test_message:
        message_received = True
        print("✅ Test message successfully received!")

def on_disconnect(client, userdata, rc):
    """Callback när anslutningen bryts"""
    if rc != 0:
        print(f"\n⚠️  Unexpected disconnection (code: {rc})")

def on_publish(client, userdata, mid):
    """Callback när meddelande publicerats"""
    print(f"✅ Message published successfully (Message ID: {mid})")

def test_mqtt_connection():
    """Huvudfunktion för att testa MQTT-anslutningen"""
    print("\n" + "="*60)
    print("HiveMQ MQTT Connection Test")
    print("="*60)
    
    # Display configuration
    print("\n📋 Configuration:")
    print(f"   Broker: {MQTT_BROKER}")
    print(f"   Port: {MQTT_PORT}")
    print(f"   Username: {'***' if MQTT_USERNAME else '(not set)'}")
    print(f"   Password: {'***' if MQTT_PASSWORD else '(not set)'}")
    print(f"   TLS/SSL: {MQTT_USE_TLS}")
    print(f"   Topic: {MQTT_TOPIC}")
    
    # Validate configuration
    if not MQTT_BROKER or MQTT_BROKER == "mqtt.example.com":
        print("\n❌ ERROR: MQTT broker not configured!")
        print("   Update config/config.yaml with your HiveMQ broker address")
        return False
    
    if not MQTT_USERNAME or not MQTT_PASSWORD:
        print("\n⚠️  WARNING: MQTT credentials not configured!")
        print("   HiveMQ Cloud requires username and password")
        print("   Update config/config.yaml or .env file")
        return False
    
    print("\n🔄 Initializing MQTT client...")
    
    # Create MQTT client
    client = mqtt.Client(client_id="genio_ai_test")
    
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_publish = on_publish
    
    # Set credentials
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # Enable TLS/SSL
    if MQTT_USE_TLS:
        print("🔒 Enabling TLS/SSL...")
        try:
            client.tls_set(
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            client.tls_insecure_set(False)
            print("   ✅ TLS/SSL configured")
        except Exception as e:
            print(f"   ❌ TLS/SSL configuration failed: {e}")
            return False
    
    # Connect to broker
    print(f"\n🔌 Connecting to {MQTT_BROKER}:{MQTT_PORT}...")
    print("   (This may take a few seconds...)")
    
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        
        # Wait for connection and message exchange
        timeout = 10
        elapsed = 0
        
        while elapsed < timeout:
            time.sleep(0.5)
            elapsed += 0.5
            
            # Check if test completed
            if connection_successful and message_received:
                break
        
        # Give some time for final callbacks
        time.sleep(1)
        
        # Stop loop and disconnect
        client.loop_stop()
        client.disconnect()
        
        # Print results
        print("\n" + "="*60)
        print("Test Results:")
        print("="*60)
        print(f"   Connection: {'✅ SUCCESS' if connection_successful else '❌ FAILED'}")
        print(f"   Publish/Subscribe: {'✅ SUCCESS' if message_received else '❌ FAILED'}")
        print("="*60 + "\n")
        
        if connection_successful and message_received:
            print("🎉 All tests passed! HiveMQ connection is working perfectly.")
            print("\nNext steps:")
            print("1. Update MQTT credentials in config/config.yaml")
            print("2. Run: python src/main.py")
            return True
        elif connection_successful:
            print("⚠️  Connection successful but message test failed.")
            print("   This might be a timing issue. Try running the test again.")
            return False
        else:
            print("❌ Connection test failed.")
            print("\nTroubleshooting:")
            print("1. Verify HiveMQ broker address is correct")
            print("2. Check username and password in config/config.yaml")
            print("3. Ensure port 8883 is open (not blocked by firewall)")
            print("4. Verify HiveMQ Cloud cluster is running")
            return False
            
    except Exception as e:
        print(f"\n❌ Connection error: {e}")
        print("\nCommon issues:")
        print("- Invalid credentials (check username/password)")
        print("- Network connectivity problems")
        print("- Firewall blocking port 8883")
        print("- HiveMQ cluster not accessible")
        return False

if __name__ == "__main__":
    print("\n" + "🤖 Genio AI - HiveMQ Connection Test" + "\n")
    success = test_mqtt_connection()
    sys.exit(0 if success else 1)
