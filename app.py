import streamlit as st
import pandas as pd

st.title("Food Recall Tracker")

df = pd.read_csv("recalls_app.csv")

st.write("Total recalled products:", len(df))

search = st.text_input("Search for a product or company")

if search:
    results = df[df["product_description"].str.contains(search, case=False, na=False)]
    st.write("Matching products:", len(results))
