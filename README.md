# Should You Eat This?

An easy-to-use app that provides advice to help you make informed decisions about your food choices.

## Technologies Used

- Streamlit
- OpenAI API (GPT-4)
- Flask

### Written in Python & uses several native libraries like matplotlib etc.

## Problem Statement

Making healthy food choices can be challenging, especially when trying to achieve specific health goals like weight loss or maintaining a balanced diet. This project aims to simplify the decision-making process by providing users with personalized dietary advice based on their health information and the food items they plan to consume via taking and uploading a simple picture of what they plan to eat.

## How to Run

1. Clone the repository
2. Install the required dependencies: `pip3 install -r requirements.txt`
3. Set up your OpenAI API key as an environment variable via a .env  file or via the command `export OPENAI_API_KEY=your_api_key_here`
4. Also add the base URL for the openai API usage via the .env file or via the command `export OPENAI_ENDPOINT=your_base_url`
5. Run the Streamlit app: `streamlit run app.py`
6. Additionally to expose the local API, run `python3 server.py`
7. Now you can add user inputs. The local API can be found and available via CLI: `curl http://localhost:5000/get_health_details/<user_id>`

## Reflections

### What I Learned

Through this project, I gained valuable experience in integrating various technologies and APIs to create a practical application. Some key learnings include:

- Utilizing computer vision and natural language processing via large language models to analyze food images and extract relevant information.
- Developing a user-friendly interface with Streamlit to improve the overall experience.
- Implementing algorithms to calculate nutritional values and provide personalized dietary advice based on user inputs and visualizing this data.
- Handling API requests and responses, as well as incorporating error handling and user feedback mechanisms.

### What Questions/Problems Did I Face?

1. **Integrating Multiple APIs**: Combining the functionality of different APIs (e.g., OpenAI, computer vision APIs) required careful coordination and data handling to ensure a seamless user experience.

2. **Local storage**: As dietary recommendations and nutritional guidelines evolve, maintaining and updating the application's knowledge base becomes crucial for providing accurate and up-to-date advice via storage of user data.

3. **Handling Edge Cases**: Accounting for various edge cases, such as incomplete or invalid user inputs, required additional error handling and input validation mechanisms.

Despite these challenges, working on this project has been a learning experience, reinforcing the importance of attention to detail, thorough testing, and continuous iteration to create a robust and user-friendly application.


### In case you find issues while running

1. After I upload an image on streamlit, an error with `Failed to get a response from the server.` or a similar error is shown.
Ans: Your openai key is either revoked or expired. Use a new key and add it as an environment variable either in streamlit env runtime or as a variable if running locally.

2. What is a base-URL for Openai?
Ans: The project was built based on a different custom URL provided with credits for a class project work. For normal usage, please use the base api url from openai documentation. For 510 analysis, use base URL provided by the Instructor to successfully execute the commands.
