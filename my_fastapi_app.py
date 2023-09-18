from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from bson import ObjectId
import json
from datetime import datetime
import redis

app = FastAPI()

# MongoDB Configuration
mongo_host = "localhost"  # Use the same MongoDB host configuration as in your subscriber code
mongo_port = 27017
mongo_username = "root"
mongo_password = "jibran"
mongo_database = "sensor_data"
mongo_collection = "temperature_data"

# Redis Configuration
redis_host = "localhost"
redis_port = 6379

# Initialize the Redis client
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

# Initialize the MongoDB client and collection
mongo_client = MongoClient(mongo_host, mongo_port, username=mongo_username, password=mongo_password)
db = mongo_client[mongo_database]
collection = db[mongo_collection]

@app.get("/sensor_readings")
async def get_sensor_readings(start: str, end: str):
    try:
        # Attempt to convert start and end timestamps to datetime objects
        try:
            start_datetime = datetime.fromisoformat(start)
            end_datetime = datetime.fromisoformat(end)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid timestamp format")

        # Query MongoDB for sensor readings within the specified range
        readings = list(collection.find({
            "timestamp": {
                "$gte": start_datetime.isoformat(),
                "$lte": end_datetime.isoformat()
            }
        }))

        # Convert MongoDB ObjectId to string for serialization
        for reading in readings:
            reading["_id"] = str(reading["_id"])

        return readings

    except Exception as e:
        print(f"Error in /sensor_readings endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/latest_sensor_readings")
async def get_latest_sensor_readings(sensor_id: str):
    try:
        # Retrieve the latest ten readings from Redis
        redis_key = f"latest_readings:{sensor_id}"
        latest_readings = redis_client.lrange(redis_key, 0, 9)

        # Convert JSON strings back to dictionaries
        latest_readings = [json.loads(reading) for reading in latest_readings]

        return latest_readings

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
