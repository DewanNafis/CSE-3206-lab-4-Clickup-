# Weather Notification System

A Python application demonstrating **Observer** and **Adapter** design patterns. The app fetches real-time weather data from Open-Meteo API and notifies multiple display systems.

## Design Patterns Used

### 1. **Observer Pattern**
- **Purpose**: Allows multiple displays to receive weather updates automatically
- **Components**:
  - `Subject`: `WeatherStation` - manages observers and notifies them of weather changes
  - `Observer`: Abstract base class for all displays
  - `ConcreteObservers`: `ConsoleDisplay`, `EmojiDisplay`

**Benefits**: 
- ✅ Easy to add new displays without modifying existing code
- ✅ Loose coupling between weather service and display systems
- ✅ One-to-many dependency management

### 2. **Adapter Pattern**
- **Purpose**: Adapts Open-Meteo API response to our application's simple format
- **Components**:
  - `WeatherAdapter` - converts external API JSON structure to our internal format

**Benefits**:
- ✅ Can easily switch to different weather APIs
- ✅ Standardized data format across the application
- ✅ External API changes don't affect display code

## Project Structure

```
CSE3206_lab4/
│
├── main.py                 # Complete application (all-in-one)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Setup Instructions

### 1. Clone or Download the Project

```bash
cd "e:\RUET\3.2\CSE 3206\CSE3206_lab4"
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
```

**Activate virtual environment:**
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## Usage

1. Run the application
2. Enter a city name when prompted
3. View weather data in multiple formats:
   - 📺 **Console Display**: Standard terminal output
   - 🌤️ **Emoji Display**: Visual emoji-based display

## Adding New Displays

The Observer pattern makes it incredibly easy to add new display types:

```python
# Add to main.py
class FileLogger(Observer):
    def update(self, weather_data):
        with open('weather.log', 'a') as f:
            f.write(f"{weather_data['city']}: {weather_data['temp']}°C\n")
        print("\n📁 [File Logger] Data saved to weather.log")

# In main() function
station.add_observer(FileLogger())
```

## Example Output

```
Enter city name: London

[Console Display]
City: London
Temp: 12.5°C
Wind: 4.2 m/s

🌤️  [Emoji Display]
🌍 London
🌡️ 12.5°C
💨 4.2 m/s
```

## API Information

**APIs Used**: 
1. [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) - Convert city name to coordinates
2. [Open-Meteo Weather API](https://open-meteo.com/en/docs) - Fetch current weather data

**Features**:
- Current temperature
- Wind speed
- No API key required! 
- Free unlimited access

**How it works:**
1. `WeatherAPI.get_coordinates(city)` → Gets latitude/longitude from city name
2. `WeatherAPI.get_weather(lat, lon)` → Fetches weather data using coordinates
3. `WeatherAdapter.adapt()` → Converts API JSON to simple format

## Dependencies

- `requests` (2.31.0): HTTP library for API calls

## License

This project is for educational purposes (CSE 3206 Lab 4).

## Author

RUET CSE 3.2 - CSE 3206 Lab Assignment
