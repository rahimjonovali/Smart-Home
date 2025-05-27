import paho.mqtt.client as mqtt
import json
import logging
from django.contrib.auth import get_user_model
from .models import SensorData, Broker
import threading
import time

User = get_user_model()
logger = logging.getLogger(__name__)

class MQTTService:
    def __init__(self):
        self.clients = {}
        self.running = False
    
    def start_mqtt_listeners(self):
        """Start MQTT listeners for all users with brokers"""
        if self.running:
            return
            
        self.running = True
        brokers = Broker.objects.all()
        
        for broker in brokers:
            try:
                self.create_client_for_user(broker)
            except Exception as e:
                logger.error(f"Failed to create MQTT client for user {broker.user.username}: {e}")
    
    def create_client_for_user(self, broker):
        """Create and start MQTT client for a specific user"""
        user_id = broker.user.id
        
        if user_id in self.clients:
            # Disconnect existing client
            self.clients[user_id].disconnect()
            del self.clients[user_id]
        
        client = mqtt.Client()
        
        # Set authentication if provided
        if broker.username and broker.password:
            client.username_pw_set(broker.username, broker.password)
        
        # Callbacks
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.info(f"Connected to MQTT broker for user {broker.user.username}")
                # Subscribe to sensor topics
                client.subscribe("home/relay1/photoresistor")
                client.subscribe("home/relay1/pir")
            else:
                logger.error(f"Failed to connect to MQTT broker for user {broker.user.username}: {rc}")
        
        def on_message(client, userdata, msg):
            try:
                topic = msg.topic
                payload = msg.payload.decode()
                
                # Get or create sensor data for this user
                sensor_data, created = SensorData.objects.get_or_create(user=broker.user)
                
                if topic == "home/relay1/photoresistor":
                    # Update photoresistor value
                    try:
                        sensor_data.photoresistor_value = int(payload)
                        sensor_data.save()
                        logger.info(f"Updated photoresistor value for user {broker.user.username}: {payload}")
                    except ValueError:
                        logger.error(f"Invalid photoresistor value: {payload}")
                
                elif topic == "home/relay1/pir":
                    # Update PIR sensor status
                    motion_detected = payload.lower() in ['motion', 'detected', '1', 'true']
                    sensor_data.pir_motion_detected = motion_detected
                    sensor_data.save()
                    logger.info(f"Updated PIR sensor for user {broker.user.username}: {payload}")
                    
                    # Auto control lamp based on mode
                    self.handle_automatic_control(sensor_data, broker)
                    
            except Exception as e:
                logger.error(f"Error processing MQTT message: {e}")
        
        def on_disconnect(client, userdata, rc):
            logger.info(f"Disconnected from MQTT broker for user {broker.user.username}")
        
        client.on_connect = on_connect
        client.on_message = on_message
        client.on_disconnect = on_disconnect
        
        # Connect to broker
        try:
            client.connect(broker.host, broker.port, 60)
            client.loop_start()
            self.clients[user_id] = client
            logger.info(f"MQTT client started for user {broker.user.username}")
        except Exception as e:
            logger.error(f"Failed to connect MQTT client for user {broker.user.username}: {e}")
    
    def handle_automatic_control(self, sensor_data, broker):
        """Handle automatic lamp control based on sensor data and mode"""
        try:
            if sensor_data.control_mode == 'pir':
                # PIR mode: turn on lamp when motion detected
                new_status = sensor_data.pir_motion_detected
                if sensor_data.lamp_status != new_status:
                    self.publish_lamp_command(broker, "ON" if new_status else "OFF")
                    sensor_data.lamp_status = new_status
                    sensor_data.save()
            
            elif sensor_data.control_mode == 'photoresistor':
                # Photoresistor mode: turn on lamp when it's dark (low value)
                # Assuming threshold of 300 (adjust based on your sensor)
                threshold = 300
                new_status = sensor_data.photoresistor_value < threshold
                if sensor_data.lamp_status != new_status:
                    self.publish_lamp_command(broker, "ON" if new_status else "OFF")
                    sensor_data.lamp_status = new_status
                    sensor_data.save()
                    
        except Exception as e:
            logger.error(f"Error in automatic control: {e}")
    
    def publish_lamp_command(self, broker, command):
        """Publish lamp control command"""
        try:
            import paho.mqtt.publish as publish
            publish.single(
                topic=broker.topic,
                payload=command,
                hostname=broker.host,
                port=broker.port,
                auth={'username': broker.username, 'password': broker.password}
            )
            logger.info(f"Published {command} to lamp for user {broker.user.username}")
        except Exception as e:
            logger.error(f"Failed to publish lamp command: {e}")
    
    def stop_all_clients(self):
        """Stop all MQTT clients"""
        self.running = False
        for client in self.clients.values():
            client.loop_stop()
            client.disconnect()
        self.clients.clear()
        logger.info("All MQTT clients stopped")



# Global instance
mqtt_service = MQTTService()