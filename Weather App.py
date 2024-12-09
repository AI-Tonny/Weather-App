import requests
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import json
import os

load_dotenv()

API_KEY: str = os.getenv("API_KEY")
BASE_URL: str = os.getenv("BASE_URL")


def ShowMenu() -> None:
    """
    Displays the program's main menu.
    """
    print("Menu.")
    print("1. Get current weather for city")
    print("2. Get future weather for city")
    print("3. Show weather in favorite cities")
    print("4. Add city to favorites")
    print("5. Remove city from favorites")
    print("6. Exit")


def load_favorites(filename: str = "favorites.json") -> list[str]:
    """
    Loads the list of favorite cities from a file.

    Args:
        filename (str): The name of the file containing favorite cities.

    Returns:
        list[str]: A list of favorite cities.
    """
    if os.path.exists(filename):
        try:
            with open(filename, "r") as jsonF:
                return json.load(jsonF)
        except json.decoder.JSONDecodeError:
            return []
    return []


def save_favorites(cities: list[str], filename: str = "favorites.json") -> None:
    """
    Saves the list of favorite cities to a file.

    Args:
        cities (list[str]): The list of favorite cities.
        filename (str): The name of the file to save the cities.
    """
    if not os.path.exists(filename):
        print(f"A file \"{filename}\" has been created to record favorite cities.")

    with open(filename, "w") as jsonF:
        json.dump(cities, jsonF)


def get_city(message: str = "Enter city") -> str:
    """
    Prompts the user to enter a city name with input validation.

    Args:
        message (str): The message displayed to the user.

    Returns:
        str: The entered city name.
    """
    city: str = input(message)
    if city and not city.isspace():
        return city

    print("The city is entered incorrectly, try again.")
    return get_city(message)


def get_days() -> int:
    """
    Prompts the user to enter the number of days for the weather forecast (1-5).

    Returns:
        int: The number of days.
    """
    try:
        days: int = int(input("How many days do you want to receive a forecast for? (1-5): "))

        if not 1 <= days <= 5:
            print("Please enter a valid day within(1-5).")
            return get_days()

        return days
    except ValueError:
        print("Please enter a valid day within (1-5).")
        return get_days()


def plot_temperature_forecast(dates: list[str], temperatures: list[float]) -> None:
    """
    Plots a temperature forecast over multiple days.

    Args:
        dates (list[str]): List of dates.
        temperatures (list[float]): List of temperatures.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker="o", linestyle="-", color="blue")
    plt.title("Temperature Forecast")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def getCurrentWeather(city: str) -> dict:
    """
    Retrieves the current weather data for a given city.

    Args:
        city (str): The name of the city.

    Returns:
        dict: Weather data or an error message.
    """
    params: dict = {"q": city, "appid": API_KEY, "units": "metric", "lang": "en"}
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"City \"{city}\" not found. Status code: {response.status_code}"}


def getFutureWeather(city: str, days: int = 5) -> dict:
    """
    Retrieves the weather forecast for a city over a given number of days.

    Args:
        city (str): The name of the city.
        days (int): The number of days (1-5).

    Returns:
        dict: Weather forecast data or an error message.
    """
    FORECAST_URL: str = os.getenv("FORECAST_URL")
    params: dict = {"q": city, "appid": API_KEY, "cnt": days*8, "units": "metric", "lang": "en"}
    response = requests.get(FORECAST_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return {"error": f"City \"{city}\" not found. Status code: {response.status_code}"}


def displayCurrentWeather(data: dict) -> None:
    """
    Displays current weather data for a city.

    Args:
        data (dict): The weather data.
    """
    if "error" in data:
        print(data["error"])
        return

    city: str = data["name"].capitalize()
    weather: str = data["weather"][0]["description"].capitalize()
    temp: str = data["main"]["temp"]
    temp_min: str = data["main"]["temp_min"]
    temp_max: str = data["main"]["temp_max"]
    feels_like: str = data["main"]["feels_like"]
    humidity: str = data["main"]["humidity"]
    wind_speed: str = data["wind"]["speed"]
    wind_deg: str = data["wind"]["deg"]
    sea_level: str = data["main"]["sea_level"]
    pressure: str = data["main"]["pressure"]

    print(f"\n--- Weather in {city} ---")
    print(f"Description: {weather}")
    print(f"Temperature: {temp}°C")
    print(f"Temperature min: {temp_min}°C")
    print(f"Temperature max: {temp_max}°C")
    print(f"Feels like: {feels_like}°C")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"Wind deg: {wind_deg}°")
    print(f"Sea level: {sea_level} hPa")
    print(f"Pressure: {pressure} hPa")


def displayFutureWeather(data: dict, days: int) -> None:
    """
    Displays the weather forecast for a city over multiple days.

    Args:
        data (dict): The weather forecast data.
        days (int): The number of forecast days.
    """
    if "error" in data:
        print(data["error"], "\n")
        return

    print(f"\n--- {days}-Day Forecast for {data['city']['name'].capitalize()}---")
    for entry in data['list']:
        time: str = entry['dt_txt']
        temp: str = entry['main']['temp']
        humidity: str = entry['main']['humidity']
        wind_speed: str = entry['wind']['speed']
        desc: str = entry['weather'][0]['description'].capitalize()

        print(f"{time}: {temp}°C, {humidity}%, {wind_speed} m/s, {desc}")


def main() -> None:
    """
    Main function to run the weather application.
    """
    filename: str = "favorites.json"
    favorites: list[str] = load_favorites(filename)
    input(" === Weather App === ")

    ShowMenu()
    while (actionUser := input("\nYour choice: ")) != "6":
        match actionUser:
            case "1":
                city: str = get_city("Enter city: ")
                data: dict = getCurrentWeather(city)
                displayCurrentWeather(data)
            case "2":
                city: str = get_city("Enter city: ")
                days: int = get_days()
                data: dict = getFutureWeather(city, days)
                displayFutureWeather(data, days)

                if "error" not in data:
                    question: str = input("\nWould you like to see a graphical temperature chart (Y/N)? ").upper()
                    if question == "Y":
                        dates: list[str] = [entry["dt_txt"] for entry in data["list"]]
                        temperatures: list[float] = [entry["main"]["temp"] for entry in data["list"]]
                        plot_temperature_forecast(dates, temperatures)
            case "3":
                if not favorites:
                    print("No favorite places found.")
                    continue

                for city in favorites:
                    data: dict = getCurrentWeather(city)
                    displayCurrentWeather(data)
            case "4":
                city: str = get_city("Enter your favorite place: ")
                if city not in favorites:
                    data: dict = getCurrentWeather(city)
                    if "error" in data:
                        print(f"Favorite city \"{city}\" not found, try again.")
                        continue
                    favorites.append(city)
                    print(f"City \"{city}\" added to favorites.")
                else:
                    print(f"City \"{city}\" is already in your favorites list.")
            case "5":
                city: str = get_city("Enter your favorite location to delete: ")
                if city in favorites:
                    favorites.remove(city)
                    print(f"City \"{city}\" has been removed from favorites.")
                else:
                    print(f"City \"{city}\" is not in the favorites list.")
            case _:
                print("Invalid choice, please try again.")

    save_favorites(favorites, filename)
    print("Exiting...")


if __name__ == '__main__':
    main()
