name="BDA-Exp:8 Apply Windowing Functions and aggregate function using PySpark SQL."
def run():
    print("""BDA-Exp:8 Apply Windowing Functions and aggregate function using PySpark SQL."


!pip install pyspark

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("PySpark_WindowFunction_Example").getOrCreate()

Data=[("Ramu","Erode",30,200),("Sree","Salem",25,100),("kamala","Erode",33,100),
      ("Raju","Theni",35,300),("Mala","Ooty",27,150),("Rani","Ooty",24,700),
      ("Sam","karur",34,400),("Jillu","Ooty",23,500),("Vidhu","Theni",31,900)]

columns=["Name","Native","Age","PocketMoney"]

df = spark.createDataFrame(data = Data, schema = columns)
df.printSchema()
df.show(truncate=False)

from pyspark.sql.window import Window
from pyspark.sql.functions import row_number
windowSpec  = Window.partitionBy("Native").orderBy("PocketMoney")

df.withColumn("row_number",row_number().over(windowSpec)) \
    .show(truncate=False)

from pyspark.sql.functions import rank
df.withColumn("rank",rank().over(windowSpec)) \
    .show()

from pyspark.sql.functions import dense_rank
df.withColumn("dense_rank",dense_rank().over(windowSpec)) \
    .show()

from pyspark.sql.functions import percent_rank
df.withColumn("percent_rank",percent_rank().over(windowSpec)) \
    .show()

from pyspark.sql.functions import ntile
df.withColumn("ntile",ntile(2).over(windowSpec)) \
    .show()

from pyspark.sql.functions import cume_dist
df.withColumn("cume_dist",cume_dist().over(windowSpec)) \
   .show()

from pyspark.sql.functions import lag
df.withColumn("lag",lag("PocketMoney",2).over(windowSpec)) \
      .show()

from pyspark.sql.functions import lead
df.withColumn("lead",lead("PocketMoney",2).over(windowSpec)) \
    .show()

windowSpecAgg  = Window.partitionBy("Native")
from pyspark.sql.functions import col,avg,sum,min,max,row_number
df.withColumn("row",row_number().over(windowSpec)) \
  .withColumn("avg", avg(col("PocketMoney")).over(windowSpecAgg)) \
  .withColumn("sum", sum(col("PocketMoney")).over(windowSpecAgg)) \
  .withColumn("min", min(col("PocketMoney")).over(windowSpecAgg)) \
  .withColumn("max", max(col("PocketMoney")).over(windowSpecAgg)) \
  .where(col("row")==1).select("Native","row","avg","sum","min","max") \
  .show()

df.withColumn("row",row_number().over(windowSpec)) \
  .withColumn("avg", avg(col("PocketMoney")).over(windowSpecAgg)) \
  .withColumn("sum", sum(col("PocketMoney")).over(windowSpecAgg)) \
  .show()

""")