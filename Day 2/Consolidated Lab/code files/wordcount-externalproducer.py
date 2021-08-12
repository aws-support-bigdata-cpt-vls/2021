from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import *

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to 52.91.147.81:9999 include timestamp column
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "52.91.147.81") \
    .option("port", 9999) \
    .option("includeTimestamp", "true") \
    .load()


# csv to hdfs
query=lines\
    .writeStream \
    .format("csv")\
    .trigger(processingTime="10 seconds")\
    .option("checkpointLocation", "hdfs:///user/hadoop/checkpoint1") \
    .option("path", "/user/hadoop/output1") \
    .outputMode("append") \
    .start()

query.awaitTermination()
