import csv
from logging import exception
from operator import ge
import random
from urllib import request
import json
import datetime
import tweepy
def get_random_quote(quotes_file='quotes.csv'):
    try:
        with open(quotes_file) as csvfile:
           quotes = [{'author': line[0],
                      'quote': line[1]} for line in csv.reader(csvfile, delimiter='|')]
    
    except Exception as e:
        quotes = [{'author': 'Eric Idle',
                   'quote': 'Always Look on the Bright Side of Life.'}]
    return random.choice(quotes)

def get_weather_forecast(coords={'lat': 28.4717 ,'lon':-80.5378}):
    try:
        api_key= 'e33f01646531c26304e692b68172d093'
        url=f'https://api.openweathermap.org/data/2.5/forecast?lat={coords["lat"]}&lon={coords["lon"]}&appid={api_key}&units=metric'
        data= json.load(request.urlopen(url))
        forecast = {'city': data['city']['name'], # city name
                    'country': data['city']['country'], # country name
                    'periods': list()} # list to hold forecast data for future periods
        
        for period in data['list'][0:9]: # populate list with next 9 forecast periods 
            forecast['periods'].append({'timestamp': datetime.datetime.fromtimestamp(period['dt']),
                                        'temp': round(period['main']['temp']),
                                        'description': period['weather'][0]['description'].title(),
                                        'icon': f'http://openweathermap.org/img/wn/{period["weather"][0]["icon"]}.png'})
        
        return forecast

    except Exception as e:
        print(e)

def get_twitter_trends(woeid=23424977):
    try:
        api_key='ZQmrEuyRF1Ohck3bcdOcbhbSK'
        api_secret_key='uVMV5atUHX1nOoE8AdcG8bkgf6cNC4RjXG6RobzJykpxOOTmv6'
        auth= tweepy.AppAuthHandler(api_key,api_secret_key)
        return tweepy.API(auth).trends_place(woeid)[0]['trends']
    except Exception as e:
        print(e)

def get_wikipedia_article():
    try:
        data= json.load(request.urlopen('https://en.wikipedia.org/api/rest_v1/page/random/summary'))
        return {
            'title': data['title'],
            'extract': data['extract'],
            'url' : data['content_urls']['desktop']['page'] 
        }
    except Exception as e:
        print(e)

if __name__ == '__main__':
    print('\nTesting quote generation...')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')
    
    quote = get_random_quote(quotes_file = None)
    print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')
    
    ##### test get_weather_forecast() #####
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    austin = {'lat': 30.2748,'lon': -97.7404} # coordinates for Texas State Capitol
    forecast = get_weather_forecast(coords = austin) # get Austin, TX forecast
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['periods']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    invalid = {'lat': 1234.5678 ,'lon': 1234.5678} # invalid coordinates
    forecast = get_weather_forecast(coords = invalid) # get forecast for invalid location
    if forecast is None:
        print('Weather forecast for invalid coordinates returned None')
        
    #### Test get_twitter_trends ####
    print('\nTesting twitter trend generation...')
    
    trends= get_twitter_trends()
    if trends:
        print('\nTop 10 twitter trends in United states')
        for trend in trends[0:10]:
            print(f'-{trend["name"]}:{trend["url"]}')
    
    trends= get_twitter_trends(woeid = 44418)
    if trends:
        print('\nTop 10 twitter trends in London')
        for trend in trends[0:10]:
            print(f'-{trend["name"]}:{trend["url"]}')
            
    trends=get_twitter_trends(woeid=-1)
    if trends is None:
        print('Twitter trends is invalid for this location...WOEID returned None')
    
    ##### test get_wikipedia_article() #####
    print('\nTesting random Wikipedia article retrieval...')

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')
        
            