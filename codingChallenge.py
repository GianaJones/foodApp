
import requests
import json
import time
from datetime import datetime
import pandas as pd
import csv
import streamlit as st
import numpy


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
meal = st.selectbox("Meal: ", ["Breakfast", "Lunch", "Dinner"])

locationID = 0
mealID = 0

meals = pd.read_csv("wellesley-meals.csv")
ids = pd.read_csv("wellesley-dining.csv")


if dining_hall == "Lulu":
    locationID = ids.loc[0]["locationId"]
    if meal == "Breakfast":
        mealID = ids.loc[0]["mealID"]
    elif meal == "Lunch":
        mealID = ids.loc[1]["mealID"]
    elif meal == "Dinner":
        mealID = ids.loc[2]["mealID"]

if dining_hall == "Tower":
    locationID = ids.loc[9]["locationId"]
    if meal == "Breakfast":
        mealID = ids.loc[9]["mealID"]
    elif meal == "Lunch":
        mealID = ids.loc[10]["mealID"]
    elif meal == "Dinner":
        mealID = ids.loc[11]["mealID"]

if dining_hall == "Bates":
    locationID = ids.loc[3]["locationId"]
    if meal == "Breakfast":
        mealID = ids.loc[3]["mealID"]
    elif meal == "Lunch":
        mealID = ids.loc[4]["mealID"]
    elif meal == "Dinner":
        mealID = ids.loc[5]["mealID"]

if dining_hall == "Stone D":
    locationID = ids.loc[6]["locationId"]
    if meal == "Breakfast":
        mealID = ids.loc[6]["mealID"]
    elif meal == "Lunch":
        mealID = ids.loc[7]["mealID"]
    elif meal == "Dinner":
        mealID = ids.loc[8]["mealID"]

#st.write(locationID)
#st.write(mealID)

menu = pd.DataFrame(get_menu(date, locationID, mealID))

displayMenu = menu.drop(columns = ["id", "image", "categoryName", "stationOrder", "allergens", "preferences", "price", "nutritionals"])


#result = pd.DataFrame(columns = ["name", "date", "description", "stationName"])

resulty = []

for i in range(len(displayMenu)):
    row = displayMenu.iloc[i]
    if date in row["date"]:
        resulty.append(row)
        #st.write(row["name"])
        #result = result.add(row)

result = pd.DataFrame(resulty)
    
with st.expander("Menu"):
    st.write(result)

col1, col2, col3, col4 = st.columns(("name", "date", "description", "category"),
                                    vertical_alignment = 'center'
)


#st.write(result, columns = ["name", "date", "description", "stationName"])




