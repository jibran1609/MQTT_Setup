import paho.mqtt.client as mqtt
import json
import pymongo
import redis
from pymongo import MongoClient
from bson import ObjectId  # Import ObjectId from pymongo

# MQTT Broker Details
mqtt_broker_host = "localhost"  # MQTT broker host (can be the service name defined in docker-compose.yml)
mqtt_broker_port = 1883  # Default MQTT port
mqtt_username = "user"
mqtt_password = "jibran"

# MQTT Topics to Subscribe to
mqtt_topic = "sensors/temperature"  # Change to "sensors/humidity" for humidity readings

# MongoDB Configuration
mongo_host = "localhost"  # Use the service name defined in docker-compose.yml
mongo_port = 27017  # Default MongoDB port
mongo_username = "root"  # Your MongoDB username
mongo_password = "jibran"  # Your MongoDB password
mongo_database = "sensor_data"  # The name of the MongoDB database
mongo_collection = "temperature_data"  # The name of the MongoDB collection

# Redis Configuration
redis_host = "localhost"  # Redis host (can be the service name defined in docker-compose.yml)
redis_port = 6379  # Default Redis port

# Initialize the Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(mqtt_topic)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    try:
        # Parse the received JSON message
        payload = json.loads(msg.payload.decode())

        # Connect to MongoDB
        client = MongoClient(mongo_host, mongo_port, username=mongo_username, password=mongo_password)
        db = client[mongo_database]
        collection = db[mongo_collection]

        # Insert the sensor data into MongoDB
        result = collection.insert_one(payload)

        # Convert the MongoDB ObjectId to a string
        if "_id" in payload:
            payload["_id"] = str(payload["_id"])

        # Print the received data and success message
        print("Received Sensor Data:")
        print(json.dumps(payload, indent=4))
        if result.acknowledged:
            print("Data stored successfully in MongoDB")

        # Store the latest ten readings in Redis
        store_latest_reading(payload)

    except Exception as e:
        print(f"Error processing message: {str(e)}")

def store_latest_reading(payload):
    try:
        sensor_id = payload["sensor_id"]
        temperature = payload["value"]

        # Retrieve the current list of latest readings from Redis
        redis_key = f"latest_readings:{sensor_id}"
        latest_readings = redis_client.lrange(redis_key, 0, 9)

        # Add the new reading to the list
        latest_readings.insert(0, json.dumps(payload))

        # Trim the list to keep only the latest ten readings
        latest_readings = latest_readings[:10]

        # Update the Redis key with the latest readings
        redis_client.delete(redis_key)
        for reading in latest_readings:
            redis_client.lpush(redis_key, reading)

    except Exception as e:
        print(f"Error storing reading in Redis: {str(e)}")

# MQTT Client Setup
client = mqtt.Client()
client.username_pw_set(username=mqtt_username, password=mqtt_password)
client.on_connect = on_connect
client.on_message = on_message

# Connect to MQTT Broker
client.connect(mqtt_broker_host, mqtt_broker_port)

try:
    # Start MQTT loop
    client.loop_forever()
except KeyboardInterrupt:
    print("Subscriber stopped.")
    client.disconnect()
