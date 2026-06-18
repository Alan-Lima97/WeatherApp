from dataclasses import dataclass


@dataclass
class WeatherData:
    temperature: float
    temperature_symbol: str
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_unit: str
    weather_id: int
    description: str
    sunrise: str
    sunset: str
