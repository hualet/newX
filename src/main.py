import os
import sys
import pickle
import gtk
from weather_widget import WeatherPad
from utils import CONFIG_DIR as config_dir

import gettext
from gettext import gettext as _
gettext.bindtextdomain("newX", "../locale")
gettext.textdomain('newX')

if(not os.path.exists(config_dir)):
    os.makedirs(config_dir)
    open(config_dir + "weather_info_file", "w").close
elif not os.path.exists(config_dir + "weather_info_file"):
    open(config_dir + "weather_info_file", "w").close

weather_info_file = open(config_dir + r"weather_info_file")
file_content = weather_info_file.read()
weather_info_file.seek(0)
weather_info = {}
if(not file_content):
    weather_info["text"] = _("Unknown")
    weather_info["pic"] = "smile"
    weather_info["temp"] = ""
    weather_info["woeid"] = None
    weather_info["location"] = _("Location.")
    
    weather_info["wind"] = _("Unknown")
    weather_info["humidity"] = _("Unknown")
    weather_info["visibility"] = _("Unknown")

    weather_info["forecast1"] = {
        "low" : "",
        "high" : "",
        "text" : _("Unknown"),
        "code" : _("Unknown"),
        "pic" : "yahoo19"
        }
    weather_info["forecast2"] = weather_info["forecast3"] = weather_info["forecast4"] = weather_info["forecast5"] = weather_info["forecast1"]
else:    
    try:
        weather_info = pickle.load(weather_info_file)
        weather_info_file.close()
    except Exception:
        open(config_dir + "weather_info_file", "w").close
        sys.exit()

WeatherPad(weather_info)
gtk.main()
