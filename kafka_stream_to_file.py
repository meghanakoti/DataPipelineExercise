from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, when
from pyspark.sql.types import StructType, StringType, IntegerType

# Start Spark session
spark = SparkSession.builder.appName("KafkaStreamToFile").getOrCreate()

# Define schema for your Kafka messages
schema = StructType() \
    .add("timestamp", StringType()) \
    .add("service", StringType()) \
    .add("latency", IntegerType()) \
    .add("status_code", IntegerType())

# Read from Kafka topics
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "auth-service,billing-service,search-service") \
    .load()

# Parse JSON messages
logs = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("log")) \
    .select("log.*")

# Add a 'color' column: red if latency > 500
tagged = logs.withColumn("color", when(col("latency") > 500, "red").otherwise("green"))

# Write to local files
query = tagged.writeStream \
    .format("csv") \
    .option("path", "output_files") \
    .option("checkpointLocation", "chk_dir") \
    .outputMode("append") \
    .start()

query.awaitTermination()
