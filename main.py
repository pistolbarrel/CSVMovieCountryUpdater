import csv
import os

import requests
import json


def prepareTitle(title):
    title = prepareOther(title)
    if title[0:4] == "The ":
        title = title[4:] + ", " + title[0:3]
    if title[0:2] == "A ":
        title = title[2:] + ", " + title[0:1]
    return title


def prepareOther(other):
    return other.replace("&CM^", ',')


def updateCountryOnExistingMovies():
    put_uri = "http://localhost:8080/rest/addcountryonexisting"

    # csv file has columns title, director, country, year
    TITLE = 0
    DIRECTOR = 1
    COUNTRY = 2
    YEAR = 3

    with open('Country.csv', encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        update_count = 0
        for row in csv_reader:
            movie_dto = {"title": prepareTitle(row[TITLE]),
                         "year": row[YEAR],
                         "countries": row[COUNTRY],
                         "actors": "",
                         "directors": "",
                         "collections": ""
                         }

            response = requests.put(put_uri, json=movie_dto)
            if response.status_code != 200:
                print("Movie does not exist " + prepareTitle(row[TITLE]) + ":" + row[YEAR])
            else:
                update_count += 1
            line_count += 1
            if line_count % 100 == 0:
                print(f'Processed {line_count} lines.')
    print(f'Processed {line_count} lines, updating {update_count} movies')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    updateCountryOnExistingMovies()
