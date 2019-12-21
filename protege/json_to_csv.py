import jsonlines
import csv
import re

i = 1
games = []
with jsonlines.open('../steam-scraper/output/dataset.jl') as reader:
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
    for key in list(game.keys()):
        # If it is a list, it should go to its separate csv with the game id
        if isinstance(game[key], list):
            for value in game[key]:
                # If it is a dict (reviews), write its values (assumes they're literals)
                if isinstance(value, dict):
                    files[key].writerow(value.values())
                else:
                    files[key].writerow([game["id"], value])
            del game[key]
    # Write the remainder values to the games' csv
    files["games"].writerow(game.values())
