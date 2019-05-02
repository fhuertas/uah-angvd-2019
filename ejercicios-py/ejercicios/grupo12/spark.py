import sys

from pyspark.sql import SparkSession
from pyspark.sql.functions import *


def build_context():
    builder = SparkSession \
        .builder \
        .appName("StructuredNetworkNumbersMean")

    if len(sys.argv) > 1:
        builder.master(sys.argv[1])
    return builder.getOrCreate()


def media():
    spark = build_context()

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Split the lines into words

    # Generate running word count
    todos_numeros = lines.withColumn("value", avg("value"))

    query = todos_numeros \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    media()
