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
            submitted = st.form_submit_button("Submit")

            if submitted:
                self.make_prediction(
                    start_city, end_city
                )

    def make_prediction(
        self, start_city, end_city
    ):
        if not self.model:
            st.error("Model not loaded.")
            return

        try:
            prediction = self.model.predict(
                [
                    start_city,
                    end_city
                ]
            )
            st.success(f"Go to : {prediction}")
        except Exception as e:
            st.error(f"Error : {e}")


if __name__ == "__main__":
    app = App("path/to/your/model.h5")
    app.render_form()
