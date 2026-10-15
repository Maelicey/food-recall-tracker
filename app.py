import streamlit as st
import pandas as pd

st.title("Food Recall Tracker")

df = pd.read_csv("recalls_app.csv")

st.write("Total recalled products:", len(df))
