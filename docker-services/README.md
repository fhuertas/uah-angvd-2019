# Servicios dockerizados

## Apache Spark

Este servicio se arranca con los siguientes comandos

```bash
cd spark
docker-compse -p spark down # Solo si es necesario limpiar un servicio anterior
docker-compose -p spark up 
```

En los ficheros `spark/spark_master_env` y `spark/spark_worker_eng` se pueden configurar de 
de manera parte sencilla del servicio para el maestro, en el primer fichero, o del worker, 
en el segundo fichero. 

## Confluent Platform

Este servicio arranca todos o parte los servicios de la plataforma de confluent. Estos son:

* Zookeeper (1 instancia)
* kafka (1 broker)
* Schema registry
* Kafka Connect
* KSQL
* Control center

No es necesario levantar todos los servicios del stack. 

```bash
cd cp-platform
docker-compose -p cp-platform down # si es necesario limpiar una instancia del servicio anterior
docker-compose -p cp-platform up [<id del servicio>] # Si no se indica nada se arrancan todos los servicios  
```

Identificadores de los servicios: 
* zookeeper
* broker
* schema-registry
* connect
* control-center
* ksql-server
* ksql-cli
* ksql-datagen
* rest-proxy

## Apache kafka version varios brokers

Version alternativa de Apache Kafka con multiples brokers y con las imágenes no enterprise