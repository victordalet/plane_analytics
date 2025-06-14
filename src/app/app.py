import streamlit as st
import tensorflow as tf
from typing import Optional
import pandas as pd
import numpy as np


NUMBER_BEST_TO_DISPLAY = 5


class App:
    def __init__(self, model_path):
        self.model: Optional[tf.keras.Model] = self.load_model(model_path)

    @staticmethod
    def load_model(model_path: str):
        try:
            return tf.keras.models.load_model(model_path)
        except Exception as e:
            return None

    def render_form(self):
        airports_csv = pd.read_csv("docker/data/airports.csv")
        with st.form("prediction_form"):
            start_city = st.selectbox(
                "Start City",
                options=airports_csv["IATA_CODE"],
                format_func=lambda code: airports_csv.loc[
                    airports_csv["IATA_CODE"] == code, "AIRPORT"
                ].values[0],
            )
            end_city = st.selectbox(
                "End City",
                options=airports_csv["IATA_CODE"],
                format_func=lambda code: airports_csv.loc[
                    airports_csv["IATA_CODE"] == code, "AIRPORT"
                ].values[0],
            )
            submitted = st.form_submit_button("Submit")

            if submitted:
                self.make_prediction(start_city, end_city)

    def make_prediction(self, start_city, end_city):
        if not self.model:
            st.error("Model not loaded.")
            return

        try:
            airline_csv = pd.read_csv("docker/data/airlines.csv")

            prediction = pd.DataFrame(
                columns=[
                    "DIVERTED",
                    "CANCELLED",
                    "ARRIVAL_DELAY",
                    "DEPARTURE_DELAY",
                    "SCORE",
                    "AIRLINE",
                ]
            )
            for airline in airline_csv["IATA_CODE"]:
                x_col = [start_city, end_city, airline]
                for i in range(len(x_col)):
                    x_col[i] = sum([ord(c) for c in x_col[i]])

                r = self.model.predict(np.array([x_col]))

                prediction.loc[len(prediction)] = {
                    "DIVERTED": r[0][0],
                    "CANCELLED": r[0][1],
                    "ARRIVAL_DELAY": r[0][2],
                    "DEPARTURE_DELAY": r[0][3],
                    "SCORE": r[0][0] + r[0][1] + r[0][2] + r[0][3],
                    "AIRLINE": airline_csv[airline_csv["IATA_CODE"] == airline][
                        "AIRLINE"
                    ].values[0],
                }
            st.success(f"Best airline :")
            table_best_airline = prediction.sort_values(
                by="SCORE", ascending=False
            ).head(NUMBER_BEST_TO_DISPLAY)

            st.table(table_best_airline["AIRLINE"].reset_index(drop=True))

        except Exception as e:
            st.error(f"Error : {e}")


if __name__ == "__main__":
    app = App("./model.keras")
    app.render_form()
