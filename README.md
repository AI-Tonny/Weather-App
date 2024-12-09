# 🌤️ Weather App

## 🌟 Overview
Weather App is a Python application that provides real-time weather information for a specified city, as well as a 1-5 day forecast. The program can also display a graphical representation of temperature forecasts and manage a list of favorite cities.

## 🚀 Features
- **🌞 Current Weather**: Get detailed information about the current weather for a specific city.
- **📅 Forecast**: Receive a 1-5 day weather forecast, including graphical temperature charts.
- **❤️ Favorite Cities**: Add, view, and remove cities from your list of favorite locations.
- **💾 Data Storage**: Store favorite cities in a local JSON file for persistent access.
- **📊 Graphical Display**: Visualize temperature trends using Matplotlib.

## 🛠️ Requirements
To run the application, ensure you have the following installed:
- Python 3.9+
- Required Python libraries:
  - `requests` 📦
  - `matplotlib` 📊
  - `json` 🗂️
  - `os` 🖥️
  - `dotenv` (optional, for managing API keys) 🔐

You can install the dependencies by running:
```bash
pip install requests matplotlib python-dotenv
```

## 🗝️ How to get an API key on OpenWeather:
- 🌐 Go to the OpenWeather website.
- 📝 Register or log in to your account.
- 🔑 Go to API Keys section.
- ➕ Click Generate Key to create a new API key.
- 📋 Copy the key and use it in your code.

## 💡 How to Use:
Run the script in your terminal.

Choose an option from the menu:

Get current weather.

Get a forecast for 1-5 days.

Manage your favorite cities.

Enter a city name to receive weather information.

Optionally, visualize the temperature forecast in a graphical chart.

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
