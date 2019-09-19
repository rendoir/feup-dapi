import re
import argparse

def merge_files():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dataset', type=str, default="output/dataset.jl")
    parser.add_argument('-p', '--products', type=str, default="output/products.jl")
    parser.add_argument('-r', '--reviews', type=str, default="output/reviews.jl")
    args = parser.parse_args()

    dataset_file = open(args.dataset, "w+")
    products_file = open(args.products, "r")
    reviews_file = open(args.reviews, "r")

    id_to_product = dict()

    for product in products_file:
        id = re.search('\"id\": \"(\d+)\"', product).group(1)
        id_to_product[id] = product

    id_to_reviews = dict()

    for review in reviews_file:
        id = re.search('\"product_id\": \"(\d+)\"', review).group(1)
        if id in id_to_reviews:
            id_to_reviews[id] = id_to_reviews[id] + ", "
            id_to_reviews[id] = id_to_reviews[id] + review.rstrip("\n\r")
        else:
            id_to_reviews[id] = review.rstrip("\n\r")

    for product_id in id_to_product:
        dataset_line = id_to_product[product_id].rstrip("\n\r")[:-1]
        if product_id in id_to_reviews:
            dataset_line = dataset_line + ', "reviews": [' + id_to_reviews[product_id] + ']}'
        dataset_file.write(dataset_line + "\n")

    dataset_file.close()
    products_file.close()
    reviews_file.close()


if __name__ == '__main__':
    merge_files()
