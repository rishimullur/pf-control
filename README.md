# Should You Eat This?

A easy-to-use app that provides advice to help you make informed decisions about your food choices.

## Technologies Used

- Streamlit
- OpenAI API (GPT-4)
- Flask

### Written in python & uses several native libraries like matplotlib etc.

## Problem Statement

Making healthy food choices can be challenging, especially when trying to achieve specific health goals like weight loss or maintaining a balanced diet. This project aims to simplify the decision-making process by providing users with personalized dietary advice based on their health information and the food items they plan to consume.

## How to Run

1. Clone the repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Set up your OpenAI API key as an environment variable: `export OPENAI_API_KEY=your_api_key_here`
4. Run the Streamlit app: `streamlit run app.py`

## Reflections

### What I Learned

Through this project, I gained valuable experience in integrating various technologies and APIs to create a practical application. Some key learnings include:

- Utilizing computer vision and natural language processing techniques to analyze food images and extract relevant information.
- Developing a user-friendly interface with Streamlit to improve the overall experience.
- Implementing algorithms to calculate nutritional values and provide personalized dietary advice based on user inputs.
- Handling API requests and responses, as well as incorporating error handling and user feedback mechanisms.

### What Questions/Problems Did I Face?

1. **Accuracy of Food Item Detection**: Ensuring accurate detection and classification of food items in images can be challenging, especially with complex dishes or obscured items.

2. **Handling Edge Cases**: Accounting for various edge cases, such as incomplete or invalid user inputs, required additional error handling and input validation mechanisms.

3. **Integrating Multiple APIs**: Combining the functionality of different APIs (e.g., OpenAI, computer vision APIs) required careful coordination and data handling to ensure a seamless user experience.

4. **Performance Optimization**: Processing images and performing computations can be resource-intensive, necessitating strategies for optimizing performance and reducing latency.

5. **Continuous Learning and Adaptation**: As dietary recommendations and nutritional guidelines evolve, maintaining and updating the application's knowledge base becomes crucial for providing accurate and up-to-date advice.

Despite these challenges, working on this project has been an invaluable learning experience, reinforcing the importance of attention to detail, thorough testing, and continuous iteration to create a robust and user-friendly application.
