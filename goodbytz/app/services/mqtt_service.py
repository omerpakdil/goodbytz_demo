import json
import logging
from typing import Any, Dict, Optional

import paho.mqtt.client as mqtt

from app.core.config import settings

logger = logging.getLogger(__name__)


class MQTTService:
    def __init__(self):
        self.client = mqtt.Client(client_id=settings.MQTT_CLIENT_ID)
        if settings.MQTT_USERNAME and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USERNAME, settings.MQTT_PASSWORD)
        
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
        self.connected = False
        self.topics = {
            "orders": "goodbytz/orders/#",
            "kitchen": "goodbytz/kitchen/#",
        }
    
    def connect(self) -> None:
        """Connects to the MQTT broker."""
        try:
            self.client.connect(settings.MQTT_BROKER_HOST, settings.MQTT_BROKER_PORT, 60)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"MQTT connection error: {e}")
    
    def disconnect(self) -> None:
        """Closes the MQTT broker connection."""
        self.client.loop_stop()
        self.client.disconnect()
    
    def on_connect(self, client: mqtt.Client, userdata: Any, flags: Dict, rc: int) -> None:
        """Called when connection is established."""
        if rc == 0:
            logger.info("Connected to MQTT broker")
            self.connected = True
            
            # Subscribe to topics
            for topic in self.topics.values():
                client.subscribe(topic)
                logger.info(f"Subscribed to: {topic}")
        else:
            logger.error(f"MQTT connection error, code: {rc}")
            self.connected = False
    
    def on_disconnect(self, client: mqtt.Client, userdata: Any, rc: int) -> None:
        """Called when connection is lost."""
        logger.info("MQTT broker connection lost")
        self.connected = False
    
    def on_message(self, client: mqtt.Client, userdata: Any, msg: mqtt.MQTTMessage) -> None:
        """Called when a message is received."""
        try:
            payload = json.loads(msg.payload.decode())
            logger.info(f"MQTT message received: {msg.topic} - {payload}")
            
            # You can process the message here
            if msg.topic.startswith("goodbytz/orders/"):
                self.handle_order_message(msg.topic, payload)
            elif msg.topic.startswith("goodbytz/kitchen/"):
                self.handle_kitchen_message(msg.topic, payload)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON format: {msg.payload}")
        except Exception as e:
            logger.error(f"Message processing error: {e}")
    
    def handle_order_message(self, topic: str, payload: Dict[str, Any]) -> None:
        """Processes order-related messages."""
        # Order message processing logic will be here
        pass
    
    def handle_kitchen_message(self, topic: str, payload: Dict[str, Any]) -> None:
        """Processes kitchen-related messages."""
        # Kitchen message processing logic will be here
        pass
    
    def publish_order_status(self, order_id: int, status: str) -> None:
        """Publishes order status changes."""
        if not self.connected:
            logger.warning("No MQTT connection, cannot publish message")
            return
        
        topic = f"goodbytz/orders/{order_id}/status"
        payload = json.dumps({"order_id": order_id, "status": status})
        
        self.client.publish(topic, payload, qos=1)
        logger.info(f"Order status published: {order_id} - {status}")
    
    def publish_kitchen_notification(self, notification_type: str, data: Dict[str, Any]) -> None:
        """Publishes kitchen notifications."""
        if not self.connected:
            logger.warning("No MQTT connection, cannot publish notification")
            return
        
        topic = f"goodbytz/kitchen/{notification_type}"
        payload = json.dumps(data)
        
        self.client.publish(topic, payload, qos=1)
        logger.info(f"Kitchen notification published: {notification_type}")


# Singleton instance
mqtt_service = MQTTService()