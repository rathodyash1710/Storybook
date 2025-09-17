import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(page_title="Storybook Creator", page_icon="📚")

st.title("📚 Adaptive Storybook Creator")

age = st.number_input("Child's Age", min_value=1, max_value=15)
reading_level = st.selectbox("Reading Level", ["Beginner", "Intermediate", "Advanced"])
theme = st.text_input("Favorite Theme (e.g., Space, Animals, Magic)", "Animals")
gender   = st.selectbox("gender", ["Male", "Female"])
description = st.text_area("Additional Preferences(A story about a brave little lion)(optional)","")

if st.button("Generate Storybook"):
    with st.spinner("Creating your personalized story..."):
        payload = {"age": age, "reading_level": reading_level, "theme": theme,"gender":gender,"description":description}
        try:
            response = requests.post(f"{API_BASE}/generate_story/", json=payload)
            #response ="hey"
            if response.status_code == 200:
                story_data = response.json()
                st.markdown(response.json()["markdown_story"], unsafe_allow_html=True)
            else:
                st.error("Error generating story. Please try again.")
        except Exception as e:
            st.error(f"Backend not reachable: {e}")
