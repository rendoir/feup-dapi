import jsonlines
import csv
import re
import collections


game_keys = ['id', 'title', 'genres', 'developer', 'publisher', 'release_date', 'features', 'tags', 'description', 'price', 'sentiment', 'percent_positive', 'n_reviews', 'early_access', 'about', 'reviews', 'discount_price', 'franchise']
game_literals = ['id', 'title', 'release_date', 'description', 'price', 'sentiment', 'percent_positive', 'n_reviews', 'early_access', 'about', 'discount_price', 'franchise']
games = []
with jsonlines.open('./dataset.jl') as reader:
    for game in reader:
        games.append(game)

files = dict()
files["games"] = csv.writer(open('./csv/games.csv', "w+"))
files["reviews"] = csv.writer(open('./csv/reviews.csv', "w+"))
files["tags"] = csv.writer(open('./csv/tags.csv', "w+"))
files["features"] = csv.writer(open('./csv/features.csv', "w+"))
files["genres"] = csv.writer(open('./csv/genres.csv', "w+"))
files["developer"] = csv.writer(open('./csv/developer.csv', "w+"))
files["publisher"] = csv.writer(open('./csv/pusblisher.csv', "w+"))

for game in games:
    for key in game_keys:
        # Ensure same number of columns
        if not key in game.keys() and key in game_literals:
            game[key] = None

        # If it is a list, it should go to its separate csv with the game id
        if key in game and isinstance(game[key], list):
            for value in game[key]:
                # If it is a dict (reviews), write its values (assumes they're literals)
                if isinstance(value, dict):
                    files[key].writerow(value.values())
                else:
                    files[key].writerow([game["id"], value])
            del game[key]

    # Ensure same number of columns
    game = collections.OrderedDict(sorted(game.items()))
    # Write the remainder values to the games' csv
    files["games"].writerow(game.values())
