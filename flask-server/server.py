from flask import Flask,request, url_for, redirect, render_template, jsonify
#from pycaret.regression import *
import pandas as pd
import pickle
import numpy as np

from get_weather_condition import get_weather
from get_location import get_location_detail
#from flask_pymongo import PyMongo
#import urllib 
import datetime
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily,Hourly

app = Flask(__name__)

#app.config["MONGO_URI"] = "mongodb+srv://ganga:"+urllib.parse.quote("Comnet@vish")+"@cluster0.jnagl.mongodb.net/test?retryWrites=true&w=majority"
#mongo = PyMongo(app)



@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST'])
def predict():

    location_input = [x for x in request.form.values()]
    #pc=location_input[0]
    road=location_input[0]
    direction=location_input[1]
    #loc=get_location_detail(pc)
    #TF_Data = mongo.db.TrafficFlow_Data.find_one({"Direction": "M621_J3toJ2A_EB"})
    #print(TF_Data)
    directionCode={'A38_M_NB':4,'M606_J1toJ2':1,'M606_J2toJ1':2,'M606_J3toJ2':3,'M621_J1_EB':5,'M621_J1_WB':6,
    'M621_J1toM62_WB':7,'M621_J2_WB':8,'M621_J27_WB':20,'M621_J3toJ2A_EB':9,'M621_J3toJ2A_WB':10,'M621_J4_EB':11,
    'M621_J4_WB':12,'M621_J5toJ6_EB':13,'M621_J6_EB':14,'M621_J6_WB':15,'M621_J6toJ5_WB':16,'M621_J7_EB':17,
    'M621_J7toJ6_WB':18,'M621_J7toM1_EB':19,'M621_M1toJ7_WB':21}

    weather={'1':'Clear','2':'Fair','3':'Cloudy','4':'Overcast','5':'Fog','6':'Freezing Fog','7':'Light Rain','8':'Rain','9':'Heavy Rain',
   '10':'Freezing Rain','11':'Heavy Freezing Rain','12':'Sleet','13':'Heavy Sleet','14':'Light Snowfall','15':'Snowfall','16':'Heavy Snowfall',
   '17':'Rain Shower','18':'Heavy Rain Shower','19':'Sleet Shower','20':'Heavy Sleet Shower','21':'Snow Shower','22':'Heavy Snow Shower',
   '23':'Lightning','24':'Hail','25':'Thunderstorm','26':'Heavy Thunderstorm','27':'Storm'}


    #latitude=loc['result']['latitude']
    #longitude=loc['result']['longitude']
    
    #wc=get_weather()
    loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
    

    data_unseen=pd.read_csv('./data/synthetic_data.csv')

    
    #data_unseen_y = data_unseen.Class

    #weather_condition=get_weather(road=road)['weather'][0]['id']
    weekday = datetime.today().weekday()
    month= datetime.today().month
    day=datetime.today().day
    year=datetime.today().year
    hour=datetime.today().hour
    
    start = datetime(year, month, day,hour-1,0)
    end = datetime(year, month, day, hour, 59)
    

    
    
    #print(weather[str1])


    weather_condition=get_weather(road=road)
    print(weather_condition)

    #weather_condition=get_weather(road=road, year=year, month=month, day=day, hour=hour)


    isHour=data_unseen['Hour']==hour
    isMonth=data_unseen['Month']==month
    isDirection=data_unseen['Direction']==direction
    isWeekday=data_unseen['WeekDay']==weekday

    allFilters= isHour & isMonth & isDirection & isWeekday

    data_unseen=data_unseen[allFilters]
    
    data_unseen['DirectionCode']= directionCode[direction]
    
    #data_unseen['coco']=weather_condition[0]
    data_unseen['coco']=weather_condition[0]
    str1=str(round(weather_condition[0]))
    print(str1)
    print(weather[str1])

    
    data_unseen.drop(['Direction'], axis=1, inplace=True)
    #int_features = [x for x in request.form.values()]
    #final = np.array(int_features)
    #data_unseen = pd.DataFrame([final], columns = cols)latitude
    #prediction = [predict_model(model, data=data_unseen_X, round = 0)]
    
    Ypredict = loaded_model.predict(data_unseen)  
    y_prob_nm = loaded_model.predict_proba(data_unseen)
    prob=y_prob_nm[:,1]
    
    #score=accuracy_score(data_unseen_y[0:], Ypredict)
    #Ypredict = loaded_model.predict(data_unseen_X[0:])  
    #prediction = int(prediction.Label[0])
    #prediction=int_features
    showRow=0
    tcf=data_unseen.loc[:,'Total_Carriageway_Flow'].head(1)
    tcf=data_unseen['Total_Carriageway_Flow'].iloc[showRow]
    speed=data_unseen['Speed_Value'].iloc[showRow]

    #return render_template('result.html',weather=weather[str1])
    return render_template('result.html',weather=weather[str1], pred=Ypredict[showRow],
        prob=prob[showRow], road=road, direction=direction, TCF=tcf, Speed=speed )

    #return render_template('result.html',pred='Prediction:{}, Probability: {}'.format(Ypredict[6],prob[6]))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    data_unseen = pd.DataFrame([data])
    prediction = predict_model(model, data=data_unseen)
    output = prediction.Label[0]
    return jsonify(output)


if __name__ == '__main__':
    app.run(debug=True, port='3000')