name="BDA-Exp:7 Implement Spark SQL Functions to manipulate strings, dates using PySpark SQL."
def run():
    print("""BDA-Exp:7 Implement Spark SQL Functions to manipulate strings, dates using PySpark SQL



!pip install pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("StringFunctionsExample").getOrCreate()

data=[("Ram","Erode","Married",30),("Sree","Salem","Un-Married",25),("kamala","Erode","Married",33),
      ("Raju","Theni","Married",35),("Mala","Ooty","Un-Married",27),("Rani","Tuty","Un-Married",24),
      ("Sam","karur","Married",34),("Jillu","Kovai","Un-Married",23),("Vidhu","Theni","Married",31)]

column=["Name","Native","Marital Status","Age"]

df = spark.createDataFrame(data, column)

df.createOrReplaceTempView("Personal")

df.show()

concatenated_df = spark.sql("SELECT concat_ws(' - ', Name, Native, Age) AS Details FROM Personal")
print("Concatenated Strings:")
concatenated_df.show(truncate=False)

length_df = spark.sql("SELECT Name, length(Native) AS native_length FROM Personal")
print("Length of Types:")
length_df.show()

substring_df = spark.sql("SELECT Native, substring(Native, 1, 3) AS type_abbr FROM Personal")
print("Substring of Types:")
substring_df.show()

uppercase_df = spark.sql("SELECT Name, upper(Name) AS uppercase_name FROM Personal")
print("Uppercase Types:")
uppercase_df.show()

lowercase_df = spark.sql("SELECT `Marital Status`, lower(`Marital Status`) AS lowercase_maritalstatus FROM Personal")
print("Lowercase Types:")
lowercase_df.show()

from pyspark.sql.functions import base64
from pyspark.sql.functions import col
encoded_df = df.withColumn("model_base64", base64(col("Native")))
encoded_df.show()

from pyspark.sql.functions import ascii
ascii_df = df.withColumn("model_ascii", ascii(col("Name")))
ascii_df.show()

from pyspark.sql.functions import instr
position_df = df.withColumn("position", instr(col("Marital Status"), "Married"))
position_df.show()

from pyspark.sql.functions import levenshtein
levenshtein_df = df.withColumn("levenshtein_distance", levenshtein(col("Native"), col("Age")))
levenshtein_df.show()

from pyspark.sql.functions import initcap
capitalized_df = df.withColumn("model_capitalized", initcap(col("Marital Status")))
capitalized_df.show()

from pyspark.sql.functions import regexp_replace
replaced_df = df.withColumn("type_replaced", regexp_replace(col("Marital Status"), "Un-Married", "Single"))
replaced_df.show()

""DATE & TIME""

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Date_Example").getOrCreate()

from pyspark.sql.functions import *
df.select(current_date().alias("current_date")).show()

data=[["1","2020-02-01"],["2","2019-03-01"],["3","2021-03-01"]]
df=spark.createDataFrame(data,["id","input"])
df.show()

df.select(col("input"),date_format(col("input"), "MM-dd-yyyy").alias("date_format")).show()

df.select(col("input"),\
          trunc(col("input"),"Month").alias("Month_Trunc"),\
          trunc(col("input"),"Year").alias("Month_Year"),\
          trunc(col("input"),"Month").alias("Month_Trunc")).show()

from pyspark.sql.functions import col, trunc
from pyspark.sql.types import StringType, StructType, StructField


data = [("2023-07-15",), ("2023-08-20",), ("2023-09-10",)]
schema = StructType([StructField("input", StringType(), True)])


df = spark.createDataFrame(data, schema)

result_df = df.select(
    col("input"),
    trunc(col("input"), "Month").alias("Month_Trunc"),
    trunc(col("input"), "Year").alias("Month_Year"),
    trunc(col("input"), "Month").alias("Month_Trunc_2")
)

result_df.show()

#add_months() , date_add(), date_sub()
df.select(col("input"), \
          add_months(col("input"),3).alias("add_months"), \
          add_months(col("input"),-3).alias("sub_months"), \
          date_add(col("input"),4).alias("date_add"), \
          date_sub(col("input"),4).alias("date_sub")).show()

df.select(col("input"),\
          year(col("input")).alias("year"),\
          month(col("input")).alias("month"), \
          next_day(col("input"),"Sunday").alias("next_day"), \
          weekofyear(col("input")).alias("weekofyear") ).show()

df.select(col("input"),
     dayofweek(col("input")).alias("dayofweek"),
     dayofmonth(col("input")).alias("dayofmonth"),
     dayofyear(col("input")).alias("dayofyear"),
  ).show()

""")