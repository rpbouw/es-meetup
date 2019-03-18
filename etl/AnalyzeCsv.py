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
    print_column(movies_data_frame,"title")
    print_column(movies_data_frame,"originEthnicity")
    print_column(movies_data_frame,"director")
    print_column(movies_data_frame,"cast")
    print_column(movies_data_frame,"genre")
    print_column(movies_data_frame,"wikiPage")
    print_column(movies_data_frame,"plot")


def print_column(data_frame, column_name):
    print(column_name, data_frame[column_name].str.len().max())


if __name__ == '__main__':
    read_csv("../data/wiki_movie_plots_deduped.csv")
