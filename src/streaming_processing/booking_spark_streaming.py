"""
This is a script to ingest real time booking events data via Kafka
into Spark Streaming. The data is saved to an external database PostgreSQL.
"""

## Import libraries and classes

from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from pyspark.sql import Row, SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col
import json, math, datetime
import csv
import io
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import Row, SparkSession
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, col
import json, math, datetime
from kafka.consumer import SimpleConsumer
from operator import add
from kafka import KafkaConsumer
import configparser
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import udf
from pyspark.sql import DataFrameReader
from pyspark.sql import SQLContext
from pyspark import SparkConf, SparkContext
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession

"""
 This gives each incoming RDD access to the SparkSQL and DataFrame API, and will
 allow the session to be restarted in case of driver failure.  It is an
 implementation detail that the user of the class needs to be aware of.
 Essentially, SparkContext gives us access to Spark, and Spark Session gives us
 access to the DataFrame API.
"""

def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

## database config
config = configparser.ConfigParser()
config.read('config.ini')

mode = "append"
url = "jdbc:postgresql://"+config['DEFAULT']['POSTGRESQL_IP']+':'+config['DEFAULT']['POSTGRESQL_PORT']+"/price_insight_db"
properties = {"user": config['DEFAULT']['DB_USER'], "password": config['DEFAULT']['DB_PASSWORD'], "driver": "org.postgresql.Driver"}

## fire up the consumer
topic = 'booking'

def main():
    sc = SparkContext(appName="BookingDataProcessing")
    #sc.setLogLevel("WARN")
    # set microbatch interval as 10 seconds, this can be customized according to the project
    ssc = StreamingContext(sc, 10)
    # directly receive the data under a certain topic
    kafkaStream = KafkaUtils.createDirectStream(ssc, [topic], {"metadata.broker.list":"ec2-52-89-17-35.us-west-2.compute.amazonaws.com:9092,ec2-52-89-17-35.us-west-2.compute.amazonaws.com:9092"})
    # Load JSON data from Kafka
    lines = kafkaStream.map(lambda x: x[1])
    booking_rdd = lines.map(lambda x: x.replace('"','').split(','))
    #['85371', '352', '2019-02-11 07:56:44']
    booking_rdd.pprint()

    # Convert RDDs of the words DStream to DataFrame and run SQL query
    def process(time, rdd):
        print("========= %s =========" % str(time))

        try:
            # Get the singleton instance of SparkSession
            spark = getSparkSessionInstance(rdd.context.getConf())

            # Convert RDD[String] to RDD[Row] to DataFrame
            # ['85371', '352', '2019-02-11 07:56:44']
            rowRdd = rdd.map(lambda w: Row(zipcode=w[0],price=w[1],timestamp=w[2]))
            wordsDataFrame = spark.createDataFrame(rowRdd)
            wordsDataFrame.show()
            wordsDataFrame.write.jdbc(url=url, table='streaming_data', mode=mode, properties=properties)
        except Exception as e:
            print(e)

    booking_rdd.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()

if __name__ == '__main__':
    main()
"""
    # batchdata = kafkaStream.map(lambda x: x[1])
    # #batchdata.pprint()
    # # "17913,622\n,2019-02-08 02:18:18"
    # # "78248,196\n,2019-02-08 02:18:18"
    # batchdata_split = batchdata.map(lambda line: line.replace('"',''))
    # # 17913,622\n,2019-02-08 02:18:18
    # #batchdata_split.pprint()
    # booking_rdd = batchdata_split.map(lambda line: line.split(','))
    # booking_rdd.pprint()
"""
