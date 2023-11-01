# rajashankar-phase-5
Below is a brief overview of what the code does:

The application uses the Flask framework for creating a web application.
It imports necessary modules such as Flask, render_template, request, jsonify, csv, Chat from nltk.chat.util, webbrowser, os, YouTube from pytube, re, and requests.
It defines API URLs and keys for weather data (WeatherStack) and news headlines (News API).
There are several functions defined to perform specific tasks:
get_bbc_news(): Fetches top headlines from BBC News API.
get_weather(city): Fetches current weather data for a given city using WeatherStack API.
sanitize_filename(title): Removes special characters from a string to make it suitable for use as a filename.
load_responses_from_csv(file_path): Loads responses from a CSV file into a list. Each response consists of a question and an associated answer.
The application initializes the Flask app, loads responses from a CSV file, and creates a chatbot object (chat) using the loaded responses.
It defines routes for the web application:
/: Renders the index.html template.
/get_response: Handles POST requests to get a response from the user input.


To Run the Code:

Ensure you have Python 3.x installed on your system.
Install the required dependencies using pip install Flask nltk pytube requests.
Clone or download the repository to your local machine.
Create a templates folder in the root directory if it doesn't exist.
Place your HTML templates (e.g., index.html) inside the templates folder.
Specify the location of your CSV file for chatbot responses in the app.py file.
In app.py:

Replace D:\demo\Conversation.csv with the actual path where your dataset is located.
Run the Flask application using the command python app.py.

Open a web browser and navigate to http://localhost:5000 to use the application.

Please make sure to have an active internet connection for fetching weather, news, and downloading videos.

If you have any specific questions or need further explanation about a specific part of the code, feel free to ask!
