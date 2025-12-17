# Real-Time Smart City Data Pipeline 🚦

A real-time data pipeline using:

- Apache Kafka (data ingestion)
- Apache Spark Structured Streaming (processing)
- PostgreSQL (storage)
- Streamlit (live dashboard)
- Docker Compose (orchestration)

## Architecture
Producer → Kafka → Spark Streaming → PostgreSQL → Dashboard

## How to Run

```bash
docker compose down
docker volume rm real-time-smart-city-data-pipeline-with-kafka-spark-streaming-and-aws_postgres-data
docker compose up -d
sleep 20
docker exec -it spark-master \
/opt/spark/bin/spark-submit \
--master spark://spark-master:7077 \
--conf spark.jars.ivy=/tmp/.ivy2 \
--packages \
org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.4.1,org.postgresql:postgresql:42.7.3 \
/opt/spark/jobs/spark-city.py

then open:
http://localhost:8501
