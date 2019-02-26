# Leyendo tweets.

A partir de un topic con mensajes de tweeter, construir un dataset con las columnas que queramos

## Preparativos

##### Kafka
```bash
cd ~/Projects/uah-angvd-2019/docker-services/kafka-multi-broker/
docker-compose -p ejercicios down # si es necesario
docker-compose -p ejercicios up broker-1 broker-2 broker-3
```

##### Spark

```bash
cd ~/Projects/uah-angvd-2019/docker-services/spark/
docker-compose -p ejercicios up
```

#####Generador
```bash
# Arrancar el generador de mensajes (en la carpeta de los generadores)
cd ~/Projects/uah-angvd-2019/generators
sbt -Dconfig.file=configs/ejercicio6.conf "runMain com.fhuetas.uah.angdv.gen.runner.BootTweets"
```

### Consideraciones

#### Contexto de spark dentro

Kafka tiene que ser accesible de la misma forma tanto por los workers de spark como por
la maquina desde donde se lanza el Job. Como el entorno virtualizado tiene su propia red es necesario
lanzar la consola desde una de las maquinas dentro de la red.

```bash
docker run -it --rm --name client \
           -v /home/user/Projects/uah-angvd-2019/ejercicios-py/ejercicios/:/ejercicios \
           --net ejercicios_default fhuertas/spark-base:2.4.0-hadoop2.7 bash
```

#### Conector de kafka para spark

El conector de Kafka para Spark es proporcionado por un paquete externo,
por lo tanto es necesario indicarlo al usar los servicio de pyspark o spark-submit

Esto se realiza de la siguiente forma

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 ....
# o
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 ....
```

También es posible hacerlo usando como master `local[*]`

### Ejecución

```bash
# Dentro del contendor creado anteriormente ejecutarlo
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 ejercicio6/solution.py
```
Otros paquetes interesantes 
 * org.apache.spark:spark-avro_2.11:2.4.0