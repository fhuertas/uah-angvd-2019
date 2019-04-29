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

    def numbers(string):
        try:
            val = float(string)
            return val
        except ValueError:
            print("No es entero")

    remove_chars = udf(numbers)
    words = lines.withColumn("value", remove_chars("value"))

    # Generate running word count
    todos_numeros = words.withColumn("value", mean("value"))

    query = todos_numeros \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    media()
