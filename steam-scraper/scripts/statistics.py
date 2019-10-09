import argparse
import jsonlines
import seaborn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def statistics():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', type=str, default="output/dataset.jl")
    args = parser.parse_args()

    # Statistics default values
    total_n_games = 0
    total_n_reviews = 0
    total_n_scraped_reviews = 0
    n_scraped_reviews_per_game = []
    n_reviews_per_game = []
    about_text_lengths = []
    review_text_lengths = []
    total_about_text_length = 0
    total_review_text_length = 0
    usernames = set()
    genres_popularity = dict()

    # Loop each game
    with jsonlines.open(args.dataset) as reader:
        for game in reader:
            total_n_games += 1
            total_n_reviews += game["n_reviews"]
            
            scraped_reviews = game.get("reviews", [])
            total_n_scraped_reviews += len(scraped_reviews)
            n_scraped_reviews_per_game.append(len(scraped_reviews))
            n_reviews_per_game.append(game["n_reviews"])

            about_length = len(game.get("about", ""))
            about_text_lengths.append(about_length)
            total_about_text_length += about_length
            for review in scraped_reviews:
                review_length = len(review.get("text", ""))
                review_text_lengths.append(review_length)
                total_review_text_length += review_length
                usernames.add(review.get("username", ""))

            for genre in game.get("genres", []):
                if not genre in genres_popularity:
                    genres_popularity[genre] = 0 
                genres_popularity[genre] += 1

    # Post-loop statistical calculations
    average_review_per_game = total_n_scraped_reviews / total_n_games
    average_about_text_length = total_about_text_length / total_n_games
    average_review_text_length = total_review_text_length / total_n_scraped_reviews
    
    # Print simple statistics
    print(f'Total games: 36469')
    print(f'Total reviews: {total_n_reviews}')
    print(f'Scraped Games: {total_n_games}')
    print(f'Scraped reviews: {total_n_scraped_reviews}')
    print(f'Distinct users: {len(usernames)}')
    print(f'Average reviews per game: {average_review_per_game}')
    print(f'Average about length: {average_about_text_length}')
    print(f'Average review body: {average_review_text_length}')

    # Plots
    # About length histogram
    seaborn.distplot(about_text_lengths, hist=True, kde=False, hist_kws={'edgecolor':'black'})
    plt.title('Histogram of game description lengths')
    plt.xlabel('Description length (in characters)')
    plt.ylabel('Games')
    plt.savefig("output/about_lengths.png")
    plt.clf()

    # Genres popularity
    genresx = np.array(list(genres_popularity.keys())).astype(str)
    genresy = np.array(list(genres_popularity.values())).astype(int)
    genresData = pd.DataFrame({'Genres': genresx, 'Games': genresy})
    seaborn.barplot(data=genresData, y='Genres', x='Games')
    plt.title('Genres popularity')
    plt.xlabel('Games')
    plt.ylabel('Genres')
    plt.savefig("output/genres_popularity.png", bbox_inches = "tight")
    plt.clf()

    # Scraped reviews per game
    seaborn.distplot(n_scraped_reviews_per_game, hist=True, kde=False, color='#ff615e', hist_kws={'edgecolor':'black'}, bins=10)
    plt.title('Histogram of game reviews')
    plt.xlabel('Reviews')
    plt.ylabel('Games')
    plt.savefig("output/game_reviews.png")
    plt.clf()


if __name__ == '__main__':
    statistics()
