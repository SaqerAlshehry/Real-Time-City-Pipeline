# producer/producer.py

import json
import os
import random
import uuid
import time
from datetime import datetime, timedelta
from kafka import KafkaProducer

# Journey starts from Bangkok
BANGKOK_COORDINATES = {"latitude": 13.7367, "longitude": 100.5232}

# Journey ends in Pattaya
PATTAYA_COORDINATES = {"latitude": 12.9276, "longitude": 100.8771}

LATITUDE_INCREMENT = (
    PATTAYA_COORDINATES["latitude"] - BANGKOK_COORDINATES["latitude"]
) / 100
LONGITUDE_INCREMENT = (
    PATTAYA_COORDINATES["longitude"] - BANGKOK_COORDINATES["longitude"]
) / 100

# Kafka configuration (INSIDE Docker network)
KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS", "broker:29092"
)

VEHICLE_TOPIC = os.getenv("VEHICLE_TOPIC", "vehicle_data")
GPS_TOPIC = os.getenv("GPS_TOPIC", "gps_data")
TRAFFIC_TOPIC = os.getenv("TRAFFIC_TOPIC", "traffic_data")
WEATHER_TOPIC = os.getenv("WEATHER_TOPIC", "weather_data")
EMERGENCY_TOPIC = os.getenv("EMERGENCY_TOPIC", "emergency_data")

random.seed(42)

start_time = datetime.utcnow()
start_location = BANGKOK_COORDINATES.copy()


def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(30, 60))
    return start_time


def simulate_vehicle_movement():
    global start_location

    start_location["latitude"] += LATITUDE_INCREMENT
    start_location["longitude"] += LONGITUDE_INCREMENT

    start_location["latitude"] += random.uniform(-0.0005, 0.0005)
    start_location["longitude"] += random.uniform(-0.0005, 0.0005)

    return start_location


def generate_vehicle_data(device_id):
    location = simulate_vehicle_movement()
    return {
        "id": str(uuid.uuid4()),
        "device_id": device_id,
        "timestamp": get_next_time().isoformat(),
        "location": f"{location['latitude']},{location['longitude']}",
        "speed": random.uniform(10, 80),
        "direction": "Southeast",
        "brand": "HONDA",
        "model": "CR-V",
    }


def generate_gps_data(device_id, timestamp, vehicle_type="private"):
    return {
        "id": str(uuid.uuid4()),
        "device_id": device_id,
        "timestamp": timestamp,
        "speed": random.uniform(10, 80),
        "direction": "Southeast",
        "vehicle_type": vehicle_type,
    }


def generate_traffic_camera_data(device_id, timestamp, location, camera_id):
    return {
        "id": str(uuid.uuid4()),
        "device_id": device_id,
        "timestamp": timestamp,
        "location": location,
        "camera_id": camera_id,
        "snapshot": "Base64EncodedString",
    }


def generate_weather_data(device_id, timestamp, location):
    return {
        "id": str(uuid.uuid4()),
        "device_id": device_id,
        "timestamp": timestamp,
        "location": location,
        "temperature": random.uniform(30, 40),
        "weather_condition": random.choice(["Sunny", "Rainy", "Cloudy"]),
        "precipitation": random.uniform(0, 25),
        "wind_speed": random.uniform(0, 100),
        "humidity": random.randint(0, 100),
        "air_quality_index": random.uniform(0, 500),
    }


def generate_emergency_incident_data(device_id, timestamp, location):
    return {
        "id": str(uuid.uuid4()),
        "device_id": device_id,
        "incident_id": str(uuid.uuid4()),
        "timestamp": timestamp,
        "location": location,
        "type": random.choice(["Accident", "Fire", "Flood", "Earthquake"]),
        "status": random.choice(["Active", "Resolved"]),
        "description": "Description of the incident",
    }


def produce(producer, topic, data):
    producer.send(topic, value=data)
    producer.flush()


def simulate_journey(producer, device_id):
    print("🚀 Smart City Producer started...")

    while True:
        vehicle = generate_vehicle_data(device_id)

        if (
            float(vehicle["location"].split(",")[0])
            <= PATTAYA_COORDINATES["latitude"]
        ):
            print("🏁 Vehicle reached Pattaya. Stopping simulation.")
            break

        produce(producer, VEHICLE_TOPIC, vehicle)
        produce(producer, GPS_TOPIC, generate_gps_data(device_id, vehicle["timestamp"]))
        produce(
            producer,
            TRAFFIC_TOPIC,
            generate_traffic_camera_data(
                device_id, vehicle["timestamp"], vehicle["location"], "CANON"
            ),
        )
        produce(
            producer,
            WEATHER_TOPIC,
            generate_weather_data(
                device_id, vehicle["timestamp"], vehicle["location"]
            ),
        )
        produce(
            producer,
            EMERGENCY_TOPIC,
            generate_emergency_incident_data(
                device_id, vehicle["timestamp"], vehicle["location"]
            ),
        )

        print(f"📤 Sent data for {vehicle['device_id']} at {vehicle['timestamp']}")
        time.sleep(5)


if __name__ == "__main__":
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    try:
        simulate_journey(producer, "Vehicle-007")
    except KeyboardInterrupt:
        print("⛔ Simulation stopped")
