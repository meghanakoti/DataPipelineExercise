# Real-Time Data Pipeline: Kafka → Spark → Prometheus → Grafana

## Overview

This project demonstrates a real-time data pipeline that simulates service logs, processes them with Apache Spark, and visualizes system health metrics in Grafana using Prometheus.

It simulates microservices generating logs, flags high-latency events, and provides observability through modern tools.

---

## Features

- Simulates service logs in CSV format
- Sends logs to Kafka topics every 2 seconds
- Spark reads from Kafka and tags records:
  - `red` if latency > 500ms
  - `green` otherwise
- Writes tagged logs to `output_files/`
- Flask exporter exposes real-time metrics:
  - `red_entries`
  - `green_entries`
- Prometheus scrapes metrics
- Grafana visualizes red/green log counts

---

## How to Run

1. **Start Kafka & Zookeeper** (use `kafka-server-start.sh`, `zookeeper-server-start.sh`)
2. **Run the producer**:
   ```bash
   python csv_to_kafka.py

3. **Run the Spark stream processor:
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 kafka_stream_to_file.py
4. Run the Prometheus metrics exporter:
    python metrics_exporter.py

5. Start Prometheus:
   prometheus --config.file=prometheus.yml
6. Start Grafana:
    brew services start grafana
    Visit: http://localhost:3000
7. Add Prometheus in Grafana, then create a dashboard querying:
    red_entries
    green_entries
