import paho.mqtt.client as mqtt
import json
import random
import time

# MQTT Broker Details
mqtt_broker_host = "localhost"  # Change this to your MQTT broker's hostname or IP address
mqtt_broker_port = 1883  # Default MQTT port
mqtt_username = "user"
mqtt_password = "jibran"

# MQTT Callbacks
def on_publish(client, userdata, mid):
    print(f"Message published (Mid: {mid})")

# MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=mqtt_password)
client.on_publish = on_publish

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port)

# List of sensor IDs
sensor_ids = ["sensor001", "sensor002", "sensor003", "sensor004", "sensor005","sensor006", "sensor007", "sensor008", "sensor009", "sensor010"]

try:
    while True:
        for sensor_id in sensor_ids:
            # Generate a random sensor reading
            temperature = round(random.uniform(0, 100), 2)  # Replace with appropriate value for your sensor

            # Create a JSON payload
            payload = {
                "sensor_id": sensor_id,
                "value": temperature,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }

            # Construct the topic for the sensor (e.g., sensors/temperature)
            topic = f"sensors/temperature"  # Change to "sensors/humidity" for humidity readings

            # Publish the payload to the MQTT topic
            client.publish(topic, json.dumps(payload))
            print(f"Published: {json.dumps(payload)} to {topic}")

            # Sleep for a time interval (adjust as needed)
            time.sleep(10)  # Adjust the interval as needed

except KeyboardInterrupt:
    print("Publisher stopped.")
    client.disconnect()

