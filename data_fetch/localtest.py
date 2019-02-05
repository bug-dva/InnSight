from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import udf

spark = SparkSession.builder.appName("test").getOrCreate()

file_list = []
fh = open("filelist.txt", "r")
for line in fh.readlines():
    line_url = 's3n://airbnbdataset/allcsvfile/'+str(line.strip())
    file_list.append(line_url)

#file_list = ['0202.csv','0602.csv','united-states_ca_san-francisco_2016-02-02_listings.csv']

# data_schema = [StructField('city',StringType(),False),StructField('zipcode',IntegerType(),False),StructField('price',StringType(),False),StructField('last_scraped',TimestampType(),False)]
# schema = StructType(fields = data_schema)

mode = "append"
url = "jdbc:postgresql://54.189.135.213:5432/price_insight_db"
properties = {"user": "spark_user","password": "20192019","driver": "org.postgresql.Driver"}

get_price_udf = udf(lambda x:float(x.replace('$','').replace(',','')),FloatType())
#df3 = df2.withColumn('newprice', get_price_udf(df2['price']))
#df4 = df3.select(['city','zipcode','newprice'])

for file in file_list:
    raw_df = spark.read.csv(file,header=True,inferSchema=True,multiLine=True,escape='"')
    df_subset = raw_df.select(['city','zipcode','price','last_scraped'])
    df_subset_dropna = df_subset.na.drop()
    df_filtered = df_subset_dropna.filter(df_subset_dropna['zipcode'].isNotNull())
    df_filtered = df_subset_dropna.filter(df_subset_dropna['price'].isNotNull())
    df_zipcode_changed = df_filtered.withColumn('zipcode', df_filtered['zipcode'].cast(IntegerType()))
    df_final = df_zipcode_changed.withColumn('price', get_price_udf(df_zipcode_changed['price']))
    df_final.show()
    try:
        df_final.write.jdbc(url=url, table="listing", mode=mode, properties=properties)
    except Exception as e:
        print(e)
