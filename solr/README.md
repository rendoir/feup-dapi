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

