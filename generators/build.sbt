import sbt._

ThisBuild / scalaVersion     := "2.12.8"
ThisBuild / organization     := "com.fhuertas.uah.angdv.gen"
ThisBuild / organizationName := "fhuertas"

  lazy val root = project
  .in(file("."))
  .settings(settings)
