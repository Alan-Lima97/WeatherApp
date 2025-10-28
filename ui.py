import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QLineEdit, QPushButton, QVBoxLayout
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os   

class WeatherApp(QWidget):

    def __init__(self):

        super().__init__()
        # input
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        # main_frame
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel (self)
        self.description_label = QLabel(self)
        #extra_frame
        self.feels_like_label = QLabel(self)
        self.min_max_label = QLabel(self)
        self.humidity_label = QLabel(self)
        self.wind_label = QLabel(self)
        self.sunrise_sunset_label = QLabel(self)

        #group frames
        self.main_frame = QFrame(self)
        self.extra_frame = QFrame(self)

        self.initUI()

    # UI config
    def initUI (self):

        self.setWindowTitle("Weather App")

        # input layout
        input_Layout = QVBoxLayout()
        input_Layout.addWidget(self.city_label)
        input_Layout.addWidget(self.city_input)
        input_Layout.addWidget(self.get_weather_button)
        input_Layout.setSpacing(10)

        # main_frame layout
        main_frame_layout = QVBoxLayout(self.main_frame)
        main_frame_layout.addWidget(self.temperature_label)
        main_frame_layout.addWidget(self.emoji_label)
        main_frame_layout.addWidget(self.description_label)
        main_frame_layout.setContentsMargins(18, 12, 18, 12)

        #extra_frame layout
        extra_frame_layout =QVBoxLayout(self.extra_frame)
        extra_frame_layout.addWidget(self.feels_like_label)
        extra_frame_layout.addWidget(self.min_max_label)
        extra_frame_layout.addWidget(self.humidity_label)
        extra_frame_layout.addWidget(self.wind_label)
        extra_frame_layout.addWidget(self.sunrise_sunset_label)
        extra_frame_layout.setSpacing(6)
        extra_frame_layout.setContentsMargins(12, 10, 12, 10)

        # principal layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(input_Layout)
        main_layout.addWidget(self.main_frame)
        main_layout.addWidget(self.extra_frame)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(18, 18, 18, 18)

        self.setLayout(main_layout)

        # center alignment
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.feels_like_label.setAlignment(Qt.AlignCenter)
        self.min_max_label.setAlignment(Qt.AlignCenter)
        self.humidity_label.setAlignment(Qt.AlignCenter)
        self.wind_label.setAlignment(Qt.AlignCenter)
        self.sunrise_sunset_label.setAlignment(Qt.AlignCenter)

        # object names for style
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.feels_like_label.setObjectName("feels_like_label")
        self.min_max_label.setObjectName("min_max_label")
        self.humidity_label.setObjectName("humidity_label")
        self.wind_label.setObjectName("wind_label")
        self.sunrise_sunset_label.setObjectName("sunrise_sunset_label")

        # style config
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f1724, stop:1 #0b1220);
            }
            QLabel, QPushButton, QLineEdit {
                font-family: Calibri;
                color: #e6eef8;
            }
            QLabel#city_label {
                font-size: 24px;
                font-style: italic;
                color: #cfe7ff;
            }
            QLineEdit#city_input {
                font-size: 20px;
                padding: 8px 10px;
                border-radius: 8px;
                border: 1px solid rgba(255,255,255,0.08);
                background: rgba(255,255,255,0.03);
                min-width: 260px;
            }
            QPushButton#get_weather_button {
                font-size: 16px;
                padding: 10px 14px;
                border-radius: 10px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #2563eb, stop:1 #0ea5e9);
                color: white;
                border: none;
            }
            QFrame#main_frame {
                background: rgba(255,255,255,0.03);
                border-radius: 12px;
                border: 1px solid rgba(255,255,255,0.04);
                padding: 6px;
            }
            QLabel#temperature_label {
                font-size: 72px;
                font-weight: 700;
                color: #ffffff;
            }
            QLabel#emoji_label {
                font-size: 86px;
                font-family: 'Segoe UI Emoji';
            }
            QLabel#description_label {
                font-size: 20px;
                color: #d7e8ff;
            }
            QFrame#extra_frame {
                background: transparent;
                border-radius: 10px;
            }
            QLabel#feels_like_label, QLabel#min_max_label, QLabel#humidity_label,
            QLabel#wind_label, QLabel#sunrise_sunset_label {
                font-size: 14px;
                color: #cbdffd;
            }                   
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    # api calls and errors
    def get_weather(self):
    
        # api config
        load_dotenv()
        API_KEY = os.getenv("API_KEY")
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
        # get data
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            if data["cod"] == 200:
                self.display_weather(data)
        # raises errors
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from te server")
                case _:
                    self.display_error(f"HTTP Error ocurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too Many Redirects:\nCheck the URL")
        
        except requests.exceptions.RequestException as uni_error:
            self.display_error(f"Request Erro:\n{uni_error}")
    
    # display the errors
    def display_error(self, message):

        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    # display the infos
    def display_weather(self, data):

        # get infos
        temperature_c = data["main"]["temp"] - 273.15
        feels_like_c = data["main"]["feels_like"] - 273.15
        temp_min_c = data["main"]["temp_min"] - 273.15
        temp_max_c = data["main"]["temp_max"] - 273.15
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"] * 3.6
        weather_id = data["weather"][0]["id"]
        weater_description = data["weather"][0]["description"]
        # get timestamp infos
        sunrise_timestamp = data["sys"]["sunrise"]
        sunset_timestamp = data["sys"]["sunset"]
        timezone_secs = data["timezone"]
        city_timezone = timezone(timedelta(seconds=timezone_secs))
        sunrise_local = datetime.fromtimestamp(sunrise_timestamp, tz = city_timezone).strftime("%H:%M")
        sunset_local = datetime.fromtimestamp(sunset_timestamp, tz = city_timezone).strftime("%H:%M")

        # att widgets
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weater_description)
        self.feels_like_label.setText(f"Feels like: {feels_like_c:.0f}°C")
        self.min_max_label.setText(f"Min: {temp_min_c:.0f}°C / Max: {temp_max_c:.0f}°C")
        self.humidity_label.setText(f"Humidity: {humidity}% - Pressure: {pressure} hpa")
        self.wind_label.setText(f"Wind: {wind_speed:.1f} km/h")
        self.sunrise_sunset_label.setText(f"Sunrise: {sunrise_local} - Sunset: {sunset_local}")

        self.temperature_label.setStyleSheet("font-size: 75px;")

    # defines emojis
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
            case _ if 801 <= weather_id <= 804:
                return "☁️"
            case 762:
                return "🌋"
            case 771:
                return "🌀"
            case 781:
                return "🌪️"
            case 800:
                return "☀️"
            case _:
                return ""