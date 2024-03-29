import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
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

        self.get_weather_button = QPushButton("Get Weather")
        self.get_weather_button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.get_weather_button)

        self.weather_label = QLabel()
        self.layout.addWidget(self.weather_label)

        self.setLayout(self.layout)

    def get_weather(self):
        city = self.city_entry.text()
        api_key = '78b743af83a34fc78ce160059242102'
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'

        try:
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                error_message = data['error']['message']
                QMessageBox.warning(self, "Error", error_message, QMessageBox.Ok)
            else:
                temperature = data['current']['temp_c']
                weather_desc = data['current']['condition']['text']
                self.weather_label.setText(f'Temperature: {temperature}°C\nDescription: {weather_desc}')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error fetching weather: {str(e)}", QMessageBox.Ok)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
