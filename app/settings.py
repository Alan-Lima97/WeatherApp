from PyQt5.QtCore import QSettings


class WeatherSettings:
    def __init__(self):
        self.settings = QSettings("WeatherApp", "WeatherApp")

    def get_city_history(self):
        return self.settings.value("city_history", [], type=list)

    def get_last_city(self):
        return self.settings.value("last_city", "", type=str)

    def save_city(self, city):
        city_history = self.get_city_history()
        city_history = [saved_city for saved_city in city_history if saved_city.lower() != city.lower()]
        city_history.insert(0, city)
        city_history = city_history[:8]

        self.settings.setValue("last_city", city)
        self.settings.setValue("city_history", city_history)
        return city_history

    def get_units(self):
        return self.settings.value("units", "metric", type=str)

    def set_units(self, units):
        self.settings.setValue("units", units)
