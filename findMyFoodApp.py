import requests
import json
import time
from datetime import datetime
import pandas as pd
import csv
import streamlit as st
import numpy


def get_week_menu(date, locationID, mealID):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date": date, "locationID": locationID, "mealID": mealID}
    result = requests.get(base_url, params=params).text
    data = json.loads(result)
    return pd.DataFrame(data)

def get_day_menu(date, locationID, mealID):
    base_url = "https://dish.avifoodsystems.com/api/menu-items/week"
    params = {"date": date, "locationID": locationID, "mealID": mealID}
    result = requests.get(base_url, params=params).text
    data = json.loads(result)
    df = pd.DataFrame(data)
    df = df[df["date"] == date]
    df = df.drop_duplicates(subset="id")
    if df.empty:
        st.info(f"No menu available for today {datetime.today}")
        return False
    return df

st.title("Find My Food!")

#Manipulating date to match date in dataframe
date = str(st.date_input("Date: ")) + "T00:00:00"




dining_hall = st.selectbox("Dining Hall: ", ["Lulu", "Tower", "Stone D", "Bates"])
meal = st.selectbox("Meal: ", ["Breakfast", "Lunch", "Dinner"])



locationID = 0
mealID = 0

with open("wellesley-meals.csv", "r") as file:
    meals = pd.read_csv(file)
    
ids = pd.read_csv("wellesley-dining.csv")

def get_meal_and_location(df, loc, meal):
    """

    """
    if loc == "Lulu":
        loc = "Bao"
    matching_df = df[(df["location"] == loc) & (df["meal"] == meal)]
    locationID = matching_df["locationId"].iloc[0]
    mealID = matching_df["mealID"].iloc[0]
    return locationID, mealID


locationID, mealID = get_meal_and_location(ids, dining_hall, meal)

menu = st.button("Show Menu")
if menu:
    st.write(get_day_menu(date, locationID, mealID))

