import jsonlines
import csv
import re
import collections
import sys

#reload(sys)
#sys.setdefaultencoding('utf8')

game_keys = ['id', 'title', 'genres', 'developer', 'publisher', 'release_date', 'features', 'tags', 'description', 'price', 'sentiment', 'percent_positive', 'n_reviews', 'early_access', 'about', 'reviews', 'discount_price', 'franchise']
game_literals = ['id', 'title', 'release_date', 'description', 'price', 'sentiment', 'percent_positive', 'n_reviews', 'early_access', 'about', 'discount_price', 'franchise']
review_keys = ['product_id', 'recommended', 'date', 'text', 'hours', 'username', 'products', 'early_access', 'found_helpful', 'found_funny', 'compensation']

games = []
gameReviews = dict()
MAX_GAMES = 10
MAX_REVIEWS = 5
with jsonlines.open('../steam-scraper/output/dataset.jl') as reader:
    for game in reader:
        # Limit number of games
        if len(games) > MAX_GAMES:
            break

        # Limit number of reviews per game
        if 'reviews' in game and len(game['reviews']) > MAX_REVIEWS:
            game['reviews'] = game['reviews'][:MAX_REVIEWS]
        
        games.append(game)

files = dict()
files["games"] = csv.writer(open('./csv/games.csv', "w+"))
files["reviews"] = csv.writer(open('./csv/reviews.csv', "w+"))
files["tags"] = csv.writer(open('./csv/tags.csv', "w+"))
files["features"] = csv.writer(open('./csv/features.csv', "w+"))
files["genres"] = csv.writer(open('./csv/genres.csv', "w+"))
files["developer"] = csv.writer(open('./csv/developer.csv', "w+"))
files["publisher"] = csv.writer(open('./csv/pusblisher.csv', "w+"))
files["franchise"] = csv.writer(open('./csv/franchise.csv', "w+"))

for game in games:
    current_review = 1

    for key in game_keys:
        # Ensure same number of columns
        if not key in game.keys() and key in game_literals:
            game[key] = None

        # If it is a list, it should go to its separate csv with the game id
        if key in game and isinstance(game[key], list):
            for value in game[key]:
                # If it is a dict (reviews), write its values (assumes they're literals)
                if isinstance(value, dict):
                    # Ensure same number of columns
                    for review_key in review_keys:
                        if not review_key in value.keys():
                            value[review_key] = None
                    value['review_id'] = current_review
                    current_review += 1
                    value = collections.OrderedDict(sorted(value.items()))

                    files[key].writerow(value.values())
                else:
                    # Not a dict, just id and value
                    files[key].writerow([game["id"], value])
            del game[key]

        # Handle exceptions
        # Write franchise to its file, since there may be null values
        if key == 'franchise' and not game['franchise'] is None:
            files['franchise'].writerow([game["id"], game['franchise']])

    # Ensure same number of columns
    game = collections.OrderedDict(sorted(game.items()))
    # Write the remainder values to the games' csv
    files["games"].writerow(game.values())
