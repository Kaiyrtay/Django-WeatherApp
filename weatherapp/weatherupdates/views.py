import requests
import json
from datetime import datetime
from django.shortcuts import render
from django.conf import settings


def index(request):
    try:
        CAT_API_KEY = settings.CAT_API_KEY
        cat_url = f'https://api.thecatapi.com/v1/images/search?&api_key={CAT_API_KEY}'
        cat_response = requests.get(cat_url).json()

        if request.method == 'POST':
            WEATHER_API_KEY = settings.WEATHER_API_KEY
            city_name = request.POST.get('city')
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric'
            response = requests.get(url).json()
            current_time = datetime.now()
            formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")
            city_weather_update = {
                'city': city_name,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °C',
                'country_code': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + 'km/h',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                'time': formatted_time,
            }
        else:
            city_weather_update = {}

        context = {
            'city_weather_update': city_weather_update,
            'cat_url': cat_response[0]['url'],
        }
        return render(request, 'weatherupdates/home.html', context)
    except:
        return render(request, 'weatherupdates/404.html')
