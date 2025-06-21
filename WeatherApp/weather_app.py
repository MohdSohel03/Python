
# === Weather App with Dark Mode and GUI ===
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
import pyttsx3
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from plyer import notification
import os

# === CONFIG ===
API_KEY = "9a15504fef0640b59d4e473af4c6a64c"  # <- Insert your OpenWeatherMap API key
AUTO_REFRESH_MINUTES = 2
ICON_PATH = "icons"
# ==============

engine = pyttsx3.init()
voices = engine.getProperty('voices')
languages = {
    "Female": voices[1].id if len(voices) > 1 else voices[0].id,
    "Male": next((v.id for v in voices if 'male' in v.name.lower()), voices[0].id),
}

dark_mode = False
last_report = ""

def speak(text, lang_id):
    engine.setProperty('voice', lang_id)
    engine.say(text)
    engine.runAndWait()

def get_weather_data(city):
    return requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric").json()

def get_forecast_data(city):
    return requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric").json()

def show_icon(condition):
    icon_file = os.path.join(ICON_PATH, f"{condition.lower()}.png")
    if os.path.exists(icon_file):
        img = Image.open(icon_file).resize((60, 60))
        photo = ImageTk.PhotoImage(img)
        weather_icon_label.config(image=photo)
        weather_icon_label.image = photo
    else:
        weather_icon_label.config(image='')

def generate_graph(forecast):
    temps = [item["main"]["temp"] for item in forecast["list"][:6]]
    times = [item["dt_txt"][11:16] for item in forecast["list"][:6]]

    plt.figure(figsize=(5, 3))
    plt.plot(times, temps, marker='o', color='skyblue')
    plt.title("Upcoming Temperatures")
    plt.xlabel("Time")
    plt.ylabel("Temp (°C)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("forecast.png")
    plt.close()

    img = Image.open("forecast.png").resize((300, 180))
    photo = ImageTk.PhotoImage(img)
    forecast_img_label.config(image=photo)
    forecast_img_label.image = photo

def fetch_weather():
    global last_report
    city = city_entry.get().strip()
    if not city:
        messagebox.showerror("Input Error", "Please enter a city name.")
        return

    lang = lang_var.get()
    lang_id = languages.get(lang, voices[0].id)

    weather = get_weather_data(city)
    forecast = get_forecast_data(city)

    if weather.get("cod") != 200 or forecast.get("cod") != "200":
        messagebox.showerror("Error", "Failed to fetch weather.")
        return

    now = datetime.now().strftime("%d-%b-%Y %I:%M %p")
    result = (
        f"📍 {weather['name']}, {weather['sys']['country']}\n"
        f"🕒 Last Updated: {now}\n"
        f"🌡 Temp: {weather['main']['temp']}°C | Feels Like: {weather['main']['feels_like']}°C\n"
        f"💧 Humidity: {weather['main']['humidity']}%\n"
        f"🌬 Wind: {weather['wind']['speed']} m/s\n"
        f"🌥 Description: {weather['weather'][0]['description'].title()}\n"
    )

    forecast_text = "\n📅 Forecast:\n"
    for item in forecast["list"][:3]:
        forecast_text += (
            f"{item['dt_txt'][:16]} - "
            f"{item['weather'][0]['description'].title()} - "
            f"{item['main']['temp']}°C\n"
        )

    full_report = result + forecast_text
    output_text.config(state='normal')
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, full_report)
    output_text.config(state='disabled')
    last_report = full_report

    speak(f"Weather in {weather['name']}: {weather['weather'][0]['description']}, {weather['main']['temp']}°C", lang_id)
    speak("Forecast loaded.", lang_id)

    show_icon(weather["weather"][0]["main"])
    generate_graph(forecast)

    notification.notify(
        title=f"Weather Update – {weather['name']}",
        message=f"{weather['weather'][0]['description'].title()}, {weather['main']['temp']}°C",
        timeout=5
    )

    root.after(AUTO_REFRESH_MINUTES * 60 * 1000, fetch_weather)

def toggle_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg = "#1e1e1e" if dark_mode else "#ffffff"
    fg = "#ffffff" if dark_mode else "#000000"
    text_bg = "#2e2e2e" if dark_mode else "#f0f0f0"
    root.configure(bg=bg)
    for widget in root.winfo_children():
        try:
            widget.configure(bg=bg, fg=fg)
        except:
            pass
    output_text.configure(bg=text_bg, fg=fg)

# === GUI SETUP ===
root = tk.Tk()
root.title("🌤 Weather App")
root.geometry("560x710")
style = ttk.Style(root)
style.theme_use("clam")

tk.Label(root, text="🌍 Weather App + Dark Mode", font=("Segoe UI", 15, "bold")).pack(pady=10)

frame = ttk.Frame(root)
frame.pack(pady=5)

ttk.Label(frame, text="City:").grid(row=0, column=0, sticky="e")
city_entry = ttk.Entry(frame, width=30)
city_entry.grid(row=0, column=1)

ttk.Label(frame, text="Language:").grid(row=1, column=0, sticky="e")
lang_var = tk.StringVar(value="English")
lang_menu = ttk.Combobox(frame, textvariable=lang_var, values=list(languages.keys()), state="readonly", width=28)
lang_menu.grid(row=1, column=1)

ttk.Button(root, text="🔍 Get Weather", command=fetch_weather).pack(pady=5)
ttk.Button(root, text="🌓 Toggle Mode", command=toggle_mode).pack(pady=5)

output_text = tk.Text(root, height=10, width=64, font=("Consolas", 10), wrap=tk.WORD, bg="#f0f0f0")
output_text.pack(pady=10)
output_text.config(state='disabled')

weather_icon_label = tk.Label(root)
weather_icon_label.pack(pady=4)

forecast_img_label = tk.Label(root)
forecast_img_label.pack()

tk.Label(root, text="© 2025 Mohd Sohel Ansari || Weather via OpenWeatherMap", font=("Segoe UI", 9), fg="#555").pack(pady=10)

root.mainloop()
