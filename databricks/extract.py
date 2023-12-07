# Databricks notebook source
from delta.tables import *
from pyspark.sql.functions import *

delta_table_path = '/delta/news-delta'

# Create a deltaTable object
deltaTable = DeltaTable.forPath(spark, delta_table_path)

# View the updated data as a dataframe
deltaTable.toDF().orderBy(desc('date')).show(10)

# COMMAND ----------

is_delta_table = DeltaTable.isDeltaTable(spark, delta_table_path)
print(is_delta_table)
# move delta table from dbfs to catalog 
deltaTable.toDF().write.format("delta").mode("overwrite").saveAsTable("news")

# COMMAND ----------

delta_table_path = '/delta/stocks-delta'

# Create a deltaTable object
deltaTable = DeltaTable.forPath(spark, delta_table_path)

# View the updated data as a dataframe
deltaTable.toDF().show(10)

# COMMAND ----------

is_delta_table = DeltaTable.isDeltaTable(spark, delta_table_path)
print(is_delta_table)
# move delta table from dbfs to catalog 
deltaTable.toDF().write.format("delta").mode("overwrite").saveAsTable("stock")

# COMMAND ----------

delta_table_path = '/delta/training_news-delta'

is_delta_table = DeltaTable.isDeltaTable(spark, delta_table_path)
print(is_delta_table)
# move delta table from dbfs to catalog 
deltaTable.toDF().write.format("delta").mode("overwrite").saveAsTable("training_news")
