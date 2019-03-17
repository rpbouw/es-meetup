DROP SCHEMA IF EXISTS movies CASCADE;
CREATE SCHEMA movies;
use movies;

DROP TABLE IF EXISTS stage_in;
CREATE TABLE stage_in
(releaseYear varchar(4)
,title varchar(200)
,originEthnicity varchar(20)
,director varchar(200)
,cast varchar(1000)
,genre varchar(100)
,wikiPage varchar(200)
,plot varchar(40000)
);

DROP TABLE IF EXISTS originEthnicity;
CREATE TABLE originEthnicity
(originEthnicityId int IDENTITY NOT NULL PRIMARY KEY
,originEthnicity varchar(20) NOT null);

DROP TABLE IF EXISTS movie;
CREATE TABLE movie
(movieId int IDENTITY NOT NULL PRIMARY KEY
,title varchar(200)
,originEthnicityId int
,director varchar(200)
,cast varchar(1000)
,genre varchar(100)
,wikiPage varchar(200)
,plot varchar(40000)
);

ALTER TABLE movie ADD CONSTRAINT originEthnicity_fk FOREIGN KEY (originEthnicityId) REFERENCES originEthnicity;

--now load data using script, then run below commands

INSERT INTO originEthnicity(originEthnicity) 
select distinct originEthnicity from stage_in;

INSERT INTO movie (originEthnicityId, title, director, cast, genre, wikiPage, plot)
SELECT oe.originEthnicityId,title, director, cast, genre, wikiPage, plot
FROM   stage_in si
INNER JOIN originEthnicity oe ON oe.originEthnicity=si.originEthnicity;

SELECT title, originEthnicity, director, cast, genre, wikiPage, plot
FROM   movie
INNER JOIN originEthnicity oe ON oe.originEthnicityId=movie.originEthnicityId
WHERE  originEthnicity='American'
AND    lower(plot) LIKE '%florence%';

SELECT * FROM originEthnicity;
