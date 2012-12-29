import os
import pickle
import gtk
from weather_widget import WeatherPad

config_dir = os.path.expanduser(r"~/.config/deepin-weather/")
if(not os.path.exists(config_dir)):
    os.makedirs(config_dir)
    open(config_dir + "weather_info_file", "w").close

weather_info_file = open(config_dir + r"weather_info_file")
file_content = weather_info_file.read()
weather_info_file.seek(0)
weather_info = {}
if(not file_content):
    weather_info["text"] = "Unknown"
    weather_info["pic"] = "smile"
    weather_info["temp"] = ""
    weather_info["woeid"] = None
    weather_info["location"] = "Location."
    
    weather_info["wind"] = "Unknown"
    weather_info["humidity"] = "Unknown"
    weather_info["visibility"] = "Unknown"

    weather_info["forecast1"] = {
        "low" : "",
        "high" : "",
        "text" : "Unknown",
        "code" : "Unknown",
        "pic" : "yahoo19"
        }
    weather_info["forecast2"] = weather_info["forecast1"]
else:    
    weather_info = pickle.load(weather_info_file)
    weather_info_file.close()
# weather_info["from"] = "from_file"

WeatherPad(weather_info)
gtk.main()
