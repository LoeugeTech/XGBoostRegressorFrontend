import streamlit as st
import requests
import os
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# Get the BASE_URL from the invironment variables
base_url = os.getenv("BASE_URL", "http://localhost:8000")
# Set page configuration
st.set_page_config(
    page_title="Insurance Charges Prediction",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state = "expanded",
)

# Add a title and description
st.markdown(
    """
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 20px;
        border-radium: 10px;
    }
    .title {
        font-size: 30px;
        font-weight: bold;
        color: #4CAF50;
    }
    .subtitle {
        font-size: 16px;
        color: #555;
        margin-button: 20px;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #777;
        margin-top: 50px;
    }
    </style>
    <div class="main">
        <h1 class="title">💸 Insurance Charges Prediction</h1>
        <p class= "subtitle">Easily Predict insurance charges based on user details
        Fill out the form below!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Fetch metadata from FastAPI
def fetch_entities(endpoint):
    try:
        result = requests.get(f"{base_url}/api/entities/{endpoint}")
        if result.status_code == 200:
            return result.json()
        else:
            st.error(f"❌ Error: Could not fetch {endpoint} entities. Please check the API service.")
            return None
    except Exception as e:
        st.error(f"❌ Error: {e}")
        return None


sex_entities = fetch_entities("sex")
smoker_entities = fetch_entities("smoker")
region_entities = fetch_entities("region")

# User Inputs
with st.form("user_input_form"):
    st.write("### User Details")

    age = st.number_input("👱‍♂️ Age:", min_value=0, max_value=120, value=30, step=1)

    # sex input
    if sex_entities:
        sex_options = [item['label'] for item in sex_entities['sex']]
        sex = st.radio("👬 Sex:", sex_options, horizontal=True)
        sex = next(item['value'] for item in sex_entities['sex'] if item['label'] == sex)

    bmi = st.number_input("⚖️ BMI (Body Mass Index:", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
    children = st.slider("👶 Number of Children:", min_value=0, max_value=10, value=0, step=1)

    # smoker input
    if smoker_entities:
        smoker_options = [item['label'] for item in smoker_entities['smoker']]
        smoker = st.radio("👫 Smoker:", smoker_options, horizontal=True)
        smoker = next(item['value'] for item in smoker_entities['smoker'] if item['label'] == smoker)

    # region input
    if region_entities:
        region_options = [item['label'] for item in region_entities['region']]
        region = st.selectbox("📍 Region:", region_options)

        northwest, southeast, southwest = 0, 0, 0
        if region == "Northwest":
            northwest = 1
        elif region == "Southeast":
            southeast = 1
        elif region == "Southwest":
            southwest = 1

    # Submit button
    submitted = st.form_submit_button("Predict 🚀")


if submitted:
    # Make API request
    api_url = f"{base_url}/api/predict"
    data = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "northwest": northwest,
        "southeast": southeast,
        "southwest": southwest
    }
    with st.spinner("Fetching prediction..."):
        response = requests.post(api_url, json=data)

    if response.status_code == 200:
        prediction = response.json()["predicted_charges"]
        st.success(f"💵 Predicted Insurance Charges: **${prediction:.2f}**")
        st.balloons()
    else:
        st.error("❌ Error: Could not fetch prediction. Please check the API services")

    # Footer
    st.markdown(
        """
        <div class="footer">
            Made with ❤️‍ using Streamlit.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Run the Streamlit App
    # streamlit run app.py

