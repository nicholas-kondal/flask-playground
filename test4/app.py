# https://medium.com/@david_shortman/write-a-dead-simple-web-app-fast-for-a-hackathon-part-one-a-flask-backend-4410dc15970d
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello there'

from pyowm import OWM
owm = OWM('SECRET_API_KEY')
@app.route('/weather/<country>/<city>')
def weather(country, city):
    weather_manager = owm.weather_manager()
    weather_at_place = weather_manager.weather_at_place(f'{country},{city}')
    temperature = weather_at_place.weather.temperature('celsius')

    weather_details = {
        'temp_celsius': temperature['temp'],
        'temp_kelvin': temperature['temp'] + 273
    }

    if (request.args.get('show_humidity')):
        weather_details['humidity'] = weather_at_place.weather.humidity

    if (request.args.get('show_pressure')):
        weather_details['pressure'] = weather_at_place.weather.pressure

    return weather_details

# Keep this at the bottom of app.py
app.run(debug=True)

