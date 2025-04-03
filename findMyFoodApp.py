
import requests
import json
import time
from datetime import datetime
import pandas as pd
import csv
import streamlit as st


def get_menu(date, locationID, mealID):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date": date, "locationID": locationID, "mealID": mealID}
    result = requests.get(base_url, params=params).text
    return json.loads(result)


def write_menus(filename, date):
    with open(filename, "r") as f:
        file = csv.DictReader(f)
        if "/" in date:
            date = date.replace("/", "-")
        for item in file:
            time.sleep(2)
            locID =  item['locationId']
            mealID = item['mealID']
            toDump = get_menu(date, locID, mealID)
            with open(f"{item["location"]}-{item["meal"]}-{date}.json", "w") as f:
                json.dump(toDump, f)

st.title("Find My Food!")
date = st.date_input("Date: ")
date = str(date)
#url_file = write_menus("wellesley-dining.csv", date)

dining_hall = st.selectbox("Dining Hall: ", ["Lulu", "Tower", "Stone D", "Bates"])
locationID = 0
mealID = 0

ids = pd.read_csv("wellesley-dining.csv")


if dining_hall == "Lulu":
    locationID = ids.loc[0]["locationId"]

if dining_hall == "Tower":
    locationID = ids.loc[9]["locationId"]

if dining_hall == "Bates":
    locationID = ids.loc[3]["locationId"]

if dining_hall == "Stone D":
    locationID = ids.loc[6]["locationId"]

st.write(locationID)

#with open("wellesley-dining.csv", "r") as wd:
    #wd_Dict = csv.DictReader(wd)

    #result = pd.DataFrame()
    #for item in wd_Dict:
        #with open(f"{item["location"]}-{item["meal"]}-02-20-2025.json", "r") as menu:
            #data = json.load(menu)
            #newdf = pd.DataFrame(data)
            #result = pd.concat([result, newdf], ignore_index=True)
            #print(f"Appended {item["location"]}-{item["meal"]}-02-20-2025.json. Now size is {result.shape}")

#result.head()
#columns = result.columns
#betterNowDF = result.drop(columns = ['image', 'description',  'categoryName',
       #'stationName', 'stationOrder', 'allergens', 'preferences', 'price',
       #'nutritionals'], inplace = False)

#print(betterNowDF.head(100))