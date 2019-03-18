import pandas


def read_csv(csv_file):
    movies_data_frame = pandas.read_csv(csv_file)
    movies_data_frame = movies_data_frame.rename(index=str,
                                                 columns={"Release Year": "releaseYear",
                                                          "Title": "title",
                                                          "Origin/Ethnicity": "originEthnicity",
                                                          "Director": "director",
                                                          "Cast": "cast",
                                                          "Genre": "genre",
                                                          "Wiki Page": "wikiPage",
                                                          "Plot": "plot"})
    print(movies_data_frame.columns)
    print(movies_data_frame["title"].str.len().max())
    print(movies_data_frame["originEthnicity"].str.len().max())
    print(movies_data_frame["director"].str.len().max())
    print(movies_data_frame["cast"].str.len().max())
    print(movies_data_frame["genre"].str.len().max())
    print(movies_data_frame["wikiPage"].str.len().max())
    print(movies_data_frame["plot"].str.len().max())


if __name__ == '__main__':
    read_csv("../data/wiki_movie_plots_deduped.csv")
