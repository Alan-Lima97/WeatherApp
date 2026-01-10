# Weather App 🌦️

A desktop application in Python using PyQt5 that shows the weather forecast for any city in the world using the OpenWeather public API.

---

##  Features

- Search the weather for any city in the world
  
- Display:

  - Current tempetarure in Celsius;
  - Feels like temperature;
  - Min/Max temperature;
  - Humidity and pressure;
  - Wind speed;
  - Sunrise and sunset in the local time

- Detailed error handling

- Modern layout wity styled fonts

---

##  Installation

1. Clone this repository and navigate into it:

```bash
git clone https://github.com/Alan-Lima97/WeatherApp.git
cd WeatherApp
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate    # Linux / Mac
.venv\Scripts\activate       # Windows
```

3. Install dependencies
	- pip install -r requirements.txt

## Environment Variables

This application requires an API key from OpenWeather.

1. Create a `.env` file in the root directory of the project  
2. Add the following line:

    API_KEY=your_openweather_api_key_here

3. You can obtain a free API key at:  
   https://openweathermap.org/api

⚠️ Do not commit the `.env` file to the repository.

## Usage

Run the application
	- py main.py

- Enter the city name and click in the Get Weather button

- The app will display all weather information for the selected city

## Screenshots

![Main screen with infos](screenshot/screenshot_1.png)

![Main screen with infos](screenshot/screenshot_2.png)
