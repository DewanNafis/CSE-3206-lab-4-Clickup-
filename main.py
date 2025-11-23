import requests

# ------------------------------------------------
#   ADAPTER PATTERN → Convert API JSON to our format
# ------------------------------------------------

class WeatherAdapter:
    @staticmethod
    def adapt(api_response, city):
        """Convert Open-Meteo response into simple internal structure."""
        current = api_response["current_weather"]
        return {
            "city": city,
            "temp": current["temperature"],
            "wind": current["windspeed"]
        }


# ------------------------------------------------
#   OBSERVER PATTERN
# ------------------------------------------------

class Observer:
    def update(self, weather_data):
        raise NotImplementedError


class ConsoleDisplay(Observer):
    def update(self, weather_data):
        print(f"\n[Console Display]")
        print(f"City: {weather_data['city']}")
        print(f"Temp: {weather_data['temp']}°C")
        print(f"Wind: {weather_data['wind']} m/s")


class EmojiDisplay(Observer):
    def update(self, weather_data):
        print("\n🌤️  [Emoji Display]")
        print(f"🌍 {weather_data['city']}")
        print(f"🌡️ {weather_data['temp']}°C")
        print(f"💨 {weather_data['wind']} m/s")


# ------------------------------------------------
#   SUBJECT (Observable)
# ------------------------------------------------

class WeatherStation:
    def __init__(self):
        self.observers = []

    def add_observer(self, obs):
        self.observers.append(obs)

    def notify(self, data):
        for obs in self.observers:
            obs.update(data)


# ------------------------------------------------
#   WEATHER SERVICE (API CALLS)
# ------------------------------------------------

class WeatherAPI:
    @staticmethod
    def get_coordinates(city):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
        res = requests.get(url).json()
        if "results" not in res:
            return None
        first = res["results"][0]
        return first["latitude"], first["longitude"]

    @staticmethod
    def get_weather(lat, lon):
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        return requests.get(url).json()


# ------------------------------------------------
#   MAIN PROGRAM
# ------------------------------------------------

def main():
    station = WeatherStation()

    # Add observers
    station.add_observer(ConsoleDisplay())
    station.add_observer(EmojiDisplay())

    city = input("Enter city name: ")

    coords = WeatherAPI.get_coordinates(city)
    if not coords:
        print("City not found!")
        return

    lat, lon = coords
    api_data = WeatherAPI.get_weather(lat, lon)

    # Adapt API response to internal format
    internal_data = WeatherAdapter.adapt(api_data, city)

    # Notify all observers
    station.notify(internal_data)


if __name__ == "__main__":
    main()
