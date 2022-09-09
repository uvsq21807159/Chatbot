import pyodbc
import numpy as np
import random as rd
from azure_composants import *
from model import create_model
from normalizer import IGNORE_WORDS, tokenize, stem_and_lower, bag_of_words
from query_db import *
from train import intents
#connection to database
cnxn = pyodbc.connect(
    "DRIVER={ODBC Driver 18 for SQL Server};SERVER="
    + SERVER
    + ";DATABASE="
    + DATABASE
    + ";UID="
    + USERNAME
    + ";PWD="
    + PASSWORD
)
cursor = cnxn.cursor()

#recovery of data from the pickle file
model, all_words, tags = create_model("data/data.pickle")

#function that returns the answer generate
def bot_response(message):
    while True:
        message = tokenize(message)
        message = [
            stem_and_lower(word) for word in message if word not in IGNORE_WORDS
        ]
        #calculation of predictions
        result = model.predict([bag_of_words(message, all_words)])
        result_i = np.argmax(result)
        tag = tags[result_i]

        if tag == "day_ranking":
            return day_ranking(cursor)
        elif tag == "min_pollution_hour":
            return min_pollution_hour(cursor)
        elif tag == "max_pollution_hour":
            return max_pollution_hour(cursor)
        elif tag == "loc_ranking":
            return loc_ranking(cursor)
        elif tag == "recent_news":
            return recent_news(cursor)
        elif tag == "hour_ranking":
            return hour_ranking(cursor)
        elif tag == "max_pollution_day":
            return max_pollution_day(cursor)
        elif tag == "min_pollution_day":
            return min_pollution_day(cursor)
        elif tag == "wrong_place_wrong_time":
            return wrong_place_wrong_time(cursor)
        elif tag == "wrong_place_wrong_date":
            return wrong_place_wrong_date(cursor)
        elif tag == "versailles_current_pollution":
            return versailles_current_pollution(cursor)
        elif tag == "lille_current_pollution":
            return lille_current_pollution(cursor)
        elif tag == "nice_current_pollution":
            return nice_current_pollution(cursor)
        elif tag == "brest_current_pollution":
            return brest_current_pollution(cursor)
        elif tag == "bayonne_current_pollution":
            return bayonne_current_pollution(cursor)
        elif tag == "strasbourg_current_pollution":
            return strasbourg_current_pollution(cursor)

        else:
            for tg in intents["intents"]:
                if tg["tag"] == tag:
                    responses = tg["responses"]

            return rd.choice(responses)
