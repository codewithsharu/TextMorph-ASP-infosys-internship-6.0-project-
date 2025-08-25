import streamlit as st
import requests

st.title("Register User")

# Registration form
with st.form("register_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    submit = st.form_submit_button("Register")

if submit:
    if not username or not email or not password:
        st.error("Please fill in all fields.")
    else:
        # Send username, email, and password in payload
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        try:
            response = requests.post("http://127.0.0.1:5000/register", json=payload)
            data = response.json()
            if response.ok:
                st.success(data.get("message", "Registration successful!"))
            else:
                st.error(data.get("message", "Registration failed."))
        except Exception as e:
            st.error(f"Error: {e}")