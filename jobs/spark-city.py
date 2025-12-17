# jobs/spark-city.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import (
    StructType, StructField, StringType,
    TimestampType, DoubleType, IntegerType
)

# =========================
# Spark Session
# =========================
spark = (
    SparkSession.builder
    .appName("SmartCityStreaming")
    .config(
        "spark.jars.packages",
        "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,"
        "org.postgresql:postgresql:42.7.3"
    )
    .getOrCreate()
)
spark.conf.set(
    "spark.sql.kafka.bootstrap.servers",
    "broker:9092"
)

spark.sparkContext.setLogLevel("WARN")

# =========================
# PostgreSQL Config
# =========================
POSTGRES_URL = "jdbc:postgresql://postgres:5432/smartcity"
POSTGRES_PROPERTIES = {
    "user": "bigdata",
    "password": "bigdata123",
    "driver": "org.postgresql.Driver"
}

# =========================
# Schemas
# =========================
vehicle_schema = StructType([
    StructField("id", StringType()),
    StructField("device_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("location", StringType()),
    StructField("speed", DoubleType()),
    StructField("direction", StringType()),
    StructField("brand", StringType()),
    StructField("model", StringType()),
])

gps_schema = StructType([
    StructField("id", StringType()),
    StructField("device_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("speed", DoubleType()),
    StructField("direction", StringType()),
    StructField("vehicle_type", StringType()),
])

traffic_schema = StructType([
    StructField("id", StringType()),
    StructField("device_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("location", StringType()),
    StructField("camera_id", StringType()),
    StructField("snapshot", StringType()),
])

weather_schema = StructType([
    StructField("id", StringType()),
    StructField("device_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("location", StringType()),
    StructField("temperature", DoubleType()),
    StructField("weather_condition", StringType()),
    StructField("precipitation", DoubleType()),
    StructField("wind_speed", DoubleType()),
    StructField("humidity", IntegerType()),
    StructField("air_quality_index", DoubleType()),
])

emergency_schema = StructType([
    StructField("id", StringType()),
    StructField("device_id", StringType()),
    StructField("incident_id", StringType()),
    StructField("timestamp", TimestampType()),
    StructField("location", StringType()),
    StructField("type", StringType()),
    StructField("status", StringType()),
    StructField("description", StringType()),
])

# =========================
# Helper Functions
# =========================
def read_kafka_topic(topic, schema):
    return (
        spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "broker:9092")
        .option("bootstrap.servers", "broker:9092")
        .option("subscribe", topic)
        .option("startingOffsets", "latest")
        .load()
        .selectExpr("CAST(value AS STRING)")
        .select(from_json(col("value"), schema).alias("data"))
        .select("data.*")
    )

def write_to_postgres(batch_df, batch_id, table_name):
    (
        batch_df.write
        .jdbc(
            url=POSTGRES_URL,
            table=table_name,
            mode="append",
            properties=POSTGRES_PROPERTIES
        )
    )

# =========================
# Streams
# =========================
vehicle_stream = read_kafka_topic("vehicle_data", vehicle_schema)
gps_stream = read_kafka_topic("gps_data", gps_schema)
traffic_stream = read_kafka_topic("traffic_data", traffic_schema)
weather_stream = read_kafka_topic("weather_data", weather_schema)
emergency_stream = read_kafka_topic("emergency_data", emergency_schema)

# =========================
# Write Streams
# =========================
queries = [
    vehicle_stream.writeStream
        .foreachBatch(lambda df, bid: write_to_postgres(df, bid, "vehicle_data"))
        .outputMode("append")
        .start(),

    gps_stream.writeStream
        .foreachBatch(lambda df, bid: write_to_postgres(df, bid, "gps_data"))
        .outputMode("append")
        .start(),

    traffic_stream.writeStream
        .foreachBatch(lambda df, bid: write_to_postgres(df, bid, "traffic_data"))
        .outputMode("append")
        .start(),

    weather_stream.writeStream
        .foreachBatch(lambda df, bid: write_to_postgres(df, bid, "weather_data"))
        .outputMode("append")
        .start(),

    emergency_stream.writeStream
        .foreachBatch(lambda df, bid: write_to_postgres(df, bid, "emergency_data"))
        .outputMode("append")
        .start(),
]

spark.streams.awaitAnyTermination()

