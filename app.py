import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")


st.title("Food Recall Tracker")
display_columns = ["report_date", "product_description", "recalling_firm", "reason_for_recall", "classification", "status"]

df = pd.read_csv("recalls_app.csv")

st.write("Total recalled products:", len(df))

search = st.text_input("Search for a product or company")
class_choice = st.selectbox("Classification", ["All", "Class I", "Class II", "Class III"])

if search:
    in_product = df["product_description"].str.contains(search, case=False, na=False)
    in_company = df["recalling_firm"].str.contains(search, case=False, na=False)
    results = df[in_product | in_company]
    if class_choice != "All":
        results = results[results["classification"] == class_choice]
    results = results.sort_values("report_date", ascending=False)
    st.write("Matching products:", len(results))

    st.dataframe(results[display_columns], hide_index=True)

    
