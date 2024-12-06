name="BDA-Exp:4"
def run():
    print("""BDA-Exp:4



pip install pyspark

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

emptyRDD = spark.sparkContext.emptyRDD()
print(emptyRDD)

rdd2 = spark.sparkContext.parallelize([])
print(rdd2)

from pyspark.sql.types import StructType, StructField, StringType

schema = StructType([
    StructField('firstname', StringType(), True),
    StructField('middlename', StringType(), True),
    StructField('lastname', StringType(), True)
])

print(schema)

df = spark.createDataFrame(emptyRDD,schema)
df.printSchema()

df1 = emptyRDD.toDF(schema)
df1.printSchema()

df2 = spark.createDataFrame([], schema)
df2.printSchema()

df3 = spark.createDataFrame([], StructType([]))
df3.printSchema()

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
dept = [("Finance",10),("Marketing",20),("Sales",30),("IT",40)]
print(type(dept))
rdd = spark.sparkContext.parallelize(dept)
print(type(rdd))
print(rdd)

df = rdd.toDF()
df.printSchema()
df.show(truncate=False)

deptColumns = ["dept_name","dept_id"]
df2 = rdd.toDF(deptColumns)
df2.printSchema()
df2.show()

deptDF = spark.createDataFrame(rdd, schema = deptColumns)
deptDF.printSchema()
deptDF.show()

from pyspark.sql.types import StructType,StructField, StringType
deptSchema = StructType([
StructField('dept_name', StringType(), True),
StructField('dept_id', StringType(), True)
])
deptDF1 = spark.createDataFrame(rdd, schema = deptSchema)
deptDF1.printSchema()

deptDF1.show()

import pyspark
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
dept = [("Finance",10),("Marketing",20),("Sales",30),("IT",40)]
rdd = spark.sparkContext.parallelize(dept)
df = rdd.toDF()
df.printSchema()
df.show()

deptColumns = ["dept_name","dept_id"]
df2 = rdd.toDF(deptColumns)
df2.printSchema()
df2.show()

deptDF = spark.createDataFrame(rdd, schema = deptColumns)
deptDF.printSchema()
deptDF.show()

from pyspark.sql.types import StructType,StructField, StringType
deptSchema = StructType([
StructField('dept_name', StringType(), True),
StructField('dept_id', StringType(), True)
])
deptDF1 = spark.createDataFrame(rdd, schema = deptSchema)
deptDF1.printSchema()
deptDF1.show()

import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
data = [("James","","Smith","36636","M",60000),
        ("Michael","Rose","","40288","M",70000),
        ("Robert","","Williams","42114","","400000"),
        ("Maria","Anne","Jones","39192","F",500000),
        ("Jen","Mary","Brown","","F",0)]
columns = ["first_name","middle_name","last_name","dob","gender","salary"]
pysparkDF = spark.createDataFrame(data = data, schema = columns)
pysparkDF.printSchema()
pysparkDF.show(truncate=False)
pandasDF = pysparkDF.toPandas()
print(pandasDF)

from pyspark.sql.types import StructType, StructField, StringType, IntegerType

dataStruct = [
    (("James", "", "Smith"), "36636", "M", "3000"),
    (("Michael", "Rose", ""), "40288", "M", "4000"),
    (("Robert", "", "Williams"), "42114", "M", "4000"),
    (("Maria", "Anne", "Jones"), "39192", "F", "4000"),
    (("Jen", "Mary", "Brown"), "", "F", "-1")
]

schemaStruct = StructType([
    StructField('name', StructType([
        StructField('firstname', StringType(), True),
        StructField('middlename', StringType(), True),
        StructField('lastname', StringType(), True)
    ])),
    StructField('dob', StringType(), True),
    StructField('gender', StringType(), True),
    StructField('salary', StringType(), True)
])

df = spark.createDataFrame(data=dataStruct, schema=schemaStruct)

df.printSchema()

pandasDF2 = df.toPandas()

print(pandasDF2)

""")