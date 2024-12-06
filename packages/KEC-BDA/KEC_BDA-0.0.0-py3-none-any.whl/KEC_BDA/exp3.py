name="BDA-Exp:3"
def run():
    print("""BDA-Exp:3


    !pip install pyspark

    from pyspark.sql import SparkSession
    spark=SparkSession.builder.appName("SimpleDAGexample").getOrCreate()

    df=spark.read.csv("/content/medical_insurance.csv",header="True")
    print(df)

    print(type(df))

    df.show()

    df.select(df['smoker'],df['region']).show()

    print(df.dtypes)

    df1=spark.read.csv("/content/medical_insurance.csv",header=True,inferSchema=True)
    df1

    from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType
    schema = StructType([
        StructField("column1", DoubleType(), True),
        StructField("column2", StringType(), True),
        StructField("column3", DoubleType(), True),
        StructField("column4", DoubleType(), True),
        StructField("column5", StringType(), True),
        StructField("column6", StringType(), True),
        StructField("column7", DoubleType(), True)

    ])

    df = spark.read.csv("/content/medical_insurance.csv", header=True, schema=schema)

    df.show()

    from pyspark.sql.functions import col
    filtered_df = df.filtter(col("column3") <50.0)
    filtered_df.show()

    ordered_df = df.orderBy(col("column6"))
    ordered_df.show()

    dfs=df.groupby("column4").min("column7")
    dfs.show()

    df1 = spark.read.json('/content/sample_data/anscombe.json')
    df1.show()
    print(df1.printSchema())

    df2=spark.read.text("/content/Friends_Transcript.txt")

    df2.show(truncate=False)
""")