from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily,Hourly

import requests   

def get_weather(road):

    
      #url='http://pro.openweathermap.org/data/2.5/weather?q=Birmingham,uk&APPID=b68960a402d40a497b69695725ad73af'

    



   # Create Point for Birmingham
    #Birmingham = Point(52.49, -1.86, 140)
    #Bradford = Point(53.79, -1.75, 168.78)
    #Leeds= Point(53.801277, -1.548567, 340)
   
   #print('City : ',City)
   month= datetime.today().month
   day=datetime.today().day
   year=datetime.today().year
   hour=datetime.today().hour
   #print(year, month, day, hour, City)
   start = datetime(year, month, day,hour,0)
   end = datetime(year, month, day, hour, 59)
   #print(hour)
   if road =='M606':
       #City = Point(53.79, -1.75, 168.78)
       data = Hourly(Point(53.79, -1.75, 168.78), start, end)
         #City='Bradford'
   elif road=='M621':
        #City='Leeds'
       City= Point(53.801277, -1.548567, 340)
       data = Hourly(Point(53.801277, -1.548567, 340), start, end)
   elif road=='A38(M)':
        #City='Birmingham'
       City = Point(52.49, -1.86, 140)
       data = Hourly(Point(52.49, -1.86, 140), start, end)
    #data = Hourly(City, start, end)
   weather_df = data.fetch()
   print(start)
   print(weather_df)
   coco=list(weather_df['coco'])
    #print(coco[0])
    #str1=str(round(coco[0]))
    #print(str1)
    #print(weather[coco])
    
   weather={'1':'Clear','2':'Fair','3':'Cloudy','4':'Overcast','5':'Fog','6':'Freezing Fog','7':'Light Rain','8':'Rain','9':'Heavy Rain',
   '10':'Freezing Rain','11':'Heavy Freezing Rain','12':'Sleet','13':'Heavy Sleet','14':'Light Snowfall','15':'Snowfall','16':'Heavy Snowfall',
   '17':'Rain Shower','18':'Heavy Rain Shower','19':'Sleet Shower','20':'Heavy Sleet Shower','21':'Snow Shower','22':'Heavy Snow Shower',
   '23':'Lightning','24':'Hail','25':'Thunderstorm','26':'Heavy Thunderstorm','27':'Storm'}
    
   weather_df=weather_df.reset_index()
    #print(weather[str1])
    
   return coco


