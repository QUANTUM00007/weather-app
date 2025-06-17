import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)


API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])

def index():
    weather = {}
    if request.method == "POST":
        city = request.form.get("city")  # Use .get to avoid crash
        if city:  # Ensure city is not empty
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": city.title(),
                    "temperature": data["main"]["temp"],
                    "description": data["weather"][0]["description"].title(),
                    "icon": data["weather"][0]["icon"]
                }
            else:
                weather["error"] = "City not found"
        else:
            weather["error"] = "Please enter a city name"
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run()