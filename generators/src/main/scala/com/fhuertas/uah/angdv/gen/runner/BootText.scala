package com.fhuertas.uah.angdv.gen.runner
import com.fhuertas.uah.angdv.gen.SimpleGens
import com.fhuertas.uah.angdv.gen.kafka.KafkaBuilder
import com.typesafe.config.ConfigFactory
import org.log4s.getLogger
import org.scalacheck.Gen

import scala.concurrent.Await
import scala.concurrent.duration.Duration
import scala.util.Try

object BootText extends App {
  import com.fhuertas.uah.angdv.gen.config.KafkaConfigNs._
  val logger = getLogger
  // namespaces
  val nsBootText = "generator.text"

  // config values
  val config           = ConfigFactory.load().getConfig(nsBootText)
  val kafkaConfig      = config.getConfig(Consumer)
  val runTime          = config.getDuration(TotalTime).toMillis
  val batchTime        = config.getDuration(BatchTime).toMillis
  val mediaWords       = Try(config.getInt(MediaWords)).toOption
  val deviationWords   = Try(config.getInt(DeviationWords)).toOption
  val elementsPerBatch = config.getInt(ElementsPerBatch)
  val topic            = config.getString(TopicName)

  val producer = KafkaBuilder.buildProducer[Nothing, String](kafkaConfig)
  val endMillis = System.currentTimeMillis() + runTime
  val generator = Gen.listOfN(elementsPerBatch, SimpleGens.textGenerator(mediaWords, deviationWords))

  val future = KafkaBuilder.publishGenRec(producer, topic, endMillis, batchTime, generator)
  Await.result(future , Duration.Inf)
}
