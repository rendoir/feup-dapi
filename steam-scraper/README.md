# Steam Scraper

This repository contains [Scrapy](https://github.com/scrapy/scrapy) spiders for **crawling products** and **scraping all user-submitted reviews** from the [Steam game store](https://steampowered.com).

## Installation

Install Python 3 and virtualenv

Clone the repository
```bash
git clone https://github.com/rendoir/feup-dapi.git
```
Start and activate a Python 3 virtualenv with:
```bash
cd feup-dapi/steam-scraper/
virtualenv -p python3 env
. env/bin/activate
```
Install Python dependencies via:
```bash
pip3 install -r dependencies.txt
```

## Crawling the Products

The purpose of `ProductSpider` is to discover product pages on the [Steam product listing](http://store.steampowered.com/search/?) and extract useful metadata from them.
A neat feature of this spider is that it automatically navigates through Steam's age verification checkpoints.  

To crawl through all the products on Steam:
```bash
scrapy crawl products -o output/products.jl 
```
When it completes you should have metadata for all games on Steam in `output/products.jl`.

It's also possible to retrieve only one product:
```bash
scrapy crawl products -o output/product.jl -a steam_id=812140
```

Scrapy also includes a setting to limit the number of scraped products:
```bash
scrapy crawl products -o output/products.jl -s CLOSESPIDER_ITEMCOUNT=10
```

Here's some example output:
```python
{
    'title': "Assassin's Creed® Odyssey",
    'description': "Choose your fate in Assassin's Creed® Odyssey. From outcast "
                   'to living legend, embark on an odyssey to uncover the secrets '
                   'of your past and change the fate of Ancient Greece.',
    'developer': ['Ubisoft Quebec', 'Ubisoft Montreal', 'Ubisoft Bucharest', 
                  'Ubisoft Singapore', 'Ubisoft Montpellier', 'Ubisoft Kiev', 
                  'Ubisoft Shanghai'],
    'early_access': False,
    'genres': ['Action', 'Adventure', 'RPG'],
    'id': 812140,
    'n_reviews': 28504,
    'percent_positive': 84,
    'price': 59.99,
    'publisher': ['Ubisoft'],
    'franchise': "Assassin's Creed", 
    'release_date': "05-10-2018",
    'sentiment': 'Very Positive',
    'features': ['Single-player', 'Steam Achievements', 'Steam Trading Cards',
              'Captions available', 'In-App Purchases', 'Partial Controller Support'],
    'tags': ['Open World', 'RPG', 'Assassin',
             'Singleplayer', 'Action', 'Historical',
             'Adventure', 'Stealth', 'Story Rich',
             'Third Person', 'Parkour', 'Female Protagonist',
             'Sexual Content', 'Choices Matter', 'Violent',
             'Atmospheric', 'Great Soundtrack', 'Nudity',
             'Multiplayer', 'Gore'],
    'about': "Choose your fate in Assassin's Creed® Odyssey.From outcast to "
          'living legend, embark on an odyssey to uncover the secrets of your '
          'past and change the fate of Ancient Greece.TRAVEL TO ANCIENT GREECE '
          'From lush vibrant forests to volcanic islands and bustling cities, '
          'start a journey of exploration and encounters in a war torn world '
          'shaped by gods and men.FORGE YOUR LEGENDYour decisions will impact '
          'how your odyssey unfolds. Play through multiple endings thanks to '
          'the new dialogue system and the choices you make. Customize your '
          'gear, ship, and special abilities to become a legend.FIGHT ON A NEW '
          "SCALEDemonstrate your warrior's abilities in large scale epic "
          'battles between Athens and Sparta featuring hundreds of soldiers, '
          'or ram and cleave your way through entire fleets in naval battles '
          'across the Aegean Sea.GAZE IN WONDERExperience the action in a '
          'whole new light with Tobii Eye Tracking. The Extended View feature '
          'gives you a broader perspective of the environment, and the Dynamic '
          'Light and Sun Effects immerse you in the sandy dunes according to '
          'where you set your sights. Tagging, aiming and locking on your '
          'targets becomes a lot more natural when you can do it by looking at '
          'them. Let your vision lead the way and enhance your gameplay. Visit '
          'the Tobii website to check the list of compatible devices. '
          '-----Additional notes:Eye tracking features available with Tobii '
          'Eye Tracking.'
}
```

## Extracting the Reviews

The purpose of `ReviewSpider` is to scrape user-submitted reviews of a particular product (`steam_id` parameter) or set a of products from the [Steam community portal](http://steamcommunity.com/).

It can alternatively ingest a text file containing URLs such as
```
https://steamcommunity.com/app/316790/reviews/?browsefilter=mostrecent&p=1
https://steamcommunity.com/app/207610/reviews/?browsefilter=mostrecent&p=1
https://steamcommunity.com/app/414700/reviews/?browsefilter=mostrecent&p=1
```
via the `url_file` command line argument:
```bash
scrapy crawl reviews -o output/reviews.jl -a url_file=url_file.txt
```

It can also process the output file from a previous product crawl, scraping all reviews for all the products in the file using the `games_file` command line argument:
```bash
scrapy crawl reviews -o output/reviews.jl -a games_file=output/products.jl
```

There's also an option to limit the number of reviews per product:
```bash
scrapy crawl reviews -o output/reviews.jl -a steam_id=812140 -a limit=100
```

Or limit the total number of reviews using Scrapy's settings:
```bash
scrapy crawl reviews -o output/reviews.jl -a games_file=output/products.jl -s CLOSESPIDER_ITEMCOUNT=1000
```

Here's an output sample:
```python
{
    'date': '2019-08-12',
    'early_access': False,
    'found_funny': 2,
    'hours': 70.9,
    'product_id': 812140,
    'products': 156,
    'recommended': True,
    'found_helpful': 33,
    'found_funny': 2,
    'text': "Ubisoft really wasn't joking around when it called the latest "
            "Assassin's Creed game an Odyssey. It's not just in the Greek "
            'tragedy-inspired story, the vast, vast map or the sheer number of '
            "hours you're going to sink into it. It's the journey. The journey "
            'from one Greek island to another, with dolphins and whales cresting '
            "the waves alongside your boat. It's about the journey across the "
            "stunning Grecian landscape, it's also about the journey to discover "
            "who exactly you are in Assassin's Creed Odyssey.",
    'username': 'BGy'}
```
