# Weather Notification System

A Python application demonstrating **Observer** and **Adapter** design patterns. The app fetches real-time weather data from Open-Meteo API and displays it through multiple notification systems.

## 🎯 Design Patterns Used

### 1. **Observer Pattern** (Lines 24-61)
**Purpose**: Enables multiple displays to automatically receive weather updates when data changes.

**Components**:
- **Subject**: `WeatherStation` - Manages observers and broadcasts notifications
- **Observer**: Abstract base class defining the `update()` interface
- **Concrete Observers**: 
  - `ConsoleDisplay` - Standard text output
  - `EmojiDisplay` - Visual emoji-based display

**Benefits**: 
- ✅ Add new displays without modifying existing code
- ✅ Loose coupling between weather service and displays
- ✅ Automatic notification to all registered observers
- ✅ One-to-many dependency management

**Code Location**:
```python
# Subject (lines 48-61)
class WeatherStation:
    def add_observer(self, obs):
        self.observers.append(obs)
    
    def notify(self, data):
        for obs in self.observers:
            obs.update(data)

# Observers (lines 24-46)
class ConsoleDisplay(Observer):
    def update(self, weather_data):
        # Display logic here
```

### 2. **Adapter Pattern** (Lines 7-21)
**Purpose**: Converts Open-Meteo API's complex JSON structure into a simple, standardized format.

**Components**:
- **Target Interface**: Our simple weather data format (dict with city, temp, wind)
- **Adaptee**: Open-Meteo API with complex nested JSON structure
- **Adapter**: `WeatherAdapter.adapt()` method

**Benefits**:
- ✅ Easily switch to different weather APIs (just create new adapter)
- ✅ Standardized data format across the application
- ✅ External API changes isolated from display code
- ✅ Simplifies complex API responses

**Code Location**:
```python
# Adapter (lines 7-21)
class WeatherAdapter:
    @staticmethod
    def adapt(api_response, city):
        current = api_response["current_weather"]
        return {
            "city": city,
            "temp": current["temperature"],
            "wind": current["windspeed"]
        }
```

## 📂 Project Structure

```
CSE3206_lab4/
│
├── main.py              # Complete application (all-in-one file)
├── requirements.txt     # Python dependencies (requests)
├── .gitignore          # Git ignore rules
└── README.md           # This documentation
```

## 🚀 Setup Instructions

### 1. Clone or Download the Project

```powershell
cd "e:\RUET\3.2\CSE 3206\CSE3206_lab4"
```

### 2. Create Virtual Environment (Optional but Recommended)

```powershell
python -m venv venv
```

**Activate virtual environment:**
- **Windows PowerShell**: `.\venv\Scripts\Activate.ps1`
- **Windows CMD**: `venv\Scripts\activate.bat`
- **Linux/Mac**: `source venv/bin/activate`

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- `requests==2.31.0` - For making HTTP API calls

### 4. Run the Application

```powershell
python main.py
```

## Usage

1. Run the application
2. Enter a city name when prompted
3. View weather data in multiple formats:
   - 📺 **Console Display**: Standard terminal output
   - 🌤️ **Emoji Display**: Visual emoji-based display

## ➕ Adding New Displays (Observer Pattern)

The Observer pattern makes it incredibly easy to add new notification types without modifying existing code!

### Example 1: File Logger
```python
# Add to main.py after EmojiDisplay class
class FileLogger(Observer):
    def update(self, weather_data):
        with open('weather.log', 'a') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {weather_data['city']}: {weather_data['temp']}°C, {weather_data['wind']} m/s\n")
        print("\n📁 [File Logger] Data saved to weather.log")

# In main() function
station.add_observer(FileLogger())
```

### Example 2: SMS Notifier
```python
class SMSNotifier(Observer):
    def __init__(self, phone_number):
        self.phone_number = phone_number
    
    def update(self, weather_data):
        message = f"{weather_data['city']}: {weather_data['temp']}°C"
        print(f"\n📱 [SMS] Sent to {self.phone_number}: {message}")

# In main() function
station.add_observer(SMSNotifier("+1234567890"))
```

### Example 3: JSON API Webhook
```python
import requests

class WebhookNotifier(Observer):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
    
    def update(self, weather_data):
        requests.post(self.webhook_url, json=weather_data)
        print(f"\n🌐 [Webhook] Data sent to {self.webhook_url}")

# In main() function
station.add_observer(WebhookNotifier("https://example.com/webhook"))
```

**That's it!** No need to modify `WeatherStation`, `WeatherAPI`, or `WeatherAdapter` classes. Just create a new Observer and register it! 🎉

## 💻 Example Output

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

### Testing Different Cities
```
Enter city name: Tokyo

[Console Display]
City: Tokyo
Temp: 18.3°C
Wind: 3.1 m/s

🌤️  [Emoji Display]
🌍 Tokyo
🌡️ 18.3°C
💨 3.1 m/s
```

## 🌐 API Information

### APIs Used (No Key Required!)

**1. Open-Meteo Geocoding API** (Line 71-77)
- **URL**: `https://geocoding-api.open-meteo.com/v1/search?name={city}`
- **Purpose**: Converts city name to latitude/longitude coordinates
- **Example Response**:
  ```json
  {
    "results": [
      {"latitude": 51.5074, "longitude": -0.1278, "name": "London"}
    ]
  }
  ```

**2. Open-Meteo Weather API** (Line 79-86)
- **URL**: `https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true`
- **Purpose**: Fetches current weather data for given coordinates
- **Example Response**:
  ```json
  {
    "current_weather": {
      "temperature": 15.2,
      "windspeed": 12.5
    }
  }
  ```

### API Call Flow

```
User Input: "London"
    ↓
1. WeatherAPI.get_coordinates("London")  [Line 71]
    → API Call to Geocoding API
    → Returns: (51.5074, -0.1278)
    ↓
2. WeatherAPI.get_weather(51.5074, -0.1278)  [Line 79]
    → API Call to Weather API
    → Returns: {"current_weather": {...}}
    ↓
3. WeatherAdapter.adapt(api_response, "London")  [Line 14]
    → Converts: {"temperature": 15.2, "windspeed": 12.5}
    → To: {"city": "London", "temp": 15.2, "wind": 12.5}
    ↓
4. WeatherStation.notify(weather_data)  [Line 58]
    → Notifies all observers (ConsoleDisplay, EmojiDisplay)
```

**Advantages**:
- ✅ No API key required
- ✅ Free unlimited access
- ✅ Fast and reliable
- ✅ Simple JSON responses

## 📦 Dependencies

- **requests** (2.31.0) - HTTP library for making API calls to Open-Meteo services

## 🎓 Educational Purpose

This project demonstrates practical implementation of design patterns for **CSE 3206 Lab 4** at Rajshahi University of Engineering & Technology (RUET).

### Learning Objectives
✅ Understanding Observer Pattern for event-driven programming  
✅ Implementing Adapter Pattern for API integration  
✅ Working with RESTful APIs  
✅ Writing clean, maintainable Python code  
✅ Separation of concerns and SOLID principles  

## 🔧 Troubleshooting

**Issue**: City not found  
**Solution**: Try different spelling or use major city names (e.g., "New York", "London", "Tokyo")

**Issue**: Network error  
**Solution**: Check your internet connection. The app requires internet to fetch weather data.

**Issue**: Import error for requests  
**Solution**: Run `pip install -r requirements.txt` to install dependencies

## 📝 Code Structure Overview

| Lines | Component | Pattern | Description |
|-------|-----------|---------|-------------|
| 7-21 | `WeatherAdapter` | Adapter | Converts API JSON to simple format |
| 24-46 | `Observer`, `ConsoleDisplay`, `EmojiDisplay` | Observer | Notification displays |
| 48-61 | `WeatherStation` | Observer | Subject managing observers |
| 64-86 | `WeatherAPI` | - | API integration layer |
| 89-115 | `main()` | - | Application entry point |

## 👨‍💻 Author

**RUET CSE 3.2** - CSE 3206 Software Engineering Lab Assignment

## 📄 License

This project is for educational purposes only.
