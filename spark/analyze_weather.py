from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, max, min

spark = (
    SparkSession.builder.appName('WeatherAnalysis')
    .master('spark://spark-master:7077')
    .getOrCreate()
)

df = spark.read.option('header', True).csv('/opt/airflow/spark/weather_data.csv')
df = df.withColumn('temperature', df['temperature'].cast('float'))

agg_data = df.agg(
    avg('temperature').alias('avg_temp'),
    min('temperature').alias('min_temp'),
    max('temperature').alias('max_temp'),
)

agg_data.show()

spark.stop()
