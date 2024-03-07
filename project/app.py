from flask import Flask, render_template, request
from weather import get_current_weather, get_forecast_weather,get_city_name

app = Flask(__name__)

@app.route('/')
def  index():
    return render_template('index.html')

@app.route('/weather', methods=['GET','POST'])
def  weather():
    temperature =""
    humidity = ""
    wind_speed = ""
    city="Sangli"
    
    # detecting whether  the user has submitted a form or not or by  getting cityname current location it
    if request.method == 'POST':
        city=get_city_name()
    else:
        city = request.args.get('city')
    
    if not bool(city.strip()):
        city = "Sangli"
        
        
    weather_data = get_current_weather(city)
    forecast_list =get_forecast_weather(city)
        
    
    if not weather_data['cod'] == 200:
        # return "City not found"
        return render_template('error.html')
    
    temperature = f"{weather_data["main"]["temp"]:.1f}"
    humidity=f"{weather_data["main"]["humidity"]}"
    wind_speed=f"{weather_data['wind']['speed']}"
    icon = (weather_data['weather'][0]['icon']) + "@4x.png"
    description = weather_data['weather'][0]['description']
    localdate = forecast_list[0]['date']
    cityname = weather_data['name']
    cod =  weather_data['cod']
    
    return render_template('index.html',
                    temperature = temperature,
                    humidity = humidity,
                    wind_speed = wind_speed,
                    icon = icon,
                    description = description,
                    cityname =cityname,
                    localdate =localdate,
                    forecast_list=forecast_list,
                    cod = cod)

if __name__ == "__main__":
    app.run(debug=True)