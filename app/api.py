import requests


class WeatherApiError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class OpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_current_weather(self, city, units):
        params = {
            "q": city,
            "appid": self.api_key,
            "units": units,
            "lang": "en",
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            status_code = error.response.status_code if error.response is not None else None
            raise WeatherApiError(self.get_http_error_message(status_code), status_code) from error
        except requests.exceptions.RequestException as error:
            raise WeatherApiError("Connection Error") from error

    @staticmethod
    def get_http_error_message(status_code):
        match status_code:
            case 400:
                return "Bad Request"
            case 401:
                return "Unauthorized\nAPI key not loaded or not activated"
            case 404:
                return "City not found"
            case _:
                return "HTTP Error"
