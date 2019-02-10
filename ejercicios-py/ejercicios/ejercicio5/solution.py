from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
import sys


def build_context():
    builder = SparkSession \
        .builder \
        .appName("StructuredNetworkWordCount")

    if len(sys.argv) > 1:
        builder.master(sys.argv[1])
    return builder.getOrCreate()


def main():
    spark = build_context()

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()
    # Query that "replicate" input
    # query2 = lines \
    #     .writeStream \
    #     .outputMode("append") \
    #     .format("console") \
    #     .start()

    # Split the lines into words
    words = lines.select(
        explode(
            split(lines.value, " ")
        ).alias("word")
    )

    # Generate running word count
    word_counts = words.groupBy("word").count()

    query = word_counts \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    main()
