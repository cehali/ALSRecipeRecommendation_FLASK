import heapq
import re
import pandas as pd
import numpy as np
from json import dumps
from flask import Flask

app = Flask(__name__)

recommendations = []
recipes_rated = []
recipes_recom = []
recom_results = []
rated_results = []

user_index = 1

recipes = np.load('recipes.npy')

ratings = pd.read_csv('ratings.csv')

ratings_values = np.load('ratings_values.npy')

recipes_id = np.load('recipes_id.npy')

users_recs = pd.read_csv('recom_users.csv')

ratings_indexed = pd.read_csv('ratings_indexed.csv')

recipes_recommended = users_recs[users_recs['user_id_index'] == user_index]['recommendations'].values[0]
recipes_recommended = [int(s.replace(",", "")) for s in re.findall('\d+,', recipes_recommended)]

for rec in recipes_recommended:
    recommendations.append((ratings_indexed[ratings_indexed['recipe_id_index'] == rec]
                            .groupby('recipe_id_index').first()['recipe_id'].values))

recipes_rated_index = heapq.nlargest(20, range(len(ratings_values[user_index])), ratings_values[user_index].take)
recipes_rated_id = recipes_id[[recipes_rated_index]]

for rec1, rec2 in zip(recipes_rated_id, recommendations):
    for recipe in recipes:
        if rec1 == recipe.get('amazon_id'):
            recipes_rated.append(recipe)
        if rec2[0] == recipe.get('amazon_id'):
            recipes_recom.append(recipe)

for i in range(0, len(recipes_rated)):
    rated_results.append(str(recipes_rated[i].get('title')))

for i in range(0, len(recipes_recom)):
    recom_results.append(str(recipes_recom[i].get('title')))


@app.route('/rated', methods=['GET'])
def get_recipes_rated():

    return dumps(rated_results)


@app.route('/recom', methods=['GET'])
def get_recommendation():

    return dumps(recom_results)


if __name__ == "__main__":
    app.run()

