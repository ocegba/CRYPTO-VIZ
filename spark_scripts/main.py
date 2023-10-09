from pyspark.sql import SparkSession

def main():
    # Créez une session Spark
    spark = SparkSession.builder \
        .appName("KafkaConsumer") \
        .getOrCreate()

    # Lisez les données de Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "test") \
        .load()

    # Sélectionnez les valeurs des messages Kafka 
    values = df.selectExpr("CAST(value AS STRING)")

    # Écrivez les données dans le terminal
    console_query = values.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    # Écrivez les données dans un fichier
    def write_to_file(batch_df, batch_id):
        batch_df.write.csv(f"path/to/directory/batch_{batch_id}.csv")

    file_query = values.writeStream \
        .foreachBatch(write_to_file) \
        .start()

    console_query.awaitTermination()
    file_query.awaitTermination()

if __name__ == "__main__":
    main()
