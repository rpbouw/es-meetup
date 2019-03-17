import pandas


def read_csv(csv_file):
    moviesDataFrame = pandas.read_csv(csv_file)
    moviesDataFrame = moviesDataFrame.rename(index=str,
                                             columns={"Release Year": "releaseYear"
                                                 , "Title": "title"
                                                 , "Origin/Ethnicity": "originEthnicity"
                                                 , "Director": "director"
                                                 , "Cast": "cast"
                                                 , "Genre": "genre"
                                                 , "Wiki Page": "wikiPage"
                                                 , "Plot": "plot"});
    print(moviesDataFrame.columns)
    print(moviesDataFrame["title"].str.len().max())
    print(moviesDataFrame["originEthnicity"].str.len().max())
    print(moviesDataFrame["director"].str.len().max())
    print(moviesDataFrame["cast"].str.len().max())
    print(moviesDataFrame["genre"].str.len().max())
    print(moviesDataFrame["wikiPage"].str.len().max())
    print(moviesDataFrame["plot"].str.len().max())


if __name__ == '__main__':
    read_csv("../data/wiki_movie_plots_deduped.csv")
