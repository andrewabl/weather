'''Ideas:
    -Online photo of city through city camera

'''
import json, sys, requests
from datetime import datetime
from json import loads
from requests import exceptions
import plot_module, keys


manual = '\n' + "Manual".center(60, '-')\
    +"\n\tUsage: weather.py [Arguments] [City name]\n"\
    + " -f   <--forecast>    - Hourly forecast\n"\
    + " -p   <--plot>        - Plotting temperature forecat(only with --forecast flag)\n"\
    + " -h   <--help>        - Print this manual\n"


openweather_url = 'http://api.openweathermap.org/data/2.5/weather?appid=' + keys.openweather
geo_url = 'https://geo.ipify.org/api/v1?apiKey=' + keys.geoip
weatherbit_url = 'https://api.weatherbit.io/v2.0/forecast/hourly?NC&key=' + keys.weatherbit

def openweather_output(data):
    print('\n' + str(data['name'] + '-' + data['sys']['country']).center(40, '-') + '\n')
    state_data = data['weather'][0]
    print(' Date:\t\t', datetime.fromtimestamp(data['dt']).strftime('%A  %H:%M:%S'))
    print(' State:\t\t', state_data['main'], '(', state_data['description'], ')')

    main_data = data['main']
    print(' Temperature:\t', round(float(main_data['temp']) - 273, 2))
    print(' Feel like:\t', round(float(main_data['feels_like']) - 273, 2))
    print(' Pressure:\t', int(main_data['pressure']))
    print(' Humidity:\t', int(main_data['humidity']))

    wind_data = data['wind']
    print(' Wind speed:\t', round(float(wind_data['speed']), 2))
    print(' Wind deg:\t', int(wind_data['deg']))

    sun_data = data['sys']
    print(' Sunrise:\t', datetime.fromtimestamp(sun_data['sunrise']).time())
    print(' Sunrset:\t', datetime.fromtimestamp(sun_data['sunset']).time())

def weatherbit_otput(data):
    print('\n' + str(data['city_name']).center(60, '-') + '\n')
    for hour_data in data['data']:
        print(' ', datetime.fromtimestamp(hour_data['ts']).strftime('%A  %H:%M'), end = ' \t')
        print('Temp: ', hour_data['temp'], '\tFells like: ', hour_data['app_temp'])

def response_api(url_master, arguments):

    try:
        url =  url_master
        for key, value in arguments.items():
            url += '&' + str(key) + '=' + str(value)
        #print(url)
        response = requests.get(url)
        return loads(response.text)

    except exceptions.ConnectionError as exp:
        raise SystemExit('Connection failure')
    except json.JSONDecodeError as exp:
        raise exp
    
hourly_flag = 0
ploy_flag = 0
count = 1 

#Checking for parameters
while count < len(sys.argv):
    
    try:
        if sys.argv[count] == '-f' or sys.argv[count] == '--forecast':
        
            
            hourly_flag = sys.argv[count + 1]

            if hourly_flag.isdigit() == False or not 2 <= int(hourly_flag) <= 48:
                del sys.argv[count]
                hourly_flag = 0
                raise Exception('Uncorrect forecast parameter. It should be in [2:48] range')

            del sys.argv[count:count + 2]
            continue

        elif sys.argv[count] == '-h' or sys.argv[count] == '--help':
            print(manual)
            sys.exit()

        elif sys.argv[count] == '-p' or sys.argv[count] == '--plot':
            ploy_flag = 1
            del sys.argv[count]
            continue

        elif sys.argv[count][0] == '-':
            raise Exception('Uncorrect option ' + sys.argv[count] + ". Try '--help' for clarification.\a")

        count +=1

    except IndexError:
        print("E: Uncorrect syntax. Try '--help' for clarification.\a")
        sys.exit()

    except Exception as exp:
        print('\aE: ' + str(exp))
        sys.exit()

#Finding geo IP
if len(sys.argv) == 1:

    try:
        json_geo = response_api(geo_url, {})
        sys.argv.append(json_geo['location']['city'])
        print()

    except SystemExit as exp:
        print("\a E: " + str(exp))

#Main loop
for arg in sys.argv[1:]:

    try:
        if hourly_flag == 0:
            json_weather = response_api(openweather_url, arguments={'q': arg})
            openweather_output(json_weather)

        else:
            json_weather = response_api(weatherbit_url, arguments={'hours' : hourly_flag, 'city': arg})
            weatherbit_otput(json_weather)
            if ploy_flag != 0:
                plot_module.plotting(json_weather)

    except SystemExit as exp:
         print("\aE: " + str(exp))

    except KeyError as exp:
        if exp.args[0] == 'name':
            print("\aE: Information about '%s' city is not available" %arg)
    except json.JSONDecodeError as exp:
        print("\aE: Information about '%s' city is not available" %arg)

    print()