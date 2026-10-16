import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")


st.title("Food Recall Tracker")
display_columns = ["report_date", "product_description", "recalling_firm", "reason_for_recall", "classification", "status"]

df = pd.read_csv("recalls_app.csv")

df["year"] = pd.to_datetime(df["report_date"]).dt.year
                            
st.write("Total recalled products:", len(df))

search = st.text_input("Search for a product or company, or reason")
class_choice = st.selectbox("Classification", ["All", "Class I", "Class II", "Class III"])

if search:
    in_product = df["product_description"].str.contains(search, case=False, na=False)
    in_company = df["recalling_firm"].str.contains(search, case=False, na=False)
    in_reason = df["reason_for_recall"].str.contains(search, case=False, na=False)
    results = df[in_product | in_company | in_reason]
    if class_choice != "All":
        results = results[results["classification"] == class_choice]
    results = results.sort_values("report_date", ascending=False)
    st.write("Matching products:", len(results))

    st.dataframe(results[display_columns], hide_index=True)

st.header("Recall Trends by Year")
products_per_year = df["year"].value_counts().sort_index()
st. bar_chart(products_per_year)
st.caption("The chart counts recalled products per year. 2026 includes data up to October.")

st.header("Recall by Classification")
products_per_class = df["classification"].value_counts().sort_index()
st.bar_chart(products_per_class)
st.caption("The chart counts recalled products per Class.")

st.header("Recall by Common Reasons")
products_per_category = df["reason_category"].value_counts().sort_index()
st.bar_chart(products_per_category)
st.caption("The chart shows the reason for recall. Categories are based on keywords in the recall reason. 'Other' means no keyword matched.")

st.header("Companies with the most recalls")
events_per_company = df.groupby("recalling_firm")["event_id"].nunique().sort_values(ascending=False).head(10)
st.bar_chart(events_per_company)
st.caption("The chart shows the recall events. Company names may vary (Whole Foods/ WFM). Big companies sell more products.")

st.caption("Data source: FDA openFDA food enforcement reports (snapshot from October 2026). This app is not an official FDA source, and the data may not be complete or up to date. Please check the official FDA website for current recall information.")
