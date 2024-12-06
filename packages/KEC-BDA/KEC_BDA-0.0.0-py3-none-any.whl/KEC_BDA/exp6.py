name="BDA-Exp:6 Perform DDL and DML operations in PySpark SQL."
def run():
    print(""" BDA-Exp:6 Perform DDL and DML operations in PySpark SQL.


!pip install pyspark

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[1]").appName("SparkByExamples.com").getOrCreate()

""DDL""

data = [("Pooja","KEC",21),("Sree","PSG",20),("Oviya","SKCET",22),("Tanvi","KEC",19),("Uma","NEC",23),("Roshini","PSG",23),("Ram","NEC",20),("Sita","KEC",22),("Nandi","PSG",24),("Vidhu","KEC",18)]
columns = ["Name","College","Age"]
df = spark.createDataFrame(data, columns)

df.write.saveAsTable("Table", format="parquet", mode="overwrite")

spark.sql("DESCRIBE Table").show()

spark.sql("SHOW COLUMNS FROM Table").show()

from pyspark.sql import functions as F
df.withColumn("new_column", F.lit("some_value")).write.saveAsTable("new_column_2")

spark.sql("DESCRIBE new_column_2").show()

spark.catalog.dropTempView("new_table_name_1")
spark.sql("DROP TABLE IF EXISTS new_table_name_1")

new_data = [("David","KEC", 30,"Erode"),("Bob","NEC", 45,"Coimbatore")]
columns = ["name", "age","new_column"]
new_df = spark.createDataFrame(new_data, columns)
new_df.write.insertInto("new_column_2")
new_df.show()

person_name = "Sree"
new_age = 56
updated_df = df.withColumn("age", F.when(F.col("name") == person_name, new_age).otherwise(F.col("Age")))

updated_df.show()
df.show()

updated_df = updated_df.filter(F.col("name") != "Sree")
updated_df.show()

""DML""

new_data = [("David", "KEC", 30, "Erode"), ("Bob", "NEC", 45, "Coimbatore")]
columns = ["Name", "College", "Age", "new_column"] 
new_df = spark.createDataFrame(new_data, columns)

new_df.write.saveAsTable("new_column_2", mode="append")

spark.sql("SELECT * FROM new_column_2").show()

person_name = "Sree"
new_age = 56
updated_df = df.withColumn("Age", F.when(F.col("Name") == person_name, new_age).otherwise(F.col("Age")))

updated_df.show()


filtered_df = updated_df.filter(F.col("Name") != person_name)


filtered_df.show()

""")