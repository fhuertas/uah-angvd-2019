# Spark Structured Streaming con python

## Preparar el entornos

Levantar el servicio

```
# desde la carpeta del servicio de spark.
docker-compose down; docker-compose up
```

## Como ejecutarlo

Una aplicación de Spark Structured Streaming se puede ejecutar de varias formas
* Desde la consola de pyspark. Util para exploraciones de forma rapida

```
pyspark --py-files path/to/python/zip/ogg/or/py
```

* Con el comando spark-submit. De esta forma se puede establecer cada parametro
la llamada lo que es muy util para aplicaciones en produción o pre-produción


```
spark-submit --py-files path/to/python/zip/ogg/or/py --master spark://spark.host:7077 py-file.py
```

* Con python (Incluido desde los entornos de desarrollo). Útil para el desarrollo
de las aplcaciones. Es necesario indicar los parametros al crear el contexto en
la aplicación. y tener importado el modulo de pyspark

## Contar palabras.

Levantar un socket para las pruebas
```
nc -lk 9999
```

Ejecutar el ejemplo. Desde el path de los ejercicios de python

### Modo consola

```
make clean env package
pyspark --py-files dist/ejercicios_python-1.0.0.zip --master spark://localhost:7077
# dentro de la consola de pyspark
from ejercicios.ejercicio5 import solution
solution.main()
```

### Spark submit

```
make clean env package
spark-submit --master spark://localhost:7077 --py-files dist/ejercicios_python-1.0.0.zip \
    ejercicios/ejercicio5/solution.py
```

### Desde el ejecutable de python

En este entorno se puede porque la dependencia de pyspark se encuentra incluida

```
make clean env
source env/bin/activate
# Con el módulo
python -m ejercicios.ejercicio5.solution spark://localhost:7077
# o con el fichero
python python ejercicios/ejercicio5/solution.py spark://localhost:7077
```

### Código del ejemplo

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount")
    .getOrCreate()

lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

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

```
