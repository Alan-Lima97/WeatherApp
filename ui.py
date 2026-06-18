import os
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QComboBox,
    QPushButton,
    QVBoxLayout,
)

from dotenv import load_dotenv


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # input
        self.city_label = QLabel("Enter city name:")
        self.city_input = QComboBox()
        self.city_input.setEditable(True)
        self.unit_input = QComboBox()
        self.unit_input.addItem("Celsius", "metric")
        self.unit_input.addItem("Fahrenheit", "imperial")
        self.unit_input.addItem("Kelvin", "standard")
        self.get_weather_button = QPushButton("Get Weather")

        # main_frame
        self.temperature_label = QLabel()
        self.emoji_label = QLabel()
        self.description_label = QLabel()

        # extra_frame
        self.feels_like_label = QLabel()
        self.min_max_label = QLabel()
        self.humidity_label = QLabel()
        self.wind_label = QLabel()
        self.sunrise_sunset_label = QLabel()

        # frames
        self.main_frame = QFrame()
        self.extra_frame = QFrame()

        self.settings = QSettings("WeatherApp", "WeatherApp")

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setMinimumWidth(360)
        self.resize(360, 500)

        # input layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.city_label)
        input_layout.addWidget(self.city_input)
        input_layout.addWidget(self.unit_input)
        input_layout.addWidget(self.get_weather_button)
        input_layout.setSpacing(10)

        # main frame layout
        main_frame_layout = QVBoxLayout(self.main_frame)
        main_frame_layout.addWidget(self.temperature_label)
        main_frame_layout.addWidget(self.emoji_label)
        main_frame_layout.addWidget(self.description_label)
        main_frame_layout.setContentsMargins(18, 12, 18, 12)

        # extra frame layout
        extra_frame_layout = QVBoxLayout(self.extra_frame)
        extra_frame_layout.addWidget(self.feels_like_label)
        extra_frame_layout.addWidget(self.min_max_label)
        extra_frame_layout.addWidget(self.humidity_label)
        extra_frame_layout.addWidget(self.wind_label)
        extra_frame_layout.addWidget(self.sunrise_sunset_label)
        extra_frame_layout.setSpacing(6)
        extra_frame_layout.setContentsMargins(12, 10, 12, 10)

        # main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.main_frame)
        main_layout.addWidget(self.extra_frame)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(18, 18, 18, 18)

        self.setLayout(main_layout)

        # alignment
        for widget in [
            self.city_label,
            self.temperature_label,
            self.emoji_label,
            self.description_label,
            self.feels_like_label,
            self.min_max_label,
            self.humidity_label,
            self.wind_label,
            self.sunrise_sunset_label,
        ]:
            widget.setAlignment(Qt.AlignCenter)

        self.city_input.lineEdit().setAlignment(Qt.AlignCenter)

        # object names (stylesheet)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.unit_input.setObjectName("unit_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.main_frame.setObjectName("main_frame")
        self.extra_frame.setObjectName("extra_frame")

        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.feels_like_label.setObjectName("feels_like_label")
        self.min_max_label.setObjectName("min_max_label")
        self.humidity_label.setObjectName("humidity_label")
        self.wind_label.setObjectName("wind_label")
        self.sunrise_sunset_label.setObjectName("sunrise_sunset_label")

        self.load_stylesheet()
        self.load_unit_preference()

        # signals
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.lineEdit().returnPressed.connect(self.get_weather)
        self.city_input.activated.connect(lambda _index: self.get_weather())
        self.unit_input.currentIndexChanged.connect(self.handle_unit_changed)

        self.load_city_history()
        self.display_empty_state()

    def load_stylesheet(self):
        stylesheet_path = Path(__file__).resolve().parent / "style.qss"
        icon_path = Path(__file__).resolve().parent / "icons" / "chevron-down.svg"
        stylesheet = stylesheet_path.read_text(encoding="utf-8")
        stylesheet = stylesheet.replace("__CHEVRON_DOWN_ICON__", icon_path.as_posix())
        self.setStyleSheet(stylesheet)

    def get_weather(self):
        env_path = Path(__file__).resolve().parent / ".env"
        load_dotenv(env_path, override=True)

        api_key = os.getenv("API_KEY")

        if not api_key:
            self.display_error("API key not found\nCheck your .env file")
            return

        city = self.city_input.currentText().strip()

        if not city:
            self.display_error("Please enter a city name")
            return

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units={self.get_selected_units()}&lang=en"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.save_city_to_history(city)
            self.display_weather(response.json())

        except requests.exceptions.HTTPError:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request")
                case 401:
                    self.display_error("Unauthorized\nAPI key not loaded or not activated")
                case 404:
                    self.display_error("City not found")
                case _:
                    self.display_error("HTTP Error")

        except requests.exceptions.RequestException:
            self.display_error("Connection Error")

    def load_city_history(self):
        city_history = self.settings.value("city_history", [], type=list)
        last_city = self.settings.value("last_city", "", type=str)

        self.city_input.clear()
        self.city_input.addItems(city_history)

        if last_city:
            self.city_input.setCurrentText(last_city)

    def load_unit_preference(self):
        saved_units = self.settings.value("units", "metric", type=str)
        index = self.unit_input.findData(saved_units)

        if index == -1:
            index = 0

        self.unit_input.setCurrentIndex(index)

    def get_selected_units(self):
        return self.unit_input.currentData() or "metric"

    def handle_unit_changed(self, _index):
        self.settings.setValue("units", self.get_selected_units())

        if self.city_input.currentText().strip():
            self.get_weather()

    def save_city_to_history(self, city):
        city_history = self.settings.value("city_history", [], type=list)
        city_history = [saved_city for saved_city in city_history if saved_city.lower() != city.lower()]
        city_history.insert(0, city)
        city_history = city_history[:8]

        self.settings.setValue("last_city", city)
        self.settings.setValue("city_history", city_history)

        self.city_input.clear()
        self.city_input.addItems(city_history)
        self.city_input.setCurrentText(city)

    def display_empty_state(self):
        self.temperature_label.setStyleSheet("font-size: 28px;")
        self.temperature_label.setText("Search for a city")
        self.emoji_label.setText("☁️")
        self.description_label.setText("Current weather will appear here")
        self.feels_like_label.clear()
        self.min_max_label.clear()
        self.humidity_label.clear()
        self.wind_label.clear()
        self.sunrise_sunset_label.clear()

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 28px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.feels_like_label.clear()
        self.min_max_label.clear()
        self.humidity_label.clear()
        self.wind_label.clear()
        self.sunrise_sunset_label.clear()

    def display_weather(self, data):
        units = self.get_selected_units()
        temperature_symbol = self.get_temperature_symbol(units)

        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed, wind_unit = self.get_wind_display(data["wind"]["speed"], units)

        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"].capitalize()

        tz = timezone(timedelta(seconds=data["timezone"]))
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz).strftime("%H:%M")

        self.temperature_label.setStyleSheet("font-size: 76px;")
        self.temperature_label.setText(f"{temperature:.0f}{temperature_symbol}")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description)
        self.feels_like_label.setText(f"Feels like: {feels_like:.0f}{temperature_symbol}")
        self.min_max_label.setText(f"Min: {temp_min:.0f}{temperature_symbol} / Max: {temp_max:.0f}{temperature_symbol}")
        self.humidity_label.setText(f"Humidity: {humidity}% - Pressure: {pressure} hPa")
        self.wind_label.setText(f"Wind: {wind_speed:.1f} {wind_unit}")
        self.sunrise_sunset_label.setText(f"Sunrise: {sunrise} - Sunset: {sunset}")

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

    @staticmethod
    def get_weather_emoji(weather_id):
        match weather_id:
            case _ if 200 <= weather_id <= 232:
                return "⛈️"
            case _ if 300 <= weather_id <= 321:
                return "🌦️"
            case _ if 500 <= weather_id <= 531:
                return "🌧️"
            case _ if 600 <= weather_id <= 622:
                return "❄️"
            case _ if 701 <= weather_id <= 741:
                return "🌁"
            case 800:
                return "☀️"
            case _ if 801 <= weather_id <= 804:
                return "☁️"
            case _:
                return ""
