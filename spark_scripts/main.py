from pyspark.sql import SparkSession
from pyspark.sql.types import StringType

def main():
    # Créez une session Spark
    spark = SparkSession.builder \
        .appName("KafkaConsumer") \
        .getOrCreate()

    # Lisez les données de Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "host.docker.internal:9092") \
        .option("subscribe", "test") \
        .load()

    # Sélectionnez les valeurs des messages Kafka (vous pouvez ajouter des transformations supplémentaires ici)
    values = df.selectExpr("CAST(value AS STRING)")

    # Affichez les données à l'écran
    query = values.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
