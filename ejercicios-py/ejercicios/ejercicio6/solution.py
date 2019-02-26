from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


def job():
    spark = SparkSession \
        .builder \
        .appName("KafkaTweetsReader").getOrCreate()

    schema = StructType([
        StructField("id", StringType(), True),
        StructField("createdAt", StringType(), True)])

    # schema = StructType([StructField("id", StringType(), True),StructField("name", StringType(), True)])

    kafka_input = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "broker:9092") \
        .option("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer") \
        .option("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer") \
        .option("subscribe", "users") \
        .load()

    raw_input = kafka_input.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
        .withColumn("json", from_json('value', schema)) \
        .withColumn("id", col('json.id')) \
        .withColumn("body", col('value'))

    # query = raw_input.writeStream.format("json").option("path", "/tmp/json-dir").start()
    query = raw_input \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    job()

