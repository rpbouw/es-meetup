import csv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def copy_csv_to_elasticsearch(csv_file):
    elasticsearch = Elasticsearch()
    csv_file = open(csv_file, encoding='UTF-8')
    dict_reader = csv.DictReader(csv_file)
    bulk(elasticsearch, elasticsearch_bulk_inserter(dict_reader))


def elasticsearch_bulk_inserter(dict_reader):
    row_number = 0
    for csv_model in dict_reader:
        row_number += 1
        if row_number % 1000 == 0:
            print(".", end='')
        elasticsearch_model = __map_csv_to_elasticsearch_model(csv_model)
        yield {'_op_type': 'index', '_index': 'movies_'+elasticsearch_model['releaseYear'], '_type': '_doc', '_source': elasticsearch_model}


def __map_csv_to_elasticsearch_model(csv_model):
    return {'releaseYear': csv_model['Release Year'],
            'title': csv_model['Title'],
            'originEthnicity': csv_model['Origin/Ethnicity'],
            'director': csv_model['Director'],
            'cast': csv_model['Cast'],
            'genre': csv_model['Genre'],
            'wikiPage': csv_model['Wiki Page'],
            'plot': csv_model['Plot']}


if __name__ == '__main__':
    copy_csv_to_elasticsearch("../data/wiki_movie_plots_deduped.csv")
