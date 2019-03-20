import pandas
import math


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
    movies_data_frame["releaseYear"] = movies_data_frame["releaseYear"].apply(str)
    for header in movies_data_frame.keys():
        exact_max_len = movies_data_frame[header].str.len().max()
        print(header, determine_rounded_max_len(exact_max_len))


def determine_rounded_max_len(max_len):
    if max_len > 10:
        order_of_length = math.floor(math.log10(max_len))
        value_of_order = round(math.pow(10, order_of_length))
        max_len = math.floor(max_len / value_of_order) * value_of_order + value_of_order
    return max_len


if __name__ == '__main__':
    read_csv("../data/wiki_movie_plots_deduped.csv")
