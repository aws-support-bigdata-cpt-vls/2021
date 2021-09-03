# Instructions for streaming from file 

# 1.  Download  the files for this lab from the s3 bucket s3://amazon-reviews-pds/parquet/product_category=Books/  to your home directory using the following command:

- Copy Books review data from s3 to emr cluster
```sh
cd /mnt
mkdir book_data
aws s3 cp s3://amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_01.tsv.gz .
gunzip amazon_reviews_us_Books_v1_01.tsv.gz
head amazon_reviews_us_Books_v1_01.tsv
```

- Split the file (into 10 or more chunks) so we work with a small sample of the data first

```sh
split -n10 amazon_reviews_us_Books_v1_01.tsv
ls -lsh
```


expected output:
```
[hadoop@ip-172-13-0-165 book_data]$ split -n10 amazon_reviews_us_Books_v1_01.tsv
[hadoop@ip-172-13-0-165 book_data]$ ls -lsh
total 13G
6.3G -rw-rw-r-- 1 hadoop hadoop 6.3G Nov 24  2017 amazon_reviews_us_Books_v1_01.tsv
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:49 xaa
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:49 xab
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:49 xac
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:49 xad
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:49 xae
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:49 xaf
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:50 xag
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:50 xah
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:50 xai
640M -rw-rw-r-- 1 hadoop hadoop 640M Jun 18 03:50 xaj
```

- Copy one of the splits  to hdfs  (any one of the chunks)

```sh
hdfs dfs -mkdir /user/hadoop/books/
hdfs dfs -put xaa /user/hadoop/books/
hdfs dfs -ls /user/hadoop/books/
```


- Expected output:

```
[hadoop@ip-172-13-0-165 book_data]$ hdfs dfs -ls /user/hadoop/books/
Found 1 items
-rw-r--r--   1 hadoop hdfsadmingroup  670392186 2021-06-18 03:56 /user/hadoop/books/xaa
[hadoop@ip-172-13-0-165 book_data]$ hdfs dfs -ls -h /user/hadoop/books/
Found 1 items
-rw-r--r--   1 hadoop hdfsadmingroup    639.3 M 2021-06-18 03:56 /user/hadoop/books/xaa
[hadoop@ip-172-13-0-165 book_data]$
```


- Inspect input data from pyspark shell

```sh
pyspark
```

expected output:

```sh
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
21/06/18 07:48:26 WARN HiveConf: HiveConf of name hive.server2.thrift.url does not exist
21/06/18 07:48:27 WARN Client: Neither spark.yarn.jars nor spark.yarn.archive is set, falling back to uploading libraries under SPARK_HOME.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /__ / .__/\_,_/_/ /_/\_\   version 2.4.7-amzn-1
      /_/

Using Python version 3.7.9 (default, Feb 18 2021 03:10:35)
SparkSession available as 'spark'.
>>>
```


- Run following commands

```py
df = spark\
   .read\
   .format('csv')\
   .option('inferSchema','True')\
   .option('header', True)\
   .option('delimiter','\t')\
   .load("hdfs:///user/hadoop/books/")

df.printSchema()
df..select("marketplace","customer_id", "product_id","product_category","star_rating","review_date",).show(10,5)
```





# 2. Run pyspark streaming job to stream from file

code:
```py
### StreamFromFile2HDFS.py
### Streaming from csv file

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession\
    .builder\
    .appName("StreamFromFile")\
    .getOrCreate()


schema1= StructType([
StructField('marketplace',StringType(), True),
StructField('customer_id',IntegerType(), True),
StructField('review_id',StringType(), True),
StructField('product_id',StringType(), True),
StructField('product_parent',IntegerType(), True),
StructField('product_title',StringType(), True),
StructField('product_category',StringType(), True),
StructField('star_rating',IntegerType(), True),
StructField('helpful_votes',IntegerType(), True),
StructField('total_votes',IntegerType(), True),
StructField('vine',StringType(), True),
StructField('verified_purchase',StringType(), True),
StructField('review_headline',StringType(), True),
StructField('review_body',StringType(), True),
StructField('review_date',TimestampType(), True)
])


# Create DataFrame representing the stream of input lines from connection to localhost:5560
customer = spark\
   .readStream\
   .format('csv')\
   .schema(schema1)\
   .option('header', True)\
   .option('maxFilesPerTrigger', 1)\
   .load("hdfs:///user/hadoop/books/")



ratings=customer.select("marketplace","customer_id", "product_id","product_category","star_rating","review_date")

# Fileter products with low ratings and
# lowratings=df.filter(df.star_rating < 3)
# lowratings=df.filter(df.star_rating < 3).show(truncate=False)


# Writing to File
# Stream from tsv file and save as csv to hdfs
query=ratings\
   .writeStream \
   .format("csv")\
   .trigger(processingTime="10 seconds")\
   .option("checkpointLocation", "hdfs:///user/hadoop/checkpoint8") \
   .option("path", "/user/hadoop/output") \
   .outputMode("append") \
   .start()


query.awaitTermination()
```

submit command:

```sh
spark-submit StreamFromFile2HDFS.py
```

- Check stream job output file

```sh
[hadoop@ip-172-13-0-165 fromS3]$ hdfs dfs -ls -h /user/hadoop/output
Found 6 items
drwxr-xr-x   - hadoop hdfsadmingroup          0 2021-06-18 05:51 /user/hadoop/output/_spark_metadata
-rw-r--r--   1 hadoop hdfsadmingroup      8.9 M 2021-06-18 05:51 /user/hadoop/output/part-00000-ffe8681c-76ce-4721-b8ce-31e66380b448-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup      9.0 M 2021-06-18 05:51 /user/hadoop/output/part-00001-398fed9f-59ef-46e1-b7ca-cfc0c02c97cc-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup      9.2 M 2021-06-18 05:51 /user/hadoop/output/part-00002-2a295483-e2da-4395-b69d-f63f4edb928a-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup     10.7 M 2021-06-18 05:51 /user/hadoop/output/part-00003-b4e2789a-3274-44a7-b779-5ea8f9a7c8be-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup     10.4 M 2021-06-18 05:51 /user/hadoop/output/part-00004-f5e0dbaf-3c5d-4d0a-a7f5-fc78915c9d60-c000.csv
```




# 3.  Combining multiple smaller files to few larger files 

https://aws.amazon.com/blogs/big-data/seven-tips-for-using-s3distcp-on-amazon-emr-to-move-data-efficiently-between-hdfs-and-amazon-s3/

- combine to multiple small files to few larger files of 128MB. 

- Let’s take a look into the target folders and compare them to the corresponding source folders:
input small files
```sh
[hadoop@ip-172-13-0-165 fromS3]$ hdfs dfs -ls -h /user/hadoop/output
Found 6 items
drwxr-xr-x   - hadoop hdfsadmingroup          0 2021-06-18 05:51 /user/hadoop/output/_spark_metadata
-rw-r--r--   1 hadoop hdfsadmingroup      8.9 M 2021-06-18 05:51 /user/hadoop/output/part-00000-ffe8681c-76ce-4721-b8ce-31e66380b448-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup      9.0 M 2021-06-18 05:51 /user/hadoop/output/part-00001-398fed9f-59ef-46e1-b7ca-cfc0c02c97cc-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup      9.2 M 2021-06-18 05:51 /user/hadoop/output/part-00002-2a295483-e2da-4395-b69d-f63f4edb928a-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup     10.7 M 2021-06-18 05:51 /user/hadoop/output/part-00003-b4e2789a-3274-44a7-b779-5ea8f9a7c8be-c000.csv
-rw-r--r--   1 hadoop hdfsadmingroup     10.4 M 2021-06-18 05:51 /user/hadoop/output/part-00004-f5e0dbaf-3c5d-4d0a-a7f5-fc78915c9d60-c000.csv
```

Pulling your account information to add as bucket

```sh
aws sts get-caller-identity
```

expected output:

```sh
[hadoop@ip-10-10-10-129 bin]$ aws sts get-caller-identity
{
    "Account": "327836271514",
    "UserId": "AROAUYVEQQONG2CRVJXDB:i-0b98b264649761465",
    "Arn": "arn:aws:sts::327836134414553:assumed-role/VLS_EMR_EC2_ROLE/i-0b98b264649761465"
}
```

Creating S3 bucket with account number as name of bucket

```sh
aws s3 mb s3://<account-number>
aws s3 ls
```
expected output:

```sh
[hadoop@ip-10-10-10-129 bin]$ s3 mb s3://327836134414553
[hadoop@ip-10-10-10-129 bin]$ aws s3 ls
2021-09-03 14:23:54 327836134414553
```




s3-dist-cp runs a map reduce job

```sh
s3-dist-cp --src /user/hadoop/output --dest s3://<account-number>/<S3-location> --targetSize=128 --groupBy='.*part.*(\w+)'
aws s3 sync s3://<account-number>/<S3-location> ./
```


expected output after s3-dist-cp map reduce job

```sh
[hadoop@ip-172-13-0-165 fromS3]$ aws s3 sync s3://<account-number>/<S3-location> ./
download: s3://327836134414553/clean-dataset/v to ./v
[hadoop@ip-172-13-0-165 fromS3]$ ls -lsh
total 49M
49M -rw-rw-r-- 1 hadoop hadoop 49M Jun 18 06:29 v
```

- hdfs to hdfs
```sh
 s3-dist-cp --src /user/hadoop/output --dest /user/hadoop/larger --targetSize=128 --groupBy='.*part.*(\w+)'
```


# 4.  Visualize data in HUE


- open HUE UI using master node's DNS address found in your EMR console
 http://master-node-DNS-address:8888/

- Select hive editor


- Create external hive table for s3 location containing data from stream job.

copy DDL below
```sql
use default;
CREATE EXTERNAL TABLE `book_reviews`(
  `marketplace` string, 
  `customer_id` string, 
  `review_id` string, 
  `product_id` string, 
  `product_parent` bigint, 
  `product_title` string, 
  `product_category` string, 
  `star_rating` string, 
  `helpful_votes` string, 
  `total_votes` string, 
  `vine` string, 
  `verified_purchase` string, 
  `review_headline` string, 
  `review_body` string, 
  `review_date` string)
ROW FORMAT DELIMITED  FIELDS TERMINATED BY '\t' 
STORED AS  TEXTFILE
LOCATION 's3://<account-number>/<S3-location>'
TBLPROPERTIES ('areColumnsQuoted'='false', 
  'classification'='csv', 
  'columnsOrdered'='true',
  'delimiter'='\t', 
  'skip.header.line.count'='1');
  
```

- Run the following queries to see the number of each rating type

```sql
SELECT star_rating,count(star_rating) 
FROM book_reviews 
GROUP BY star_rating;
```

```sql
SELECT star_rating,count(star_rating) 
FROM book_reviews 
WHERE star_rating < 4 
GROUP BY star_rating;
```

- use the chart option in HUE to visualize the results using bar chart and pie graph;
 

 


# Bonus: Create pyspark app to stream and view from console

- Stream from file and output to console

```py

### Streaming from csv file to console

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *


spark = SparkSession\
    .builder\
    .appName("StreamFromFile")\
    .getOrCreate()

schema1= StructType([
StructField('marketplace',StringType(), True),
StructField('customer_id',IntegerType(), True),
StructField('review_id',StringType(), True),
StructField('product_id',StringType(), True),
StructField('product_parent',IntegerType(), True),
StructField('product_title',StringType(), True),
StructField('product_category',StringType(), True),
StructField('star_rating',IntegerType(), True),
StructField('helpful_votes',IntegerType(), True),
StructField('total_votes',IntegerType(), True),
StructField('vine',StringType(), True),
StructField('verified_purchase',StringType(), True),
StructField('review_headline',StringType(), True),
StructField('review_body',StringType(), True),
StructField('review_date',TimestampType(), True)])




customer = spark\
   .readStream\
   .format('csv')\
   .schema(schema1)\
   .option('header', True)\
   .option('maxFilesPerTrigger', 1)\
   .load("hdfs:///user/hadoop/books/")


average_rating=customer.groupBy("product_title")\
		.agg((avg("star_rating").alias("average_rating")),
			(count("product_title").alias("count")))\
			.sort(desc("average_rating"))


query=average_rating.writeStream.format("console")\
 		.outputMode("complete").start()

query.awaitTermination()

```
