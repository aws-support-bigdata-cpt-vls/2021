from pyspark.sql.functions import rand, randn
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext, SQLContext
sc = SparkContext.getOrCreate()
sqlContext = SQLContext(sc)

#Create SparkSession
spark = SparkSession.builder.master("yarn").appName("SparkByExamples.com").getOrCreate()

df = sqlContext.range(0, 10000000)
df.count()

df2 = df.select("id", rand(seed=1000).alias("uniform"), randn(seed=555).alias("normal"))
row1 = df2.agg({"id": "max"}).collect()[0]
print(row1["max(id)"])

df2.createOrReplaceTempView("df2")
df_part1 = spark.sql("select * from df2 where id between 1 and 999999 order by id desc")
row2 = df_part1.agg({"id": "max"}).collect()[0]
print(row2["max(id)"])

df_part1.write.format("csv").mode("overwrite").save("/home/hadoop/data/output1/")
df_part2 = spark.sql("select * from df2 where id > 10000000 order by id desc")
row2 = df_part2.agg({"id": "max"}).collect()[0]
print(row2["max(id)"])
df_part2.write.format("csv").mode("overwrite").save("/home/hadoop/data/output2/")