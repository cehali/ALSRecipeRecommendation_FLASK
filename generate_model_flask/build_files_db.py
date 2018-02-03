import pandas as pd
import numpy as np

ratings = pd.read_csv('ratings.csv')

ratings_pivot = ratings.pivot_table(values='rating', index=['user_id'], columns=['recipe_id'], fill_value=0,
                                    dropna=False)

ratings_values = ratings_pivot.values

np.save('ratings_values', ratings_values)

recipes_id = ratings_pivot.columns.values.tolist()

np.save('recipes_id', recipes_id)