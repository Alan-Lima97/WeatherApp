import os
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFrame,
    QComboBox,
    QPushButton,
    QVBoxLayout,
)
from dotenv import load_dotenv

from app.api import OpenWeatherClient, WeatherApiError
from app.services import WeatherService
from app.settings import WeatherSettings


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.project_dir = Path(__file__).resolve().parents[2]
        self.settings = WeatherSettings()
        self.weather_service = None

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

        self.initUI()

    def initUI(self):
        self.setObjectName("weather_app")
        self.setProperty("weatherTheme", "default")
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
        self.city_input.lineEdit().setPlaceholderText("Search city")

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
        stylesheet_path = self.project_dir / "style.qss"
        icon_path = self.project_dir / "icons" / "chevron-down.svg"
        stylesheet = stylesheet_path.read_text(encoding="utf-8")
        stylesheet = stylesheet.replace("__CHEVRON_DOWN_ICON__", icon_path.as_posix())
        self.setStyleSheet(stylesheet)

    def get_weather(self):
        city = self.city_input.currentText().strip()

        if not city:
            self.display_error("Please enter a city name")
            return

        try:
            weather_data = self.get_weather_service().get_current_weather(city, self.get_selected_units())
        except WeatherApiError as error:
            self.display_error(str(error))
            return

        self.save_city_to_history(city)
        self.display_weather(weather_data)

    def get_weather_service(self):
        if self.weather_service is not None:
            return self.weather_service

        env_path = self.project_dir / ".env"
        load_dotenv(env_path, override=True)
        api_key = os.getenv("API_KEY")

        if not api_key:
            raise WeatherApiError("API key not found\nCheck your .env file")

        self.weather_service = WeatherService(OpenWeatherClient(api_key))
        return self.weather_service

    def load_city_history(self):
        city_history = self.settings.get_city_history()
        last_city = self.settings.get_last_city()

        self.city_input.clear()
        self.city_input.addItems(city_history)

        if last_city:
            self.city_input.setCurrentText(last_city)

    def load_unit_preference(self):
        saved_units = self.settings.get_units()
        index = self.unit_input.findData(saved_units)

        if index == -1:
            index = 0

        self.unit_input.setCurrentIndex(index)

    def get_selected_units(self):
        return self.unit_input.currentData() or "metric"

    def handle_unit_changed(self, _index):
        self.settings.set_units(self.get_selected_units())

        if self.city_input.currentText().strip():
            self.get_weather()

    def save_city_to_history(self, city):
        city_history = self.settings.save_city(city)

        self.city_input.clear()
        self.city_input.addItems(city_history)
        self.city_input.setCurrentText(city)

    def display_empty_state(self):
        self.apply_weather_theme("default")
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
        self.apply_weather_theme("error")
        self.temperature_label.setStyleSheet("font-size: 28px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()
        self.feels_like_label.clear()
        self.min_max_label.clear()
        self.humidity_label.clear()
        self.wind_label.clear()
        self.sunrise_sunset_label.clear()

    def display_weather(self, weather_data):
        self.apply_weather_theme(weather_data.weather_id)

        self.temperature_label.setStyleSheet("font-size: 76px;")
        self.temperature_label.setText(f"{weather_data.temperature:.0f}{weather_data.temperature_symbol}")
        self.emoji_label.setText(self.get_weather_emoji(weather_data.weather_id))
        self.description_label.setText(weather_data.description)
        self.feels_like_label.setText(
            f"Feels like: {weather_data.feels_like:.0f}{weather_data.temperature_symbol}"
        )
        self.min_max_label.setText(
            f"Min: {weather_data.temp_min:.0f}{weather_data.temperature_symbol} / "
            f"Max: {weather_data.temp_max:.0f}{weather_data.temperature_symbol}"
        )
        self.humidity_label.setText(f"Humidity: {weather_data.humidity}% - Pressure: {weather_data.pressure} hPa")
        self.wind_label.setText(f"Wind: {weather_data.wind_speed:.1f} {weather_data.wind_unit}")
        self.sunrise_sunset_label.setText(f"Sunrise: {weather_data.sunrise} - Sunset: {weather_data.sunset}")

    def apply_weather_theme(self, weather_id):
        self.setProperty("weatherTheme", self.get_weather_theme(weather_id))
        self.load_stylesheet()

    @staticmethod
    def get_weather_theme(weather_id):
        if weather_id == "default":
            return "default"

        if weather_id == "error":
            return "error"

        if 200 <= weather_id <= 232 or 500 <= weather_id <= 531:
            return "rain"

        if 600 <= weather_id <= 622:
            return "snow"

        if 701 <= weather_id <= 781:
            return "atmosphere"

        if weather_id == 800:
            return "clear"

        if 801 <= weather_id <= 804:
            return "clouds"

        return "default"

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
