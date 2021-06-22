from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split

spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "52.91.147.81") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
#wordCounts = words.groupBy("word").count()

# csv to hdfs
query=words\
    .writeStream \
    .format("csv")\
    .trigger(processingTime="10 seconds")\
    .option("checkpointLocation", "hdfs:///user/hadoop/checkpoint") \
    .option("path", "/user/hadoop/output") \
    .outputMode("append") \
    .start()
 # Start running the query that prints the running counts to the console


## parquet to hdfs
#query=words\
 #   .writeStream \
  #  .format("parquet")\
   # .trigger(processingTime="10 seconds")\
    #.option("checkpointLocation", "hdfs:///user/hadoop/checkpoint2") \
    #.option("path", "/user/hadoop/output6") \
    #.outputMode("append") \
    #.start()
 # Start running the query that prints the running counts to the console


# Parquet to s3
#query=words\
#    .writeStream \
#    .format("parquet")\
#    .trigger(processingTime="10 seconds")\
#    .option("checkpointLocation", "hdfs:///user/hadoop/checkpoint") \
#    .option("path", "s3://emr-tutorials-us-east-1/mystream_app/output") \
#    .outputMode("append") \
#    .start()


#query = wordCounts \
 #   .writeStream \
  #  .outputMode("complete") \
   # .format("console") \
    #.start()

query.awaitTermination()
