import csv
from elasticsearch import Elasticsearch


def map_csv_to_elasticsearch_model(csv_model):
    return {'releaseYear': csv_model['Release Year'],
            'title': csv_model['Title'],
            'originEthnicity': csv_model['Origin/Ethnicity'],
            'director': csv_model['Director'],
            'cast': csv_model['Cast'],
            'genre': csv_model['Genre'],
            'wikiPage': csv_model['Wiki Page'],
            'plot': csv_model['Plot']}


def copy_csv_to_elasticsearch(csv_file):
    elasticsearch = Elasticsearch()

    with open(csv_file, encoding='UTF-8') as f:
        for csv_model in csv.DictReader(f, skipinitialspace=True):
            elasticsearch_model = map_csv_to_elasticsearch_model(csv_model)
            elasticsearch.index(index="movies", doc_type='_doc', body=elasticsearch_model)


if __name__ == '__main__':
    copy_csv_to_elasticsearch("wiki_movie_plots_deduped.csv")
