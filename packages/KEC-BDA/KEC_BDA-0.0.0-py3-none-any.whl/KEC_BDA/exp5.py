name="BDA-Exp:5 Find the minimum temperature in a city using PySpark "
def run():
    print("""BDA-Exp:5 Find the minimum temperature in a city using PySpark 



!pip install pyspark

from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Temperature").getOrCreate()
sc = spark.sparkContext
lines = sc.textFile("/content/Weather dataset - weather.csv")
print(lines)

header = lines.first()
print(header)

lines = lines.filter(lambda line: line != header)
print(lines.collect())


city_temperature = lines.map(lambda x: x.split(','))
print(city_temperature.collect())

city_temp = city_temperature.map(lambda x: (x[0], x[1]))
print(city_temp.collect())

print(type(city_temp))

city_max_temp = city_temperature.map(lambda x: x[1]).max()
print("City with Max Temperature:", city_max_temp)

city_min_temp = city_temperature.map(lambda x: x[1]).min()
print("City with Min Temperature:",city_min_temp)

""Method 2""

from pyspark.sql import SparkSession
from pyspark.sql.functions import max, col

spark = SparkSession.builder.appName("MaxTemperature").getOrCreate()
weather_df = spark.read.csv("/content/city_temperature.csv", header=True, inferSchema=True)

max_temp_value = weather_df.select(max("AvgTemperature").alias("MaxTemperature")).collect()[0]["MaxTemperature"]
max_temp_row = weather_df.filter(col("AvgTemperature") == max_temp_value)
max_temp_row.show()

max_temp_cities = max_temp_row.select("City"")
max_temp_cities.show()

""Method 3""
Processing from different files
""

from pyspark.sql.functions import min, split
import pandas as pd
spark = SparkSession.builder \
    .appName("CompareTemperature") \
    .getOrCreate()

csv_df = spark.read.csv("/content/min_temperature(csv).csv", header=True, inferSchema=True).select("City", "Temperature")
print("CSV file")
csv_df.show()

text_df = spark.read.text("/content/min_temperature(txt).txt")
header = text_df.first()[0]
data_df = text_df.filter(text_df["value"] != header)

text_df1 = data_df.select(
    split(col("value"), ",")[0].alias("City"),
    split(col("value"), ",")[1].alias("Temperature")
)
print("Text file")
text_df1.show()

json_df = spark.read.json("/content/min_temperature(json).json")
json_clean_df = json_df.select("City", "Temperature").filter(col("City").isNotNull())
print("JSON file")
json_clean_df.show()

tsv_df = spark.read.csv("/content/min_temperature(tsv).tsv", sep="\t", header=True, inferSchema=True).select("City", "Temperature")
print("TSV file")
tsv_df.show()

pandas_df = pd.read_excel("/content/min_temperature(Xlsx).xlsx")

xlsx_df = spark.createDataFrame(pandas_df)
print("XLS file")
xlsx_df.show()

list_data = [
    ("New York", 1),
    ("Los Angeles", 232),
    ("Chicago", 12),
    ("Houston", 33450),
    ("Miami", 248)
]

list_df = spark.createDataFrame(list_data, ["City", "Temperature"])
print("List file")
list_df.show()

combined_df = csv_df.union(json_clean_df).union(tsv_df).union(list_df).union(xlsx_df).union(text_df1)
print("Combined DataFrames")
combined_df.show()

min_temp_df = combined_df.groupBy("City").agg(min("Temperature").alias("MinTemperature"))

min_temp_df.show()
spark.stop()

""Multiple CSV File in Single Folder""

spark = SparkSession.builder.appName("MinTemperature").getOrCreate()
csv_folder_path = "/content/drive/MyDrive/BDA-EXP:5"
df = spark.read.option("header", "true").csv(csv_folder_path)
print("CSV Folder Values:")
df.show()

print(df.columns)
min_temp_df = df.groupBy("City").agg(min(col("Temperature").alias("Temperature")).alias("MinTemperature"))
min_temp_df.show()

""")