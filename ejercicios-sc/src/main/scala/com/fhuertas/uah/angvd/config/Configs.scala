package com.fhuertas.uah.angvd.config

object Configs {
  lazy val Ej3 = new {
    val root        = "ejercicio3"
    val kafka       = s"$root.kafka"
    val input  = s"$root.topics.input"
    val output = s"$root.topics.output"
  }
}
