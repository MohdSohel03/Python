# 🌦️ Weather App – Dark Mode, Voice Output & Forecast Graph

A modern desktop weather application built with **Python** and **Tkinter**, featuring:

- 🌐 Live weather updates using OpenWeatherMap API
- 🌗 Light & Dark mode toggle
- 🔊 Voice weather narration using `pyttsx3`
- 📈 Forecast graph using `matplotlib`
- 🖼 Weather icons & forecast images
- 🔔 Desktop notifications via `plyer`
- 📦 Responsive GUI using `ttk` & `Pillow`

---

## 📸 Preview

[City: Mumbai]
🌡 Temp: 32°C | Feels Like: 35°C
💧 Humidity: 70% 🌬 Wind: 3.5 m/s
🌥 Description: Light Rain

📅 Forecast:
14:00 - Light Rain - 31°C
17:00 - Overcast Clouds - 30°C
20:00 - Clear Sky - 28°C

---

## 🛠 Requirements

Install all necessary libraries with:

```bash
pip install requests pyttsx3 pillow matplotlib plyer

## 📁 Project Structure

weather-app/
├── weather_app.py
├── icons/
│   ├── clear.png
│   ├── clouds.png
│   ├── rain.png
│   └── ...
├── forecast.png           # Auto-generated forecast chart
├── README.md

## 🧠 Features

| Feature            | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| 🔎 Search City     | Get real-time weather data by typing a city name                 |
| 📢 Voice Assistant | Speaks out current weather and forecast                          |
| 🌓 Dark Mode       | Toggle light/dark theme with a button                            |
| 📈 Forecast Graph  | Shows next 6 weather points in line chart (temp vs time)         |
| 📬 Notifications   | Pops up OS-level weather alerts                                  |
| 🖼 Weather Icons   | Displays icon based on current condition (optional icons folder) |

1. ▶️ How to Run
Replace the API key at the top of the file:
API_KEY = "your_openweathermap_api_key"

2. Run the Python script:
python weather_app.py

## 🗣 Voice Options
Choose between Male or Female voice in the dropdown.
Uses your system's TTS engine via pyttsx3.

## 🌩 Supported Weather Icons
You can place weather condition icons in the icons/ folder with names like:

-clear.png
-rain.png
-clouds.png
-snow.png
-mist.png

These will appear next to the weather report.

## 🙋‍♂️ Contact

**Developer**: Mohd Sohel Ansari  
**Email**: Uplaoding Soon  
**GitHub**: https://github.com/MohdSohel03

## 📜 License
This project is open-source under the MIT License