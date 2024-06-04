import streamlit as st
import base64, os
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Key
api_key = os.getenv('OPENAI_API_KEY')

# Ensure the API key is available
if not api_key:
    st.error("OpenAI API key not found. Please set it in your environment variables.")
    st.stop()

# Function to encode the image
def encode_image(image_file):
    return base64.b64encode(image_file.getvalue()).decode('utf-8')

# Streamlit interface with fancy UI elements
st.set_page_config(page_title="Should You Eat This?", page_icon=":fork_and_knife:", layout="centered", initial_sidebar_state="expanded")

# Custom CSS styles
st.markdown("""
    <style>
    .stProgress .st-ah {
        background-color: #00BF63;
    }
    .stProgress .st-ah:after {
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit app with fancy UI elements
with st.sidebar:
    st.title(":fork_and_knife: Should You Eat This?")

st.title("Enter your health details")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Enter your age", min_value=0, max_value=130, step=1, help="Your current age in years.")
    height = st.number_input("Enter your height (in cm)", min_value=0.0, format="%.2f", help="Your height in centimeters.")
with col2:
    weight = st.number_input("Enter your weight (in kg)", min_value=0.0, format="%.2f", help="Your current weight in kilograms.")
    target_weight = st.number_input("Enter your target weight (in kg)", min_value=0.0, format="%.2f", help="Your desired weight goal in kilograms.")
time_plan = st.number_input("Enter your time plan to reach target weight (in months)", min_value=0.0, format="%.2f", help="The duration in months to achieve your target weight.")

# Check if all health details are filled
if age == 0 or height == 0.0 or weight == 0.0 or target_weight == 0.0 or time_plan == 0.0:
    st.error("Please fill in all your health details.")
else:
    # Streamlit interface for file upload and title for planning to eat
    st.subheader("What are you planning to eat today?")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], help="Upload an image of the food you plan to eat.")
    if uploaded_file is not None:
        # Display the image
        st.image(uploaded_file, caption='Uploaded Image.', use_column_width=True)
        st.write("")

        # Getting the base64 string
        base64_image = encode_image(uploaded_file)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {api_key}"
        }

        # Initialize a fancy loader
        with st.spinner("Analyzing your food image..."):
            # First payload to get food items from the image
            first_payload = {
              "model": "gpt-4o",
              "messages": [
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "text",
                      "text": "What are the food items present in the image? Describe each food item(s) in 4-5 words."
                    },
                    {
                      "type": "image_url",
                      "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                      }
                    }
                  ]
                }
              ],
              "max_tokens": 300
            }

            # Send the first request
            response = requests.post("https://openai.ianchen.io/v1/chat/completions", headers=headers, json=first_payload)

            # Extracting the content from the first response
            first_response_content = response.json()['choices'][0]['message']['content']

# Correct usage of st.success with a single argument
            st.success(f"Detected food items: {first_response_content}")

            # Assuming the response content is a string that lists food items separated by commas
            food_items = first_response_content.split(', ')

            # Combine the second and third prompts into one
            combined_prompt = f"Imagine you are an expert dietitian. Given my age ({age}), height ({height} cm), current weight ({weight} kg), target weight ({target_weight} kg), and my time plan ({time_plan} months), list down the approximate calories and the glycemic index for the following food items: {', '.join(food_items)}. Also, can I eat these food items and still meet my daily calorie goal?"

            # New payload for the combined request
            combined_payload = {
              "model": "gpt-4o",
              "messages": [
                {
                  "role": "user",
                  "content": combined_prompt
                }
              ],
              "max_tokens": 1000
            }

            # Send the combined request
            combined_response = requests.post("https://openai.ianchen.io/v1/chat/completions", headers=headers, json=combined_payload)

            # Extracting the content from the combined response
            combined_response_content = combined_response.json()['choices'][0]['message']['content']

            # Display the nutritional information and dietary advice on Streamlit
            st.info(f"Nutritional Information and Dietary Advice: {combined_response_content}")
            print(combined_response_content)

        # Display a success message
        st.success("Analysis complete! :thumbsup:")

        # Add a call-to-action button
        if st.button("Analyze Another Food Item"):
            st.experimental_rerun()

# Add a footer
st.markdown("""
    <footer style="text-align: center; font-size: 12px; margin-top: 40px;">
        <p>Made with <3 by <a href="https://rishim.xyz" target="_blank">Rishi</a></p>
    </footer>
""", unsafe_allow_html=True)