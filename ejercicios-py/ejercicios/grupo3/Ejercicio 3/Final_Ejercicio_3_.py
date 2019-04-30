from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys


def build_context():
    builder = SparkSession.builder.appName("StructuredNetworkWordCount")

    if len(sys.argv) > 1:
        builder.master(sys.argv[1])
    return builder.getOrCreate()


def job():

    sc = SparkContext(appName="Sparkstreaming")
    sc.setLogLevel("WARN")

    spark = build_context()

    kafka_input = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "numbers") \
        .load()

    def numbers_transformation(string):
        return int(0 if string == "" else string)

    num_value = udf(numbers_transformation)

    df = kafka_input.withColumn("num", num_value("value"))
    print(df)

    numbers = df.selectExpr("CAST(timestamp AS timestamp)", "CAST(num AS bigint)")

    avg_numbers = numbers.select(avg("num"))

    query = avg_numbers \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    job()
