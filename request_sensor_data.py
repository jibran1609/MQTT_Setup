import requests

# Define the base URL where your FastAPI server is running
base_url = "http://localhost:8000"  # Replace with the correct URL if different

# Example 1: Retrieve the last 5 sensor readings for a specific sensor
sensor_id = "sensor001"
last_n = 5
response = requests.get(f"{base_url}/sensor-readings/?sensor_id={sensor_id}&last_n={last_n}")

if response.status_code == 200:
    sensor_data = response.json()
    print(f"Last {last_n} Sensor Readings for Sensor ID {sensor_id}:")
    for reading in sensor_data:
        print(reading)
else:
    print(f"Error: {response.status_code}, {response.text}")

# Example 2: Retrieve sensor readings within a date range
start_range = "2023-09-17T00:00:00"
end_range = "2023-09-17T01:15:00"
response = requests.post(f"{base_url}/sensor-readings/range/", json={"sensor_id": sensor_id, "start_timestamp": start_range, "end_timestamp": end_range})

if response.status_code == 200:
    sensor_data = response.json()
    print(f"Sensor Readings within Range ({start_range} to {end_range}):")
    for reading in sensor_data:
        print(reading)
else:
    print(f"Error: {response.status_code}, {response.text}")
