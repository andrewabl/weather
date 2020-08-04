import matplotlib.pyplot as plot
from datetime import datetime


def plotting(data_master):
    
    data = data_master['data']
    y_values_temp = []
    y_values_app_temp = []
    x_values = []

    for hour in data:
         y_values_temp.append(hour['temp'])
         y_values_app_temp.append(hour['app_temp'])
    
    x_values = range(0, len(data))

    plot.figure(num=None, figsize=(8, 6), facecolor='#eeefff')
    plot.plot(x_values, y_values_app_temp, color='b', label='Feel Temperature')
    plot.plot(x_values, y_values_temp, color='m',label='Real Temperature')
    plot.ylabel('Temperature C \u00b0')
    plot.xlabel('Hours from now')
    plot.title('Weather Forecast for ' + str(len(x_values)) + ' hours in ' + str(data_master['city_name']))
    plot.legend()
    plot.show()