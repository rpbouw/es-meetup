import csv
import jaydebeapi
import os


def create_and_load_database():
    create_database()
    copy_csv_to_database("../data/wiki_movie_plots_deduped.csv")
    normalize_database()


def create_database():
    connection = get_connection()
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
                            ,title varchar(200)
                            ,originEthnicityId int
                            ,director varchar(200)
                            ,cast varchar(1000)
                            ,genre varchar(100)
                            ,wikiPage varchar(200)
                            ,plot varchar(40000)
                            )''')
            cursor.execute('''ALTER TABLE movie ADD CONSTRAINT originEthnicity_fk FOREIGN KEY (originEthnicityId) REFERENCES originEthnicity''')
        finally:
            cursor.close()
    finally:
        connection.close()


def copy_csv_to_database(csv_file):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''use movies''')
            with open(csv_file, encoding='UTF-8') as f:
                for row in csv.DictReader(f):
                    process_row(cursor, row)
        finally:
            cursor.close()
    finally:
        connection.close()


def process_row(cursor, row):
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


def normalize_database():
    connection = get_connection()
    try:
        cursor = connection.cursor()
        try:
            cursor.execute('''use movies''')
            cursor.execute('''INSERT INTO originEthnicity(originEthnicity) 
                            select distinct originEthnicity from stage_in''')
            cursor.execute('''INSERT INTO movie (originEthnicityId, title, director, cast, genre, wikiPage, plot)
                            SELECT oe.originEthnicityId,title, director, cast, genre, wikiPage, plot
                            FROM   stage_in si
                            INNER JOIN originEthnicity oe ON oe.originEthnicity=si.originEthnicity''')
        finally:
            cursor.close()
    finally:
        connection.close()


def get_connection():
    database = get_database_name()
    connection = jaydebeapi.connect(jclassname="org.h2.Driver",
                                    url="jdbc:h2:{}".format(database),
                                    driver_args=["sa", ""],
                                    jars="../h2/bin/h2-1.4.199.jar")
    return connection


def get_database_name():
    script_path = os.path.dirname(os.path.realpath(__file__))
    parent_path = os.path.abspath(os.path.join(script_path, os.pardir))
    database = os.path.join(parent_path, 'database/movies')
    return database


if __name__ == '__main__':
    create_and_load_database()
