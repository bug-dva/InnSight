from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
from pyspark.sql.functions import udf
from pyspark.sql import DataFrameReader
from pyspark.sql import SQLContext
from pyspark import SparkConf, SparkContext
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

spark = SparkSession.builder.appName("CalculateMetrics").getOrCreate()

city = sys.argv[1]

mode = "overwrite"
url = "jdbc:postgresql://"+config['DEFAULT']['POSTGRESQL_IP']+':'+config['DEFAULT']['POSTGRESQL_PORT']+"/price_insight_db"
properties = {"user": config['DEFAULT']['DB_USER'], "password": config['DEFAULT']['DB_PASSWORD'], "driver": "org.postgresql.Driver"}

df_listing = spark.read.jdbc(url=url, table="listing_" + city, properties=properties)

# calculate the average price by (zipcode,date), for the trend chart
result_average_price_trend = df_listing.groupBy("zipcode", "timestamp").agg({'price':'mean'})

# calculate average price by (zipcode, month)
result_seasonality = df_listing.groupBy("zipcode", "month").agg({'price':'mean'})

# calculate rental type distribution
#result_rental_type_distribution = df_listing.groupBy('zipcode','property_type')['zipcode','property_type'].count()

# calculate room type distribution
#result = df_listing.select(['zipcode','timestamp','price']).describe('price')

result_average_price_trend.show()
result_seasonality.show()

try:
    #result.write.jdbc(url=url, table="trend_by_zipcode_" + city, mode=mode, properties=properties)
    result_average_price_trend.write.jdbc(url=url, table="average_price_trend_" + city, mode=mode, properties=properties)
    result_seasonality.write.jdbc(url=url, table="seasonality_" + city, mode=mode, properties=properties)
except Exception as e:
    print(e)
