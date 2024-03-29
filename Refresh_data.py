import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap
import requests

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather App")
        self.layout = QVBoxLayout()

        self.city_label = QLabel("Enter city:")
        self.layout.addWidget(self.city_label)

        self.city_entry = QLineEdit()
        self.layout.addWidget(self.city_entry)

        self.units_combo = QComboBox()
        self.units_combo.addItems(["Celsius", "Fahrenheit"])
        self.layout.addWidget(self.units_combo)

        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.get_weather_button)

        self.weather_icon_label = QLabel()
        self.layout.addWidget(self.weather_icon_label)

        self.weather_info_label = QLabel()
        self.layout.addWidget(self.weather_info_label)

        self.forecast_label = QLabel()
        self.layout.addWidget(self.forecast_label)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_weather)
        self.layout.addWidget(self.refresh_button)

        self.setLayout(self.layout)

        self.api_key = '78b743af83a34fc78ce160059242102'
        self.weather_data = None
        self.forecast_data = None

    def get_weather(self):
        city = self.city_entry.text()
        units = self.units_combo.currentText().lower()
        url = f'http://api.weatherapi.com/v1/forecast.json?key={self.api_key}&q={city}&aqi=no&days=5&units={units}'

        try:
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                error_message = data['error']['message']
                QMessageBox.warning(self, "Error", error_message, QMessageBox.Ok)
            else:
                self.weather_data = data['current']
                self.forecast_data = data['forecast']['forecastday']
                self.display_weather_info()
                self.display_forecast()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error fetching weather: {str(e)}", QMessageBox.Ok)

    def refresh_weather(self):
        if self.weather_data:
            self.display_weather_info()
        if self.forecast_data:
            self.display_forecast()

    def display_weather_info(self):
        temperature = self.weather_data['temp_c']
        humidity = self.weather_data['humidity']
        wind_speed = self.weather_data['wind_kph']
        weather_desc = self.weather_data['condition']['text']
        icon_url = "http:" + self.weather_data['condition']['icon']
        
        pixmap = QPixmap()
        icon_data = requests.get(icon_url).content
        pixmap.loadFromData(icon_data)
        self.weather_icon_label.setPixmap(pixmap)
        self.weather_icon_label.setScaledContents(True)

        units = self.units_combo.currentText()
        if units == "Celsius":
            temperature_label = f"Temperature: {temperature}°C"
        else:
            temperature = self.weather_data['temp_f']
            temperature_label = f"Temperature: {temperature}°F"

        detailed_weather_info = f'Description: {weather_desc}\n' \
                                f'Wind Speed: {wind_speed} km/h\n' \
                                f'Humidity: {humidity}%'

        self.weather_info_label.setText(f"{temperature_label}\n{detailed_weather_info}")

    def display_forecast(self):
        forecast_info = "Forecast:\n"
        for day in self.forecast_data:
            date = day['date']
            max_temp = day['day']['maxtemp_c']
            min_temp = day['day']['mintemp_c']
            weather_desc = day['day']['condition']['text']
            forecast_info += f"{date} - Max Temp: {max_temp}°C, Min Temp: {min_temp}°C, {weather_desc}\n"
        self.forecast_label.setText(forecast_info)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
