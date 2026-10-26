# food-recall-tracker


A public web app to search and explore U.S. food recalls, built on the FDA's openFDA data.

**Live app:** https://food-recall-tracker.streamlit.app

## Overview

The Food Recall Tracker lets anyone search about 29,000 recalled food products reported by the FDA since 2012. Users can search by product, company, or recall reason, filter by severity, and explore recall trends through charts.

## Features

- **Search** by product, company, or reason, with newest recalls first
- **Filter** by recall classification (Class I, II, III)
- **Analytics:** recalls by year, by classification, by reason, and companies with the most recall events

## Recall classifications

The FDA classifies each recall by how serious the health risk is:

| Class | Meaning | Example |
|---|---|---|
| **Class I** | Most serious: the product could cause serious health problems or death | Listeria contamination, undeclared peanut |
| **Class II** | The product could cause temporary or reversible health problems; serious harm is unlikely | Some foreign material, like small plastic pieces |
| **Class III** | Unlikely to cause any health problems | Labeling errors, like a wrong net weight |

## How I built it

1. **Data collection (Python):** downloaded the full food enforcement dataset from openFDA's bulk download, and validated the record count against the API total.
2. **Cleaning (pandas):** selected 10 relevant fields, converted dates, and checked for missing values, empty strings, and duplicates.
3. **Analysis (SQL in BigQuery):** analyzed trends by year and grouped free-text recall reasons into categories using keyword rules (`CASE` + `LIKE`).
4. **App (Streamlit):** built a search and analytics app, deployed on Streamlit Community Cloud.

**Tools:** Python, pandas, SQL, Google BigQuery, Streamlit, GitHub

## Repository files

- `01_get_recall_data-2.ipynb`: data collection and cleaning (Python)
- `analysis.sql`: SQL analysis in BigQuery
- `app.py`: Streamlit app
- `recalls_app.csv`: app data, with reason categories
  
## Key findings

- **Listeria** is the most common reason for Class I recalls (the most serious category), followed by **Salmonella** and **undeclared allergens**.
- **2017** had the most recalled products, but fewer recall events than 2016: the peak came from larger recall events, not more of them.
- Nearly **half** of recalled products are Class I.
- Grocery chains lead in recall events, which reflects their size and product range rather than lower safety.

## Limitations

- **Products vs. events:** each record is one recalled product; one recall event can include many products.
- **Reason categories** are keyword-based; recalls with no matching keyword are labeled "other."
- **Company names** are not standardized (e.g., "Whole Foods Market" and "WFM Purchasing, LP").
- **Static snapshot:** data is from October 2026 and is not updated automatically. 2026 is a partial year.

## Next steps

- Automatic data updates
- Canada's CFIA recalls, in French and English

## Disclaimer

This app is not an official FDA source. Data may be incomplete or out of date. Always check [fda.gov](https://www.fda.gov) for current recall information.

## Data source

[openFDA Food Enforcement Reports](https://open.fda.gov/apis/food/enforcement/)
