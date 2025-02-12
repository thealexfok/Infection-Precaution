import streamlit as st
import pandas as pd
from fuzzywuzzy import process
from PIL import Image
import os

im = Image.open("favicon.ico")
st.set_page_config(
    page_title="Infection Dictionary",
    page_icon=im,
)

# Load the data with caching to avoid reloading on every interaction
@st.cache_data
def load_data():
    data = pd.read_csv("infection_data.csv")
    # Get the last modified time of the data file
    last_updated = os.path.getmtime("infection_data.csv")
    return data, last_updated

data, last_updated = load_data()

# Remove rows where 'Infection/Condition' is NaN
data = data.dropna(subset=['Infection/Condition'])


# Sort the infection conditions alphabetically
all_conditions = sorted(data['Infection/Condition'].unique().tolist())

# App layout
st.image("logo.png")
st.title("Infection Precautions Dictionary")
st.caption(f"Last updated: {pd.to_datetime(last_updated, unit='s').strftime('%Y-%m-%d')}")
st.write("Select an infection or condition to view recommended isolation precautions.")

# Create a select box with dynamic filtering
selected_infection = st.selectbox("Type to search for an infection/condition:", options=[""] + all_conditions)

# Display selected option details if an infection is selected
if selected_infection:
    filtered_data = data[data['Infection/Condition'] == selected_infection]
    st.write("### Search Results")
    
    # Display the filtered data without any row ID
    st.table(filtered_data[['Infection/Condition', 'Type of Precaution', 'Duration of Precaution', 'Precautions/Comments']])
else:
    st.warning("Please select an infection name from the dropdown.")

# Expandable section to view all data, excluding "Data ID"
with st.expander("View all infections"):
    # Display all data without any row ID
    st.dataframe(data[['Infection/Condition', 'Type of Precaution', 'Duration of Precaution', 'Precautions/Comments']])

st.divider()
st.write("Data sourced from \n\n https://www.cdc.gov/infection-control/hcp/isolation-precautions/appendix-a-type-duration.html")

st.divider()
footer_html = """<div style='text-align: center;'>
  <p>Developed with ❤️ in St. Helena</p>
</div>"""
st.markdown(footer_html, unsafe_allow_html=True)