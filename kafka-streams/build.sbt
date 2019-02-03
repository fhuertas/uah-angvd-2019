import sbt._

ThisBuild / scalaVersion     := "2.12.8"
ThisBuild / organization     := "com.fhuertas.kafka.streams"
ThisBuild / organizationName := "fhuertas"
ThisBuild / assemblyJarName in assembly := "kafka-streams.jar"

lazy val root = project
.in(file("."))
.settings(settings)
