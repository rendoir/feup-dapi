# Solr commands

## Basic

### Solr

Start solr

`bin/solr start`

Stop solr

`bin/solr stop`

### Core

Creating core:

`bin/solr create_core -c [core_name]`

Deleting core:

`bin/solr delete [core_name]`

## Indexing

### Via post

1 doc per game

`bin/post -c [core_name] [file/dir_path]`

### Via update

1 doc per review

`curl 'http://localhost:8983/solr/core_name/update/json/docs?split=/reviews&commit=true' -H 'Content-type:application/json' --data-binary @[file_path]`


1 doc per game and review

`curl 'http://localhost:8983/solr/core_name/update/json/docs?split=/|/reviews&commit=true' -H 'Content-type:application/json' --data-binary @[file_path]`

## Schema

Get schema fields

`curl http://localhost:8983/solr/games3/schema/fields`

Get schema field types

`curl http://localhost:8983/solr/games3/schema/fieldtypes`

## Query

### Parents Query Parser

Filters games based on reviews

Select all games

`curl http://localhost:8983/solr/games2/query -d 'q={!parent which="title:*"}'`

Select all games that have a least a review that has the word "hell" in its text

`curl http://localhost:8983/solr/games2/query -d 'q={!parent which="title:*"}text:hell'`

### Children Query Parser

Filters reviews based on games

Select all reviews

`curl http://localhost:8983/solr/games2/query -d 'q={!child of="title:*"}'`

Select all reviews that belong to a game that has the word "tomb" in its title

`curl http://localhost:8983/solr/games2/query -d 'q={!child of="title:*"}title:tomb'`

### Child Doc Transformer

Appends reviews in results

Select all games and append all reviews for each

`curl http://localhost:8983/solr/games2/query -d 'q={!parent which="title:*"}&fl=*,[child]'`

Select all games and append all reviews that don't recommend the game for each

`curl http://localhost:8983/solr/games2/query -d 'q={!parent which="title:*"}&fl=*,[child childFilter=/reviews/recommended:false]'`
