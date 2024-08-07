from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import requests
import datetime

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = 'YOUR_API_KEY_HERE'
search_history = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return templates.TemplateResponse("index.html", {"request": request, "weather_data": None, "current_time": current_time, "history": search_history})

@app.get("/weather", response_class=HTMLResponse)
async def get_weather(request: Request, city: str = Query(None), lat: float = Query(None), lon: float = Query(None), zip_code: str = Query(None)):
    if not any([city, lat, lon, zip_code]):
        return templates.TemplateResponse("index.html", 
                                          {"request": request,
                                           "weather_data": None,
                                           "error_message": "Please enter a city name, coordinates (latitude and longitude), or ZIP code."}
                                         )

    weather_data = None
    error_message = None

    if city:
        weather_data = fetch_weather("q", city)
    elif lat and lon:
        weather_data = fetch_weather("lat", lat, "lon", lon)
    elif zip_code:
        weather_data = fetch_weather("zip", zip_code)

    if not weather_data:
        error_message = f"Weather data not found for {city or ''}"

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if city and city not in search_history:
        search_history.append(city)

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "weather_data": weather_data,
                                                     "current_time": current_time,
                                                     "history": search_history,
                                                     "error_message": error_message}
                                     )

def fetch_weather(*args):
    params = {args[i]: args[i + 1] for i in range(0, len(args), 2)}
    params["appid"] = API_KEY
    params["units"] = "metric"

    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    complete_url = base_url + "&".join(f"{key}={value}" for key, value in params.items())

    response = requests.get(complete_url)
    data = response.json()

    if data['cod'] != '404':
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        sys = data['sys']
        return {
            'city': data.get('name', '').capitalize(),
            'country': sys.get('country'),
            'temperature': main.get('temp'),
            'feels_like': main.get('feels_like'),
            'temp_min': main.get('temp_min'),
            'temp_max': main.get('temp_max'),
            'humidity': main.get('humidity'),
            'pressure': main.get('pressure'),
            'description': weather.get('description', '').capitalize(),
            'icon_url': f'http://openweathermap.org/img/wn/{weather["icon"]}@2x.png',
            'wind_speed': wind.get('speed'),
            'wind_deg': wind.get('deg'),
            'clouds': data.get('clouds', {}).get('all'),
            'visibility': data.get('visibility'),
            'sunrise': datetime.datetime.fromtimestamp(sys.get('sunrise', 0)).strftime('%H:%M:%S'),
            'sunset': datetime.datetime.fromtimestamp(sys.get('sunset', 0)).strftime('%H:%M:%S'),
        }
    else:
        return None

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

