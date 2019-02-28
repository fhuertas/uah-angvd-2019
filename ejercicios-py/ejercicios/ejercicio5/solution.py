from pyspark.sql import SparkSession
from pyspark.sql.functions import *

import sys
import re


def build_context():
    builder = SparkSession \
        .builder \
        .appName("StructuredNetworkWordCount")

    if len(sys.argv) > 1:
        builder.master(sys.argv[1])
    return builder.getOrCreate()


def job1():
    spark = build_context()

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Split the lines into words

    def numbers(string):
        result = re.sub("\\D", "", string)
        return int(0 if result == "" else result)

    remove_chars = udf(numbers)
    words = lines.withColumn("value", remove_chars("value"))

    # Generate running word count
    # word_counts = words.withColumn("value", sum("value"))

    query = words \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    query.awaitTermination()


def job2():
    spark = build_context()

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Split the lines into words

    def only_vocals(string):
        result = re.sub("[^aeiou]*", "", string)
        return "".join(set(result))

    udf_only_vocals = udf(only_vocals)

    words = lines.withColumn("letters-count", length(udf_only_vocals("value")))

    query = words \
        .writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()


def job3():
    # Creando el contexto. Aqui se pueden establecer configuración del Job de Spark
    # o delegarlas a la llamada de spark-submit
    spark = SparkSession \
        .builder \
        .appName("StructuredNetworkWordCount") \
        .getOrCreate()

    # Creando el source de datos. y lo transforma en un dataset en streaming
    # * readStream: indicando que es Streaming
    # * format: Indica que connector se va a usar, entre los posibles valores está
    #           kafka, socket, console. etc...
    # * option/options: Opciones del conector
    # * load. Finaliza la construcción

    lines = spark \
        .readStream \
        .format("socket") \
        .option("host", "localhost") \
        .option("port", 9999) \
        .load()

    # Operaciones de transformacion y manipulación. este caso divide el texto por " "
    # y lo establece como una tabla con la columna word
    words = lines.select(
        explode(
            split(lines.value, " ")
        ).alias("word")
    )

    # Operacion de agregacion por id. une todos los campos en una lista y posteriormente la cuenta
    word_counts = words.groupBy("word").count()

    # Establece el destino del dataset.
    # * writeStream: establece destino en streaming
    # * outputMode: Indica como se van actualizar los campos,
    #     * complete : Copia todos los datos del dataset cada vez
    #     * append: Copia solo los campos nuevos del dataset
    #     * update: Copia solo los datos que se han actualizado en el dataset
    # * format: donde van a copiarse los datos, al igual que el input indica el connector como
    #             kafka.
    # * option/options: Indica opciones especificas del conector
    # * start: operacion que arranca el proceso de streaming.

    query = word_counts \
        .writeStream \
        .outputMode("complete") \
        .format("console") \
        .start()

    # Al ser la operacion asycrona, esta llamada espera a que acabe la query
    # (que puede no ser hasta que falle)
    query.awaitTermination()


if __name__ == "__main__":
    job2()
