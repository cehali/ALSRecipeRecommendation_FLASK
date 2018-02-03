import pandas as pd
import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer
from pyspark.ml.recommendation import ALS
from pyspark.shell import spark

recipes = np.load('recipes.npy')

ratings = pd.read_csv('ratings.csv')

ratings_values = np.load('ratings_values.npy')

ratings = spark.createDataFrame(ratings)

string_indexer1 = StringIndexer(inputCol="user_id", outputCol="user_id_index")
string_indexer2 = StringIndexer(inputCol="recipe_id", outputCol="recipe_id_index")

print string_indexer2

indexers = [string_indexer1, string_indexer2]

pipeline = Pipeline(stages=indexers)

ratings_final = pipeline.fit(ratings).transform(ratings)

als = ALS(rank=20, maxIter=20, regParam=0.1, userCol="user_id_index", itemCol="recipe_id_index", ratingCol="rating",
          coldStartStrategy="drop")
model = als.fit(ratings_final)

users_recs = model.recommendForAllUsers(10)

ratings_final.toPandas().to_csv('ratings_indexed.csv', index=False)

model.write().overwrite().save('recommendation_model_complete')

users_recs.toPandas().to_csv('recom_users.csv', index=False)





