from datetime import datetime, timezone, timedelta

from .models import WeatherData


class WeatherService:
    def __init__(self, client):
        self.client = client

    def get_current_weather(self, city, units):
        data = self.client.get_current_weather(city, units)
        return self.parse_weather_data(data, units)

    def parse_weather_data(self, data, units):
        weather_id = data["weather"][0]["id"]
        tz = timezone(timedelta(seconds=data["timezone"]))
        wind_speed, wind_unit = self.get_wind_display(data["wind"]["speed"], units)

        return WeatherData(
            temperature=data["main"]["temp"],
            temperature_symbol=self.get_temperature_symbol(units),
            feels_like=data["main"]["feels_like"],
            temp_min=data["main"]["temp_min"],
            temp_max=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            wind_speed=wind_speed,
            wind_unit=wind_unit,
            weather_id=weather_id,
            description=data["weather"][0]["description"].capitalize(),
            sunrise=datetime.fromtimestamp(data["sys"]["sunrise"], tz).strftime("%H:%M"),
            sunset=datetime.fromtimestamp(data["sys"]["sunset"], tz).strftime("%H:%M"),
        )

    @staticmethod
    def get_temperature_symbol(units):
        match units:
            case "imperial":
                return "°F"
            case "standard":
                return "K"
            case _:
                return "°C"

    @staticmethod
    def get_wind_display(wind_speed, units):
        match units:
            case "imperial":
                return wind_speed, "mph"
            case "standard":
                return wind_speed, "m/s"
            case _:
                return wind_speed * 3.6, "km/h"
