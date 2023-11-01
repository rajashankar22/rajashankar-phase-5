from flask import Flask, render_template, request, jsonify
import csv
from nltk.chat.util import Chat
import webbrowser
import os
from pytube import YouTube
import re
import requests

app = Flask(__name__)
WEATHERSTACK_API_URL = 'http://api.weatherstack.com/current'
WEATHERSTACK_API_KEY = '32b87d435e38142f7737f294a813e253'
NEWS_API_KEY = '88992b7570a34efa8a2b502530eb684c'  

def get_bbc_news():
    url = f'https://newsapi.org/v2/top-headlines'
    params = {
        'sources': 'bbc-news',
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        news_data = response.json()
        articles = news_data['articles'][:5] 
        headlines = [article['title'] for article in articles]
        return headlines
    else:
        return None
def get_weather(city):
    params = {
        'access_key': WEATHERSTACK_API_KEY,
        'query': city
    }

    response = requests.get(WEATHERSTACK_API_URL, params=params)

    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        return None

def sanitize_filename(title):
    return re.sub(r'[^\w\s]', '', title)

def load_responses_from_csv(file_path):
    responses = []

    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if len(row) == 2:
                question, answer = row
                responses.append([rf"{question}", [f"Hina: {answer}"]])
            else:
                print(f"Skipping invalid row: {row}")

    return responses

if __name__ == "__main__":
    responses = load_responses_from_csv('D:\demo\Conversation.csv')
    if not responses:
        print("No valid responses found. Please check your dataset.")
    else:
        chat = Chat(responses)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_response', methods=['POST'])
    def get_response():
        user_input = request.form['user_input']

        if user_input.lower() == 'open youtube':
            response = "opening youtube"
            webbrowser.open('https://www.youtube.com')
        elif user_input.lower() == 'open google':
            response = "opening google"
            webbrowser.open('https://www.google.com')
        elif user_input.startswith('download video '):
            video_url = user_input[15:] 
            try:
                yt = YouTube(video_url)
                stream = yt.streams.get_highest_resolution()
                output_path = os.path.join('downloads', f'{sanitize_filename(yt.title)}.mp4')


                stream.download(output_path=output_path)

                response = f"Downloaded video: {yt.title}"
            except Exception as e:
                response = f"Error: {e}"
        elif user_input.lower() == 'get news':
            news_headlines = get_bbc_news()
            if news_headlines:
                response = "Here are the latest BBC News headlines:\n\n" + "\n".join(news_headlines)
            else:
                response = "Sorry, I couldn't fetch the news headlines at the moment. Please try again later."
        elif user_input.startswith('weather in '):
            city = user_input[11:]  
            weather_data = get_weather(city)
            if weather_data and 'current' in weather_data:
                temperature = weather_data['current']['temperature']
                description = weather_data['current']['weather_descriptions'][0]
                response = f"The current temperature in {city} is {temperature}°C with {description}."
            else:
                response = "Sorry, I couldn't fetch the weather information at the moment. Please try again later."
        else:
            response = chat.respond(user_input)

        return jsonify({'response': response})

    app.run(debug=True)
