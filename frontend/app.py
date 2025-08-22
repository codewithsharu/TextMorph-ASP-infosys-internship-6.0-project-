import streamlit as st
import requests

# Title of the app
st.title("Welcome to My Streamlit App")

# Fetch data from the backend
response = requests.get("http://127.0.0.1:8000/api/data")
data = response.json()

# Display the message from the backend
st.write(data["message"])

# Add a button
if st.button("Click Me"):
    st.write("Button clicked!")

# Add a slider
slider_value = st.slider("Select a value", 0, 100)
st.write(f"You selected: {slider_value}")