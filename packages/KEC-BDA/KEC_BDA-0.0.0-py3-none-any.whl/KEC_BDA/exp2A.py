name = "BDA-Exp:2a(Action)"
def run():
    print("""BDA-Exp:2a(Action)


!pip install pyspark

from pyspark.sql import SparkSession

spark=SparkSession.builder.master("local[2]").appName("SparkByExample.com").getOrCreate()

sc = spark.sparkContext
data = [1,2,3,4,5,6,7,8,9,10,11,12]
rdd=sc.parallelize(data)
print(rdd.count())

sc = spark.sparkContext
data = [1,2,3,4,5,6,7,8,9,10,11,12]
rdd=sc.parallelize(data)
print(rdd.collect())

print(rdd.first())

from pyspark import SparkContext
spark =SparkContext.getOrCreate()
data = [1,2,3,4,5,6,7,8,9,10,11,12]
rdd=spark.parallelize(data)
print(rdd.take(5))

spark =SparkContext.getOrCreate()
data = [1,2,3,4,5,]
rdd=spark.parallelize(data)
print(rdd.reduce(lambda x, y : x + y))

sc = SparkContext.getOrCreate()

reduce_rdd = sc.parallelize([1,3,4,6])
print(reduce_rdd.reduce(lambda x, y : x + y))

sc = SparkContext.getOrCreate()
save_rdd = sc.parallelize([1,2,3,4,5,6])
save_rdd.saveAsTextFile('file2.txt')

from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local[2]").appName("TakeSampleExample").getOrCreate()
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
sample_with_replacement = rdd.takeSample(withReplacement=True, num=5, seed=42)
print("Sample with replacement:", sample_with_replacement)
sample_without_replacement = rdd.takeSample(withReplacement=False, num=5, seed=42)
print("Sample without replacement:", sample_without_replacement)
spark.stop()

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[2]").appName("TakeOrderedExample").getOrCreate()
rdd = spark.sparkContext.parallelize([10, 4, 2, 7, 3, 6, 9, 8, 1, 5])
smallest_five = rdd.takeOrdered(5)
print("Smallest 5 elements:", smallest_five)
largest_five = rdd.takeOrdered(5, key=lambda x: -x)
print("Largest 5 elements:", largest_five)
spark.stop()

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[2]").appName("SaveAsSequenceFileExample").getOrCreate()
rdd = spark.sparkContext.parallelize([("key1", 5), ("key2", 4), ("key3", 3)])
rdd.saveAsSequenceFile("sequence_file-1")
spark.stop()

spark = SparkSession.builder.master("local[2]").appName("SaveAsSequenceFileExample").getOrCreate()
spark.conf.set("dfs.checksum.enabled", "false")
rdd = spark.sparkContext.sequenceFile("sequence_file-1")
rdd.collect()

from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[2]").appName("SaveAsPickleFileExample").getOrCreate()
rdd = spark.sparkContext.parallelize([("key1", 1), ("key2", 2), ("key3", 3)])
rdd.saveAsPickleFile("pickle-file")
spark.stop()

spark = SparkSession.builder.master("local[2]").appName("ReadPickleFileExample").getOrCreate()
rdd = spark.sparkContext.pickleFile("pickle-file")
print(rdd.collect())
spark.stop()



""")