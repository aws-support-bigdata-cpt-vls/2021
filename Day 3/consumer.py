from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
spark = SparkSession \
    .builder \
    .appName("ProductCounter") \
    .getOrCreate()
# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "10.10.20.158") \
    .option("port", 8000) \
    .load()
# Extract product information from streams
products = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("product")
)
# count products bought by customers
productCount = products.groupBy("product").count()
query = productCount \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
   .start()
query.awaitTermination()