import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer
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

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_weather)
        self.layout.addWidget(self.refresh_button)

        self.alerts_label = QLabel()
        self.layout.addWidget(self.alerts_label)

        self.setLayout(self.layout)

        self.api_key = '78b743af83a34fc78ce160059242102'
        self.weather_data = None
        self.alerts_data = None

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alerts)
        self.timer.start(600000)  # Check for alerts every 10 minutes (600000 milliseconds)

    def get_weather(self):
        city = self.city_entry.text()
        units = self.units_combo.currentText().lower()
        url = f'http://api.weatherapi.com/v1/current.json?key={self.api_key}&q={city}&aqi=no&units={units}'

        try:
            response = requests.get(url)
            data = response.json()
            if 'error' in data:
                error_message = data['error']['message']
                QMessageBox.warning(self, "Error", error_message, QMessageBox.Ok)
            else:
                self.weather_data = data
                self.display_weather_info()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error fetching weather: {str(e)}", QMessageBox.Ok)

    def refresh_weather(self):
        if self.weather_data:
            self.display_weather_info()

    def check_alerts(self):
        if self.weather_data:
            city = self.city_entry.text()
            url = f'http://api.weatherapi.com/v1/alert.json?key={self.api_key}&q={city}'

            try:
                response = requests.get(url)
                data = response.json()
                if 'error' in data:
                    error_message = data['error']['message']
                    QMessageBox.warning(self, "Error", error_message, QMessageBox.Ok)
                else:
                    self.alerts_data = data
                    self.display_alerts()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error fetching alerts: {str(e)}", QMessageBox.Ok)

    def display_weather_info(self):
        temperature = self.weather_data['current']['temp_c']
        weather_desc = self.weather_data['current']['condition']['text']
        icon_url = "http:" + self.weather_data['current']['condition']['icon']
        
        pixmap = QPixmap()
        icon_data = requests.get(icon_url).content
        pixmap.loadFromData(icon_data)
        self.weather_icon_label.setPixmap(pixmap)
        self.weather_icon_label.setScaledContents(True)

        units = self.units_combo.currentText()
        if units == "Celsius":
            temperature_label = f"Temperature: {temperature}°C"
        else:
            temperature = self.weather_data['current']['temp_f']
            temperature_label = f"Temperature: {temperature}°F"

        detailed_weather_info = f'Description: {weather_desc}\n' \
                                f'Wind: {self.weather_data["current"]["wind_kph"]} km/h\n' \
                                f'Humidity: {self.weather_data["current"]["humidity"]}%'

        self.weather_info_label.setText(f"{temperature_label}\n{detailed_weather_info}")

    def display_alerts(self):
        alerts = self.alerts_data['alerts']
        if alerts:
            alert_messages = "\n".join([alert['description'] for alert in alerts])
            self.alerts_label.setText(f"Weather Alerts:\n{alert_messages}")
        else:
            self.alerts_label.setText("No weather alerts")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())
