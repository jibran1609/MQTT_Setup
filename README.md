# Setting Up MQTT Broker and Related Services Using Docker

## In this guide, we'll walk you through the process of setting up an MQTT broker, Redis, MongoDB, and associated Python scripts using Docker containers. We'll assume that you have Docker installed on your system.

Step 1: Download the Required Docker Images
Visit the Google Drive link provided to download the required .tar files:
Google Drive Link  https://drive.google.com/drive/folders/1UEstpjRt5RCzislEiL4wRgLAbnp0v8MX?usp=drive_link

Download the necessary .tar files for Redis, MQTT, and MongoDB.

## Step 2: Load Docker Images
Once you've downloaded the .tar files, load them into Docker as images. Replace <path_to_tar_file> with the actual path to the downloaded .tar files.
Download the MQTT Broker Docker Image:

	docker load -i <path_to_redis.tar>
	docker load -i <path_to_mqtt.tar>
	docker load -i <path_to_mongo.tar>
## step3
 Tag the loaded images with the following names:
 	docker tag <redis_image_id> redis:latest
	docker tag <mqtt_image_id> mqtt:latest
	docker tag <mongo_image_id> mongo:latest

 ### get docker-compose.yml file that describes the services you want to run from github.
Run Docker Compose to start the defined services:

	docker-compose up -d

 
## Step 4: Verify Docker Containers

Check that the Docker containers are running successfully by running:

	sudo docker ps

## Step 5: Run Python Scripts

Ensure that the Python scripts for the MQTT publisher, subscriber, and API code are already available in the running containers. You can either include them when building the Docker images or copy them into the containers during runtime.

If you encounter issues with the scripts or need further details, refer to the GitHub repository provided. Ensure that the scripts are properly configured to connect to the MQTT broker, Redis, and MongoDB containers.

Optionally, write a README.md file in your GitHub repository to provide detailed instructions for running and using the Python scripts.

That's it! You should now have a Dockerized MQTT broker along with Redis and MongoDB, ready to use with your Python scripts. If you encounter any issues, refer to the GitHub repository or consult the Docker documentation for troubleshooting.

## step 6

 This Python script utilizes the requests library to make HTTP GET requests to a FastAPI-based API. It retrieves sensor data, including historical readings and the latest data, by specifying timestamps and sensor IDs. Users can replace placeholders with actual values to fetch and display sensor information.

 import requests

# Define the base URL for your FastAPI application
base_url = "http://localhost:8000"

# Test the /sensor_readings endpoint
start_time = "2023-09-18T11:45:00"  # Replace with a valid start timestamp
end_time = "2023-09-18T11:50:00"   # Replace with a valid end timestamp
sensor_readings_url = f"{base_url}/sensor_readings?start={start_time}&end={end_time}"
response = requests.get(sensor_readings_url)

# Check the HTTP response status code
if response.status_code == 200:
    print("Sensor Readings:")
    print(response.json())
else:
    print(f"Failed to retrieve sensor readings. Status code: {response.status_code}")

# Test the /latest_sensor_readings endpoint
sensor_id = "sensor002"  # Replace with a valid sensor ID
latest_sensor_readings_url = f"{base_url}/latest_sensor_readings?sensor_id={sensor_id}"
response = requests.get(latest_sensor_readings_url)

# Check the HTTP response status code
if response.status_code == 200:
    print("\nLatest Sensor Readings:")
    print(response.json())
else:
    print(f"Failed to retrieve latest sensor readings. Status code: {response.status_code}")
this code saved in request_sensor_data.py 
