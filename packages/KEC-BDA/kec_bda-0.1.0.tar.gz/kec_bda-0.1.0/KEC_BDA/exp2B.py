name = "BDA-Exp:2b(TRANSFORMATION)"
def run():
    print("""BDA-Exp:2b(TRANSFORMATION)

!pip install pyspark
from pyspark.sql import SparkSession

from pyspark import SparkContext
sc = SparkContext.getOrCreate()

df = sc.parallelize([5,6,7,8,9])
print(df.map(lambda x: x+ 10).collect())

df1 = sc.parallelize([5,6,7,8,9])
print(df1.filter(lambda x: x%2 == 0).collect())

df2 = sc.parallelize(['Hii','Hello','everyone','ready'])
print(df2.filter(lambda x: x.startswith('H')).collect())

df3 = sc.parallelize([2,5,10,15,20,25])
rdd_1 = df3.filter(lambda x: x % 2 == 0)
rdd_2 = df3.filter(lambda x: x % 5 == 0)
print(rdd_1.union(rdd_2).collect())

df4 = sc.parallelize([2,4,5,10,15,20,25,30,32,35])
rdd_1 = df4.filter(lambda x: x % 2 == 0)
rdd_2 = df4.filter(lambda x: x % 5 == 0)
print(rdd_1.intersection(rdd_2).collect())

sub = sc.parallelize([1,2,4,5,6,7,8,9,10])
rdd_1 = sub.filter(lambda x: x % 2 == 0)
rdd_2 = sub.filter(lambda x: x % 5 == 0)
print(rdd_1.subtract(rdd_2).collect())

fmap = sc.parallelize(["Hii everyone", "Welcome to BDA laboratory"])
print(fmap.flatMap(lambda x: x.split(" ")).collect())

key1 = sc.parallelize([('pooja',78),('roshini',89), ('supriya',106),('sree',28)])
print(key1.reduceByKey(lambda x, y: x + y).collect())

print(key1.sortByKey(ascending=True).collect())

ps = key1.groupByKey().collect()
for key, value in ps:
    print(key, list(value))

ps = key1.countByKey().items()
for key, value in ps:
    print(key, value)
""")