import os
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from dotenv import load_dotenv


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        # input
        self.city_label = QLabel("Enter city name:")
        self.city_input = QLineEdit()
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

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setMinimumWidth(300)
        self.resize(300, 500)

        # input layout
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.city_label)
        input_layout.addWidget(self.city_input)
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
            self.city_input,
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

        # object names (stylesheet)
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
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

        # stylesheet
        self.setStyleSheet("""
        /* ===== Root ===== */
        QWidget {
            background-color: #0b1220;
        }

        /* ===== Base text ===== */
        QLabel, QLineEdit, QPushButton {
            font-family: Segoe UI, Calibri;
            color: #e6edff;
        }

        /* ===== City label ===== */
        QLabel#city_label {
            font-size: 22px;
            font-weight: 500;
            color: #c7d6ff;
        }

        /* ===== Input ===== */
        QLineEdit#city_input {
            font-size: 18px;
            padding: 10px 14px;
            border-radius: 12px;
            border: 1px solid #1e293b;
            background-color: #020617;
        }

        QLineEdit#city_input:focus {
            border: 1px solid #3b82f6;
            background-color: #020617;
        }

        /* ===== Button ===== */
        QPushButton#get_weather_button {
            font-size: 15px;
            font-weight: 600;
            padding: 10px;
            border-radius: 12px;
            background-color: #2563eb;
            border: none;
        }

        QPushButton#get_weather_button:hover {
            background-color: #1d4ed8;
        }

        QPushButton#get_weather_button:pressed {
            background-color: #1e40af;
        }

        /* ===== Cards ===== */
        QFrame#main_frame {
            background-color: #020617;
            border-radius: 16px;
            border: 1px solid #1e293b;
        }

        QFrame#extra_frame {
            background-color: transparent;
        }

        /* ===== Temperature ===== */
        QLabel#temperature_label {
            font-size: 72px;
            font-weight: 700;
            color: #ffffff;
        }

        /* ===== Emoji ===== */
        QLabel#emoji_label {
            font-size: 80px;
            margin-top: 6px;
        }

        /* ===== Description ===== */
        QLabel#description_label {
            font-size: 18px;
            color: #c7d6ff;
            margin-bottom: 6px;
        }

        /* ===== Extra info ===== */
        QLabel#feels_like_label,
        QLabel#min_max_label,
        QLabel#humidity_label,
        QLabel#wind_label,
        QLabel#sunrise_sunset_label {
            font-size: 13px;
            color: #9fb3ff;
        }
        """)


        # signals
        self.get_weather_button.clicked.connect(self.get_weather)
        self.city_input.returnPressed.connect(self.get_weather)

    def get_weather(self):
        env_path = Path(__file__).resolve().parent / ".env"
        load_dotenv(env_path, override=True)

        api_key = os.getenv("API_KEY")

        if not api_key:
            self.display_error("API key not found\nCheck your .env file")
            return

        city = self.city_input.text().strip()

        if not city:
            self.display_error("Please enter a city name")
            return

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric&lang=en"
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
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
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"] * 3.6

        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"].capitalize()

        tz = timezone(timedelta(seconds=data["timezone"]))
        sunrise = datetime.fromtimestamp(data["sys"]["sunrise"], tz).strftime("%H:%M")
        sunset = datetime.fromtimestamp(data["sys"]["sunset"], tz).strftime("%H:%M")

        self.temperature_label.setStyleSheet("font-size: 76px;")
        self.temperature_label.setText(f"{temperature:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(description)
        self.feels_like_label.setText(f"Feels like: {feels_like:.0f}°C")
        self.min_max_label.setText(f"Min: {temp_min:.0f}°C / Max: {temp_max:.0f}°C")
        self.humidity_label.setText(f"Humidity: {humidity}% - Pressure: {pressure} hPa")
        self.wind_label.setText(f"Wind: {wind_speed:.1f} km/h")
        self.sunrise_sunset_label.setText(f"Sunrise: {sunrise} - Sunset: {sunset}")

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
