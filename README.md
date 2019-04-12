# es-meetup

The python scripts in ./etl need some modules, see requirements.txt

I used PyCharm with Virtual Environment setup and Python 3.

Optional steps to simulate a database that could be fed into Elasticsearch in a CQRS model:
The script ./etc/AnalyzeCsv.py analyses the data set so we know what the database field definitions should be.
The script ./etc/CreateAndLoadDatabase.py creates an h2 database "movies" with a "movies" schema in ./database directory.

Step to load the same csv dataset in Elasticsearch:
Script LoadElasticsearch.py reads csv and loads that in Elasticsearch.

