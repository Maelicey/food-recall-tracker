import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")


st.title("Food Recall Tracker")
display_columns = ["report_date", "product_description", "recalling_firm", "reason_for_recall", "classification", "status"]

df = pd.read_csv("recalls_app.csv")

df["year"] = pd.to_datetime(df["report_date"]).dt.year
                            
st.write("Total recalled products:", len(df))

tab1, tab2 = st.tabs(["Search", "Analytics"])

with tab1:
    search = st.text_input("Search for a product, company, or reason")
    class_choice = st.selectbox("Classification", ["All", "Class I", "Class II", "Class III"])
    st.caption("Class I: most serious risk. Class II: temporary or reversible health risk. Class III: unlikely to cause health problems.")


    if search:
        in_product = df["product_description"].str.contains(search, case=False, na=False)
        in_company = df["recalling_firm"].str.contains(search, case=False, na=False)
        in_reason = df["reason_for_recall"].str.contains(search, case=False, na=False)
        results = df[in_product | in_company | in_reason]
        if class_choice != "All":
            results = results[results["classification"] == class_choice]
        results = results.sort_values("report_date", ascending=False)
        st.write("Matching products:", len(results))
        nice_names = {
            "report_date": "Report date",
            "product_description": "Product description",
            "recalling_firm": "Company",
            "reason_for_recall": "Reason for recall",
            "classification": "Class",
            "status": "Status",
        }
        st.dataframe(results[display_columns].rename(columns=nice_names), hide_index=True)

with tab2:
    st.header("Recalls by year")
    products_per_year = df["year"].value_counts().sort_index()
    st.bar_chart(products_per_year)
    st.caption("The chart counts recalled products per year. 2026 includes data up to October.")

    st.header("Recalls by classification")
    products_per_class = df["classification"].value_counts()
    st.bar_chart(products_per_class)
    st.caption("The chart counts recalled products per class.")

    st.header("Most common recall reasons")
    products_per_reason = df["reason_category"].value_counts()
    st.bar_chart(products_per_reason)
    st.caption("The chart shows the reason for recall. Categories are based on keywords in the recall reason. 'Other' means no keyword matched.")

    st.header("Companies with the most recall events")
    events_per_company = df.groupby("recalling_firm")["event_id"].nunique().sort_values(ascending=False).head(10)
    st.bar_chart(events_per_company)
    st.caption("The chart shows recall events. Company names may vary (Whole Foods / WFM). Big companies sell more products.")

st.caption("Data source: FDA openFDA food enforcement reports (snapshot from October 2026). This app is not an official FDA source, and the data may not be complete or up to date. Please check the official FDA website for current recall information.")











