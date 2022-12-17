import pandas as pd
import pymongo
from dataclasses import dataclass
import os,sys


@dataclass
class Evsvarible:
    mongo_url = os.getenv("Mongo_db_url")



evs = Evsvarible()
mongoclient = pymongo.MongoClient(evs.mongo_url)
Target_column = "class"
