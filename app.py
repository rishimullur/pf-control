import streamlit as st
import base64, os
import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from pathlib import Path

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
css = Path("style.css").read_text()
st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    # st.image("logo.png", use_column_width=True)
    st.title(":fork_and_knife: Should You Eat This?")
    st.markdown("---")

# Main content
st.title(":fork_and_knife: Add your health information")
col1, col2 = st.columns(2)
with col1:
    age = st.number_input("📅 Enter your age", min_value=0, max_value=130, step=1, help="Your current age in years.")
    height = st.number_input("📏 Enter your height (in cm)", min_value=0.0, format="%.2f", help="Your height in centimeters.")
with col2:
    weight = st.number_input("⚖️ Enter your weight (in kg)", min_value=0.0, format="%.2f", help="Your current weight in kilograms.")
    target_weight = st.number_input("🎯 Enter your target weight (in kg)", min_value=0.0, format="%.2f", help="Your desired weight goal in kilograms.")
time_plan = st.number_input("🕰️ Enter your time plan to reach target weight (in months)", min_value=0.0, format="%.2f", help="The duration in months to achieve your target weight.")

# Function to calculate BMR using the Harris-Benedict equation
# Assuming the user is male. For female, the formula will be different.
def calculate_bmr(age, weight, height):
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    return bmr

# Function to calculate daily caloric needs to maintain current weight
def maintenance_calories(bmr, activity_level='sedentary'):
    # Multiplier for different activity levels could be added here
    return bmr * 1.2  # Assuming sedentary lifestyle for simplicity

# Function to calculate caloric deficit
def calculate_caloric_deficit(weight, target_weight, time_plan):
    # 1 kg of body weight is roughly equivalent to 7700 calories
    total_calories_to_lose = (weight - target_weight) * 7700
    daily_caloric_deficit = total_calories_to_lose / (time_plan * 30)  # Assuming 30 days in a month
    return daily_caloric_deficit

# Check if all health details are filled and valid for calculation
if age > 0 and height > 0.0 and weight > 0.0 and target_weight > 0.0 and time_plan > 0.0:
    # Calculate BMR
    bmr = calculate_bmr(age, weight, height)

    # Calculate maintenance calories
    maintenance_calories_value = maintenance_calories(bmr)

    # Calculate caloric deficit
    caloric_deficit = calculate_caloric_deficit(weight, target_weight, time_plan)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    labels = ['BMR', 'Maintenance Calories', 'Caloric Deficit']
    values = [bmr, maintenance_calories_value, maintenance_calories_value - caloric_deficit]

    bars = ax.bar(labels, values, color=['#4285F4', '#34A853', '#EA4335'])

    # Adding value labels on bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom', fontweight='bold')

    # Set labels and title
    ax.set_ylabel('Calories', fontweight='bold')
    ax.set_title('BMR & Caloric Deficit Chart', fontweight='bold', fontsize=16)
    ax.tick_params(axis='x', labelrotation=45)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(color='#EEEEEE', linestyle='--')

    # Display the chart in Streamlit
    st.subheader("🔢 Your BMR and Caloric Deficit")
    st.pyplot(fig)
# else:
#     st.error("Please fill in all your health details to calculate BMR and caloric deficit.")

# Check if all health details are filled
if age == 0 or height == 0.0 or weight == 0.0 or target_weight == 0.0 or time_plan == 0.0:
    st.error("Please fill in all your health details.")
else:
    # Streamlit interface for file upload and title for planning to eat
    st.subheader("🍽️ What are you planning to eat today?")
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
            if response.status_code == 200:

                    # Extracting the content from the first response
                    first_response_content = response.json()['choices'][0]['message']['content']

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

                    # Display a success message
                    st.success(f"Analysis complete! :thumbsup:")

                    # Add a call-to-action button
                    if st.button("Analyze Another Food Item"):
                        st.experimental_rerun()

            else:
                st.error("Failed to get a response from the server.")

# Add a footer
st.markdown("""
    <footer style="text-align: center; font-size: 12px; margin-top: 40px; background-color: #0E0B24; padding: 10px;">
        <p>Made with <span style="color: #4285F4;">&hearts;</span> by <a href="https://rishim.xyz" target="_blank" style="color: #4285F4;">Rishi</a></p>
    </footer>
""", unsafe_allow_html=True)
