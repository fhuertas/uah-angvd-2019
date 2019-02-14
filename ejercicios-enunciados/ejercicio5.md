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

Nota: Este código es compatible con la consola py-spark

```python
# Importando las librerías
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

# Creando el contexto. Aqui se pueden establecer configuración del Job de Spark
# o delegarlas a la llamada de spark-submit
spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount")
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

```

## Ejercicio 5

A partir de una fuente de socket, desarrollar jobs que realizen las siguientes acciones: 
* A partir de la entrada, devolver la cantidad de latreas distintas que tiene cada entrada.
* A partir de la entrada, eliminar las letras (solo digitos) y sumar todos los números que resulten, y sumar los 
números al estado acumulado. (1a1, 2b, 33) -> (11, 2, 33) -> 47. (2w2) -> (22) -> 69
