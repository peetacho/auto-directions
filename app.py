from flask import Flask, render_template, url_for, flash, redirect, request, session
from get_routes import call_google_api, calculate_next_class, get_today_date
from get_weather import call_weather_api
import random
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    next_course_info = calculate_next_class()
    routes = call_google_api(next_course_info[0])
    pagename = 'index'
    r_words = ['Awesome', 'Wonderful', 'Incredible', 'Amazing', 'Excellent', 'Brilliant']
    titlevar = random.choice(r_words)
    weather_info = call_weather_api()
    return render_template('index.html', weather_info=weather_info, title_var=titlevar, pagename=pagename, routes=routes, next_course_info=next_course_info, today_date=get_today_date())

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))