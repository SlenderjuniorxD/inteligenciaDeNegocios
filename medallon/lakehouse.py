from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, year, month, date_format, quarter

spark = SparkSession.builder \
    .appName("Lakehouse_Contable") \
    .config("spark.jars", "mysql-connector-java-8.0.28.jar") \
    .getOrCreate()

db_url = "jdbc:mysql://serverless-us-east4.sysp0000.db2.skysql.com:4049/dyjdb?useSSL=true&requireSSL=true"
db_props = {"user": "dbpgf00710410", "password": "4wHnZv3Id4rjbe=ZCu0^v", "driver": "com.mysql.cj.jdbc.Driver"}



print("iniciando Lakehouse")

bronce_venta = spark.read.jdbc(db_url, "venta", properties=db_props)
bronce_compra = spark.read.jdbc(db_url, "compra", properties=db_props)

print("Capa Bronze cargada")

#plata
plata_venta = bronce_venta.select(
    col("fechaCliente").alias("fecha"),
    col("idpuntoVenta").alias("id_sucursal"),
    col("tipo").alias("id_tipo_doc"),
    col("nitCliente").alias("nit_tercero"),
    lit("VENTA").alias("operacion"),
    col("totalFact").alias("monto"),
    col("debitoFiscal").alias("impuesto")
).filter(col("fecha").isNotNull())


plata_compra = bronce_compra.select(
    col("fechaProv").alias("fecha"),
    col("idPuntoVenta").alias("id_sucursal"),
    col("tipo").alias("id_tipo_doc"),
    col("nitProv").alias("nit_tercero"),
    lit("COMPRA").alias("operacion"),
    col("totalFact").alias("monto"),
    col("creditoFiscal").alias("impuesto")
).filter(col("fecha").isNotNull())


plata_transacciones = plata_venta.union(plata_compra)

print("plata lista")


oro_dim_tiempo = plata_transacciones.select("fecha").distinct() \
    .withColumn("id_fecha", date_format(col("fecha"), "yyyyMMdd").cast("int")) \
    .withColumn("anio", year(col("fecha"))) \
    .withColumn("mes", month(col("fecha"))) \
    .withColumn("trimestre", quarter(col("fecha")))

oro_hechos = plata_transacciones.withColumn("id_fecha", date_format(col("fecha"), "yyyyMMdd").cast("int"))

print("capa oro")

oro_hechos.show(5)