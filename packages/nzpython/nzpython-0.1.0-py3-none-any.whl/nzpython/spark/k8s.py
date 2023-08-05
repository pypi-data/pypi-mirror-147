import os
from pyspark.conf import SparkConf


def getSparkSimpleConf(
    master="k8s://https://kubernetes.default.svc.cluster.local:443",
    memory="1024m",
    instances="2",
    image="ingkle/pyspark",
    namespace=os.environ.get("POD_NAMESPACE", ""),
):
    so = SparkConf()
    so.setMaster(master)
    so.set("spark.executor.memory", memory)
    so.set("spark.executor.instances", instances)
    so.set("spark.kubernetes.container.image", image)
    so.set("spark.kubernetes.namespace", namespace)
    return so


def getSparkDeltaConf(
    master="k8s://https://kubernetes.default.svc.cluster.local:443",
    memory="1024m",
    instances="2",
    image="ingkle/pyspark",
    s3endpoint="http://minio.minio.svc.cluster.local",
    s3accesskey="",
    s3secretkey="",
    namespace=os.environ.get("POD_NAMESPACE", ""),
):
    so = SparkConf()
    so.setMaster(master)
    so.set("spark.executor.memory", memory)
    so.set("spark.executor.instances", instances)
    so.set("spark.kubernetes.container.image", image)
    so.set("spark.kubernetes.namespace", namespace)
    so.set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    so.set(
        "spark.sql.catalog.spark_catalog",
        "org.apache.spark.sql.delta.catalog.DeltaCatalog",
    )
    so.set("spark.hadoop.fs.s3a.endpoint", s3endpoint)
    so.set("spark.hadoop.fs.s3a.access.key", s3accesskey)
    so.set("spark.hadoop.fs.s3a.secret.key", s3secretkey)
    so.set("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    so.set("spark.hadoop.fs.s3a.path.style.access", "true")
    so.set("spark.hadoop.fs.s3a.connection.ssl.enabled", "true")
    return so
