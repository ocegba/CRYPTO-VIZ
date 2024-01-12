from apscheduler.schedulers.blocking import BlockingScheduler
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import logging
from config import Config
import json
from time import sleep
from pyspark.sql import SparkSession


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
          logging.info("try")
          for data in consumer:
            logging.info("tototototo")
            logging.info("json: ", json.loads(data.value))
            # Traiter les données avec Spark
            df = self.spark.createDataFrame([data.value])
            logging.info("df: ", df.show())
       except KafkaError as err:
             logging.info("error")
             logging.info(err)
       except Exception as err:
             logging.info("error")
             logging.info(err)

    def run_worker(self):
       scheduler = BlockingScheduler()
       scheduler.add_job(self.run_tasks, 'cron', minute='*/3')
       logging.info('initializing worker cron task')
       scheduler.start()
       logging.info('finish worker cron task, wait for the next execution!')

if __name__ == '__main__':
   worker = Worker()
   worker.run_worker()