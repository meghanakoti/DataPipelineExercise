import pandas as pd, time, json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv('service_logs.csv')
for _, row in df.iterrows():
    topic = row['service']
    message = row.to_dict()
    producer.send(topic, message)
    print(f"Sent to {topic}: {message}")
    time.sleep(2)

