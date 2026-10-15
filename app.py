import streamlit as st
import pandas as pd

st.title("Food Recall Tracker")

df = pd.read_csv("recalls_app.csv")

st.write("Total recalled products:", len(df))

search = st.text_input("Search for a product or company")

if search:
    in_product = df["product_description"].str.contains(search, case=False, na=False)
    in_company = df["recalling_firm"].str.contains(search, case=False, na=False)
    results = df[in_product | in_company]
    results = df[df["product_description"].str.contains(search, case=False, na=False)]
    results = results.sort_values("report_date", ascending=False)
    st.write("Matching products:", len(results))

    st.dataframe(results)

    
