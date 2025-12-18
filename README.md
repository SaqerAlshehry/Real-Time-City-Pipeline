# 🏙️ Smart City Real-Time Data Pipeline

A complete **real-time data engineering pipeline** that simulates smart city data and processes it using modern streaming technologies.

**Kafka → Spark Structured Streaming → PostgreSQL → Streamlit Dashboard**

---

## 📌 Overview

This project demonstrates how real-time data flows through a distributed system:
- Data is **produced continuously** to Kafka topics
- **Spark Structured Streaming** consumes and processes the data
- Processed data is stored in **PostgreSQL**
- A **Streamlit dashboard** visualizes live analytics

Everything runs locally using **Docker Compose**.

---

## 🧱 Architecture

Kafka Producer

⬇️ 

Kafka Topics 

⬇️

Spark Structured Streaming


⬇️

PostgreSQL

⬇️

Streamlit


⬇️

Dashboard


---

## ⚙️ Prerequisites

### Install Docker Desktop
Download and install Docker Desktop:
- https://www.docker.com/products/docker-desktop

Verify installation:
```bash
docker --version
docker compose version
```

--- 
## ▶️ How to Run the Application
### 1️⃣ Clone the Repo
```bash
git clone https://github.com/SaqerAlshehry/Real-Time-City-Pipeline.git
cd Real-Time-Smart-City-Pipeline
```
### 2️⃣ Stop Containers & remove old data
```bash
docker compose down
docker volume rm real-time-smart-city-data-pipeline-with-kafka-spark-streaming-and-aws_postgres-data
```
### 3️⃣ Start all services
```bash
docker compose up -d
```
### 4️⃣ Wait for services to initialize
```bash
sleep 20
```
### 5️⃣ Start the Spark streaming job
```bash
docker exec -it spark-master \
/opt/spark/bin/spark-submit \
--master spark://spark-master:7077 \
--conf spark.jars.ivy=/tmp/.ivy2 \
--packages \
org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.kafka:kafka-clients:3.4.1,org.postgresql:postgresql:42.7.3 \
/opt/spark/jobs/spark-city.py
```

### 6️⃣ Open the dashboard
```bash
http://localhost:8501
```
You should see live data updating in real time!

#### ☑️ To stop the Application
```bash
docker compose down
```
