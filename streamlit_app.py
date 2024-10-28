import streamlit as st
import pandas as pd
from fuzzywuzzy import process

# Load the data with caching to avoid reloading on every interaction
@st.cache_data
def load_data():
    return pd.read_csv("infection_data.csv")

data = load_data()

# Helper function for fuzzy matching
def fuzzy_search(query, choices, limit=5, threshold=70):
    results = process.extract(query, choices, limit=limit)
    return [choice for choice, score in results if score >= threshold]

# App layout
st.image("logo.png")
st.title("Infection Precautions Dictionary")
st.write("Search for an infection or condition to view recommended isolation precautions.")

# Real-time search input without modifying session state directly
search_input = st.text_input("Search for an infection or condition", value="")

# Real-time filtering based on fuzzy matching
if search_input:
    # Perform fuzzy matching on the "Infection/Condition" column
    matches = fuzzy_search(search_input, data['Infection/Condition'].tolist())
    
    if matches:
        # Filter data to show only matching results
        filtered_data = data[data['Infection/Condition'].isin(matches)]
        st.write("### Search Results")
        st.table(filtered_data[['Infection/Condition', 'Type of Precaution', 'Duration of Precaution', 'Precautions/Comments']])
    else:
        st.write("No matching infections found.")
else:
    st.write("Please enter an infection name to search.")

# Expandable section to view all data
with st.expander("View all infections"):
    st.table(data[['Infection/Condition', 'Type of Precaution', 'Duration of Precaution', 'Precautions/Comments']])

st.write("Data sourced from \n\n https://www.cdc.gov/infection-control/hcp/isolation-precautions/appendix-a-type-duration.html")
