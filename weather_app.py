import tkinter as tk
from tkinter import messagebox
import requests

def get_weather(city_entry):
    city = city_entry.get()
    api_key = '78b743af83a34fc78ce160059242102'  # Replace 'YOUR_API_KEY' with your actual API key
    url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'

    try:
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            messagebox.showerror('Error', data['error']['message'])
        else:
            temperature = data['current']['temp_c']
            weather_desc = data['current']['condition']['text']
            messagebox.showinfo('Weather', f'Temperature: {temperature}°C\nDescription: {weather_desc}')
    except Exception as e:
        messagebox.showerror('Error', f'Error fetching weather: {str(e)}')


# Create the main window
root = tk.Tk()
root.title('Weather App')

# Create widgets
city_label = tk.Label(root, text='Enter city:')
city_label.pack()

city_entry = tk.Entry(root)
city_entry.pack()

get_weather_button = tk.Button(root, text='Get Weather', command=lambda: get_weather(city_entry))
get_weather_button.pack()


# Run the main event loop
root.mainloop()
