import streamlit as st
import tensorflow as tf
from datetime import datetime
from typing import Optional


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
        with st.form("prediction_form"):
            start_city = st.text_input("Start City")
            end_city = st.text_input("End City")
            start_date = st.date_input("Start Date")
            start_time = st.time_input("Start Time")
            end_date = st.date_input("End Date")
            end_time = st.time_input("End Time")
            submitted = st.form_submit_button("Submit")

            if submitted:
                self.make_prediction(
                    start_city, end_city, start_date, start_time, end_date, end_time
                )

    def make_prediction(
        self, start_city, end_city, start_date, start_time, end_date, end_time
    ):
        if not self.model:
            st.error("Model not loaded.")
            return

        try:
            prediction = self.model.predict(
                [
                    start_city,
                    end_city,
                    datetime.combine(start_date, start_time),
                    datetime.combine(end_date, end_time),
                ]
            )
            st.success(f"Go to : {prediction}")
        except Exception as e:
            st.error(f"Error : {e}")


if __name__ == "__main__":
    app = App("path/to/your/model.h5")
    app.render_form()
