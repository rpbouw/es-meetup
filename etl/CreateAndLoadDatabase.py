import csv
import jaydebeapi
import os


def create_and_load_database(csv_file):
    __create_database_schema()
    __copy_csv_to_database(csv_file)
    __fill_normalized_tables()


def __create_database_schema():
    connection = __get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''DROP SCHEMA IF EXISTS movies CASCADE''')
            cursor.execute('''CREATE SCHEMA movies''')
            cursor.execute('''use movies''')
            cursor.execute('''CREATE TABLE stage_in
                            (releaseYear varchar(4)
                            ,title varchar(200)
                            ,originEthnicity varchar(20)
                            ,director varchar(200)
                            ,cast varchar(1000)
                            ,genre varchar(100)
                            ,wikiPage varchar(200)
                            ,plot varchar(40000)
                            )''')
            cursor.execute('''CREATE TABLE originEthnicity
                            (originEthnicityId int IDENTITY NOT NULL PRIMARY KEY
                            ,originEthnicity varchar(20) NOT null)''')
            cursor.execute('''CREATE TABLE movie
                            (movieId int IDENTITY NOT NULL PRIMARY KEY
                            ,releaseYear varchar(4)
                            ,title varchar(200)
                            ,originEthnicityId int
                            ,director varchar(200)
                            ,cast varchar(1000)
                            ,genre varchar(100)
                            ,wikiPage varchar(200)
                            ,plot varchar(40000)
                            )''')
            cursor.execute(
                '''ALTER TABLE movie ADD CONSTRAINT originEthnicity_fk FOREIGN KEY (originEthnicityId) REFERENCES originEthnicity''')
        finally:
            cursor.close()
    finally:
        connection.close()


def __copy_csv_to_database(csv_file):
    connection = __get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''use movies''')
            with open(csv_file, encoding='UTF-8') as f:
                for row in csv.DictReader(f):
                    __process_row(cursor, row)
        finally:
            cursor.close()
    finally:
        connection.close()


def __process_row(cursor, row):
    print(row)
    cursor.execute(
        "INSERT INTO stage_in (releaseYear,title,originEthnicity,director,cast,genre,wikiPage,plot) VALUES (?,?,?,?,?,?,?,?)",
        [row['Release Year'],
         row['Title'],
         row['Origin/Ethnicity'],
         row['Director'],
         row['Cast'],
         row['Genre'],
         row['Wiki Page'],
         row['Plot']]
    )


def __fill_normalized_tables():
    connection = __get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''use movies''')
            cursor.execute('''INSERT INTO originEthnicity(originEthnicity) 
                            select distinct originEthnicity from stage_in''')
            cursor.execute('''INSERT INTO movie (releaseYear, originEthnicityId, title, director, cast, genre, wikiPage, plot)
                            SELECT releaseYear, oe.originEthnicityId,title, director, cast, genre, wikiPage, plot
                            FROM   stage_in si
                            INNER JOIN originEthnicity oe ON oe.originEthnicity=si.originEthnicity''')
        finally:
            cursor.close()
    finally:
        connection.close()


def __get_connection():
    database = __get_database_name()
    connection = jaydebeapi.connect(jclassname="org.h2.Driver",
                                    url="jdbc:h2:{}".format(database),
                                    driver_args=["sa", ""],
                                    jars=__get_path_relative_to_project_root('h2/bin/h2-1.4.199.jar'))
    return connection


def __get_database_name():
    return __get_path_relative_to_project_root('database/movies')


def __get_csv_file_name():
    return __get_path_relative_to_project_root('data/wiki_movie_plots_deduped.csv')


def __get_path_relative_to_project_root(path):
    script_path = os.path.dirname(os.path.realpath(__file__))
    print("script=", script_path)
    project_root = os.path.abspath(os.path.join(script_path, os.pardir))
    sub_path = project_root
    for subdir_name in path.split('/'):
        sub_path = os.path.join(sub_path, subdir_name)
    print("sub=", sub_path)
    return sub_path


if __name__ == '__main__':
    create_and_load_database(__get_csv_file_name())
