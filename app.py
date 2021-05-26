from pycaret.classification import load_model, predict_model
import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import json


model = load_model("gbm_model_15May2021")


def predict(model, input_df):
    prediction_df = predict_model(estimator=model, data=input_df)
    predictions = prediction_df["Label"]
    return predictions


@st.cache(suppress_st_warning=True)
def image_func():
    image_AUS = Image.open("flag.jpg")
    image_land = Image.open("AUS_land.jpg")
    st.image(image_AUS)
    st.sidebar.image(image_land)


image_func()


def run():

    st.title("Does is rain tomorrow?")
    st.subheader("A prototype app to demonstrate the weather forecasting model")

    select_bar = st.sidebar.selectbox(
        "How would you like to predict?", ("Online", "Batch")
    )

    st.sidebar.info("This app can predict if it is going to rain tomorrow")

    with open("locationAndWind.json") as f:
        cat_values_dict = json.load(f)

    if select_bar == "Online":
        Location = st.selectbox("Location", cat_values_dict["locations"])
        WindGustDir = st.selectbox("WindGustDir", cat_values_dict["windDir"])
        MinTemp = st.number_input(
            "Minimum Temperature", min_value=-10, max_value=40, value=20
        )
        MaxTemp = st.number_input(
            "Maximum Temperature", min_value=-5, max_value=50, value=20
        )
        Rainfall = st.number_input(
            "Rainfall (mm)", min_value=0.0, max_value=400.0, value=0.0
        )
        Evaporation = st.number_input(
            "Evaporation", min_value=0, max_value=150, value=0
        )
        Sunshine = st.select_slider("Sunshine (UV)", options=[i for i in range(16)])
        WindGustSpeed = st.number_input("WindGustSpeed", min_value=6, max_value=150)
        WindSpeed9am = st.number_input(
            "Windspeed 9am", min_value=0, max_value=150, value=0
        )
        WindSpeed3pm = st.number_input(
            "Windspeed 3pm", min_value=0, max_value=150, value=0
        )
        Humidity9am = st.number_input(
            "Humidity 9am", min_value=0, max_value=100, value=0
        )
        Humidity3pm = st.number_input(
            "Humidity 3pm", min_value=0, max_value=100, value=0
        )
        Pressure9am = st.number_input(
            "Pressure 9am", min_value=900.0, max_value=1100.0, value=1000.0
        )
        Pressure3pm = st.number_input(
            "Pressure 3pm", min_value=900.0, max_value=1100.0, value=1000.0
        )
        Cloud9am = st.select_slider("Clouds at 9am", options=[i for i in range(11)])
        Cloud3pm = st.select_slider("Clouds at 3pm", options=[i for i in range(11)])
        Temp9am = st.number_input(
            "Temperature at 9am", min_value=-10, max_value=40, value=20
        )
        Temp3pm = st.number_input(
            "Temperature at 3pm", min_value=-10, max_value=50, value=20
        )
        WindDir9am = st.selectbox("Wind Direction at 9am", cat_values_dict["windDir"])
        WindDir3pm = st.selectbox("Wind Direction at 3pm", cat_values_dict["windDir"])

        if st.checkbox("Did it rain today?"):
            RainToday = "Yes"
        else:
            RainToday = "No"

        input_dict = dict(
            Location=Location,
            MinTemp=MinTemp,
            MaxTemp=MaxTemp,
            Rainfall=Rainfall,
            Evaporation=Evaporation,
            Sunshine=Sunshine,
            WindGustDir=WindGustDir,
            WindGustSpeed=WindGustSpeed,
            Pressure3pm=Pressure3pm,
            Pressure9am=Pressure9am,
            Cloud3pm=Cloud3pm,
            Cloud9am=Cloud9am,
            Temp3pm=Temp3pm,
            Temp9am=Temp9am,
            WindDir3pm=WindDir3pm,
            WindDir9am=WindDir9am,
            RainToday=RainToday,
            Humidity3pm=Humidity3pm,
            Humidity9am=Humidity9am,
            WindSpeed3pm=WindSpeed3pm,
            WindSpeed9am=WindSpeed9am,
        )

        input_df = pd.DataFrame([input_dict])

        if st.button("Predict"):
            output = predict(model=model, input_df=input_df)
            st.success("Does it rain tomorrow? {}".format(output[0]))

    if select_bar == "Batch":
        file_upload = st.file_uploader(
            "Upload a csv file for predictions", type=["csv"]
        )

        if file_upload is not None:
            data = pd.read_csv(file_upload)
            predictions = predict_model(estimator=model, data=data)
            st.write(predictions)


if __name__ == "__main__":
    run()
