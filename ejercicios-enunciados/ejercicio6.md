# Leyendo tweets.

A partir de un topic con mensajes de tweeter, construir un dataset con las columnas que queramos

## Preparativos

##### Kafka
```bash
cd cd docker-services/kafka-multi-broker/
docker-compose -p cp-platform down # si es necesario
docker-compose -p cp-platform up broker-1 broker-2 broker-3
```

#####Generador
```bash
# Arrancar el generador de mensajes (en la carpeta de los generadores)
sbt -Dconfig.file=configs/ejercicio6.conf "runMain com.fhutas.uah.angdv.gen.runner.BootTweets"
```

### Consideraciones


#### Conector de kafka para spark

El conector de kafka para spark structured streaming es proporcionado por un paquete externo,
por lo tanto es necesario indicarlo al usar los servicio de pyspark o spark-submit 

Esto se realiza de la siguiente forma

```bash
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 ....
# o 
pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 ....
```

#### Spark desde local

Kafka tiene que ser accesible de la misma forma tanto por los agentes de spark como por 
la maquina desde donse se lanza el job. Como el entorno virtualizado tiene su propia red es necesario
lanzar la consola desde una de las maquinas dentro de la red. 

```bash
# copiar los archivos python.
docker cp ejercicios-py/ejercicios/ spark-master:/
# Entrar en la maquina virtual 
docker exec -it spark-master bash
spark-submit --master --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0 /ejercicios/ejercicio6/runner.py
```

```bash
docker run -v /home/user/Project/uah-2019/ejercicios-py/ejercicios:/ejercicios \
           -it --rm --name client \
           --net spark_default fhuertas/spark-base:2.4.0-hadoop2.7 -- bash
# En otra consola
docker network connect cp-platform_default client
``` 

También es posible hacerlo usando como master `local[*]`
