# ejercicios

## Development

```bash
# run a especific class
$ sbt 'runMain com.fhuertas.uah.angvf.ejercicio2.Runner'

```

The configuration could be override with including a runtime parameter
 * **-Dconfig.file=\<path\>**: Take other configuration file. 
 * **-Dfoo.bar=\<value\>**: Override a simple configuration value. 
 
Example
```bash
sbt -Dconfig.file=/tmp/other.conf -Dejercicio3.topic.input=unTopic 'runMain com.fhuertas.uah.angvf.ejercicio3.Runner'
```

## Exercise 3

Default configuration:

* **configuration file**: src/main/resources/reference.conf
* **Bootstrap servers**: localhost:9092
* **Input topic**: ej3-input
* **Output topic**: ej3-output

How to run: 
```bash
sbt 'runMain com.fhuertas.uah.angvf.ejercicio3.Runner'
```