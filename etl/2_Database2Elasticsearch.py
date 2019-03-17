import csv
import jaydebeapi
import os


def map_csv_to_model(csv_model):
    return {'releaseYear': csv_model['Release Year'],
            'title': csv_model['Title'],
            'originEthnicity': csv_model['Origin/Ethnicity'],
            'director': csv_model['Director'],
            'cast': csv_model['Cast'],
            'genre': csv_model['Genre'],
            'wikiPage': csv_model['Wiki Page'],
            'plot': csv_model['Plot']}


def copy_csv_to_database(csv_file):
    try:
        script_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = os.path.abspath(os.path.join(script_path, os.pardir))
        database = os.path.join(parent_path, 'database/data')
        conn = jaydebeapi.connect(jclassname="org.h2.Driver",
                                  url="jdbc:h2:tcp://localhost:9092/{};SCHEMA=movies".format(database),
                                  driver_args=["sa", ""],
                                  jars="../h2/bin/h2-1.4.199.jar")
        curs = conn.cursor()

        with open(csv_file, encoding='UTF-8') as f:
            for row in csv.DictReader(f):
                print(row)
                curs.execute(
                    "INSERT INTO stage_in (releaseYear,title,originEthnicity,director,cast,genre,wikiPage,plot) VALUES (?,?,?,?,?,?,?,?)",
                    [row['Release Year'],
                     row['Title'],
                     row['Origin/Ethnicity'],
                     row['Director'],
                     row['Cast'],
                     row['Genre'],
                     row['WikiPage'],
                     row['Plot']]
                )
    finally:
        if curs is not None:
            curs.close()
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    copy_csv_to_database("../data/wiki_movie_plots_deduped.csv")
