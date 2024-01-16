from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
from config import Config
import json
from time import sleep
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, LongType, BooleanType, DoubleType
from pyspark.sql.functions import col, from_json, expr

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')

class Worker:

    def __init__(self):
       self.bootstrap_server = Config.bootstrap_server
       self.topic = Config.topic
       self.spark = SparkSession.builder.master("spark://spark-master:7077").appName("KafkaToSpark").getOrCreate()

    def config_consumer(self):
       consumer = KafkaConsumer(
                                 self.topic,
                                 group_id='nifi_binance_overview_consumer',
                                 bootstrap_servers=self.bootstrap_server,
                                 auto_offset_reset='latest',
                                 )
       return consumer

    def run_tasks(self):
       try:
          consumer = self.config_consumer()
          #logging.info("try")
          for data in consumer:
            #logging.info("tototototO")
            # Décoder les données de bytes à str
            json_data = data.value.decode('utf-8')
            #logging.info(json_data)
            # Convertir JSON en dictionnaire Python
            processor = BinanceDataProcessor()
            parsed_df = processor.process_json_data(json_data, 18800000)
            #parsed_df.printSchema()
            parsed_df.show()
            data = parsed_df.collect()
            #logging.info(data)
            #logging.info('dataframe head - {}'.format(parsed_df))
       except KafkaError as err:
             logging.info("error")
             logging.info(err)
       except Exception as err:
             logging.info("error")
             logging.info(err)

    def run_worker(self):
      #  scheduler = BlockingScheduler()
      #  scheduler.add_job(self.run_tasks, 'cron', minute='*/3')
       self.run_tasks()
      #  logging.info('initializing worker cron task')
      #  scheduler.start()
      #  logging.info('finish worker cron task, wait for the next execution!')

class BinanceDataProcessor:
    def __init__(self):
        self.spark = SparkSession.builder.appName("BinanceDataProcessing").getOrCreate()
        self.spark.sql('set spark.sql.caseSensitive=true')
        
        self.binance_schema = StructType([
            StructField("e", StringType()),
            StructField("E", LongType()),
            StructField("s", StringType()),
            StructField("k", StructType([
                StructField("t", LongType()), 
                StructField("T", LongType()), 
                StructField("s", StringType()), 
                StructField("i", StringType()), 
                StructField("f", LongType()), 
                StructField("L", LongType()), 
                StructField("o", StringType()), 
                StructField("c", StringType()), 
                StructField("h", StringType()), 
                StructField("l", StringType()), 
                StructField("v", StringType()), 
                StructField("n", LongType()), 
                StructField("x", BooleanType()), 
                StructField("q", StringType()), 
                StructField("V", StringType()), 
                StructField("Q", StringType()), 
                StructField("B", StringType())
            ]))
        ])
        
    def process_json_data(self, json_data, circulating_supply):
        df = self.spark.createDataFrame([(json_data,)], ["value"])
        
        parsed_df = (
            df.withColumn("json_data", from_json(col("value"), self.binance_schema))
            .select(
                col("json_data.e").alias("event_type"),
                col("json_data.E").alias("event_time"),
                col("json_data.s").alias("symbol"),
                col("json_data.k.t").alias("start_time"),
                col("json_data.k.T").alias("end_time"),
                col("json_data.k.s").alias("kline_symbol"),
                col("json_data.k.i").alias("interval"),
                col("json_data.k.f").alias("first_trade_id"),
                col("json_data.k.L").alias("last_trade_id"),
                expr("round(json_data.k.o, 3)").alias("open_price"),  # Round open_price to 3 decimal places
                expr("round(json_data.k.c, 3)").alias("close_price"),  # Round close_price to 3 decimal places
                expr("round(json_data.k.h, 3)").alias("high_price"),    # Round high_price to 3 decimal places
                expr("round(json_data.k.l, 3)").alias("low_price"),     # Round low_price to 3 decimal places
                expr("round(json_data.k.v, 3)").alias("volume"),        # Round volume to 3 decimal places
                expr("round(json_data.k.n, 3)").alias("number_of_trades"),  # Round number_of_trades to 3 decimal places
                col("json_data.k.x").alias("is_kline_closed"),
                expr("round(json_data.k.q, 3)").alias("quote_asset_volume"),  # Round quote_asset_volume to 3 decimal places
                expr("round(json_data.k.V, 3)").alias("active_buy_volume"),   # Round active_buy_volume to 3 decimal places
                expr("round(json_data.k.Q, 3)").alias("active_buy_quote_volume"),  # Round active_buy_quote_volume to 3 decimal places
                expr("round(json_data.k.B, 3)").alias("ignore"),  # Round ignore to 3 decimal places
                expr("round((json_data.k.h - json_data.k.l) / 2, 3)").alias("bid_ask_spread"),  # Round bid_ask spread to 3 decimal places
                expr("round(json_data.k.v / (json_data.k.h - json_data.k.l), 3)").alias("liquidity_ratio"),  # Round liquidity ratio to 3 decimal places
                expr("round((close_price - open_price) / close_price, 3)").alias("profit_margin"),  # Round profit_margin to 3 decimal places
                expr("round(((close_price - open_price) / open_price) * 100, 3)").alias("roi"),  # Round roi to 3 decimal places
                expr("round(((high_price - low_price) / open_price) * 100, 3)").alias("price_spread_percentage")  # Round price_spread_percentage to 3 decimal places
            )
            .withColumn("close_price", col("close_price").cast(DoubleType()))  # Convert close_price to DoubleType
            .withColumn("volume", col("volume").cast(DoubleType()))  # Convert volume to DoubleType
            .withColumn("market_cap", expr("round(close_price * {}, 3)".format(circulating_supply)))  # Calculate and round market_cap
            .withColumn("nvtratio", expr("round(volume / {}, 3)".format(circulating_supply)))  # Calculate and round nvtratio
            .withColumn("price_change", expr("round(close_price - open_price, 3)"))  # Calculate and round price_change
            .withColumn("high_low_range", expr("round(high_price - low_price, 3)"))  # Calculate and round high_low_range
            .withColumn("average_price", expr("round((open_price + close_price + high_price + low_price) / 4, 3)"))  # Calculate and round average_price
            .withColumn("price_spread", expr("round(high_price - low_price, 3)"))  # Calculate and round price_spread
            .withColumn("price_range", expr("round(close_price - open_price, 3)"))  # Calculate and round price_range
            .withColumn("trade_liquidity", expr("round(volume / (close_price - open_price), 3)"))  # Calculate and round trade_liquidity
            .drop("json_data")
            .drop("value")
        )
        
        return parsed_df
    
    def stop(self):
        self.spark.stop()

if __name__ == "__main__":
    worker = Worker()
    worker.run_worker()
    
    #processor.stop()
