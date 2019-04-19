from pyspark.sql import SparkSession
from pyspark.sql.functions import *

def build_context():
    builder = SparkSession \
        .builder \
        .appName("StructuredNetworkAverage")
    return builder.getOrCreate()

def job_01():
    spark = build_context()

#Cargamos la data del producer

    lines = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:19092,localhost:29092,localhost:39092") \
        .option("subscribe", "tnumeros") \
        .load() \
        .withColumn("current_timestamp", current_timestamp()) #Agregamos un campo de tiempo para las ventanas temporales

    avg_num = lines.selectExpr("current_timestamp","CAST(value AS STRING)")
    avg_num.createOrReplaceTempView("tabla")
    sql_1 = spark.sql("SELECT current_timestamp, CAST(value AS int) from tabla") #Convertimos a entero el campo valor para el cálculo de la media

#Creamos la agregada con las ventanas de tiempos respectivos para el càlculo de la media

    windowedAvgDF = sql_1 \
        .withWatermark("current_timestamp", "3 seconds") \
        .groupBy(window("current_timestamp", "1 second")) \
        .avg("value")

#MOstramos en consola el resultado

    query = windowedAvgDF \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()


if __name__ == "__main__":
    job_01()
