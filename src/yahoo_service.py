import urllib
import urllib2
import os
import sys
import pickle
import xml.dom.minidom as minidom

from utils import compute_wind

code_icon_dict = {
	0  : "yahoo00",
        1  : "yahoo00",
	2  : "yahoo00",
	3  : "yahoo00",
	4  : "yahoo00",
	5  : "yahoo02",
	6  : "yahoo13",
	7  : "yahoo13",
	8  : "yahoo25",
	9  : "yahoo25",
	10 : "yahoo22",
	11 : "yahoo25",
	12 : "yahoo22",
	13 : "yahoo03",
	14 : "yahoo05",
	15 : "yahoo16",
	16 : "yahoo05",
	17 : "yahoo00",
	18 : "yahoo05",
	19 : "yahoo15",
	20 : "yahoo17",
	21 : "yahoo15",
	22 : "yahoo15",
	23 : "yahoo09",
	24 : "yahoo09",
	25 : "yahoo16",
	26 : "yahoo10",
	27 : "yahoo12",
	28 : "yahoo04",
	29 : "yahoo12",
	30 : "yahoo04",
	31 : "yahoo01",
	32 : "yahoo06",
	33 : "yahoo18",
	34 : "yahoo11",
	35 : "yahoo00",
	36 : "yahoo06",
	37 : "yahoo07",
	38 : "yahoo07",
	39 : "yahoo20",
	40 : "yahoo22",
	41 : "yahoo05",
	42 : "yahoo05",
	43 : "yahoo05",
	44 : "yahoo12",
	45 : "yahoo21",
	46 : "yahoo05",
	47 : "yahoo08",
	3200:"yahoo19"
    }

appid = "2N_GGsDV34GK3j0N1YAgVx3t6fV0Ovoy79u93JL33EfydDcDlie04jiSHa5bqTjO208-"


def get_woeid_by_place(place):
    '''
    docs
    '''
    try:
        yql = 'select woeid from geo.places where text = "' + place + '"'
        quoted_yql = urllib.quote_plus(yql.decode(sys.stdin.encoding).encode('utf8'))
        xml_str = urllib.urlopen("http://query.yahooapis.com/v1/public/yql?q=" + quoted_yql).read()
        
        dom = minidom.parseString(xml_str)
        root = dom.documentElement
        woeid_ele_list = root.getElementsByTagName("woeid")
        if len(woeid_ele_list) == 1:
            return [woeid_ele_list[0].childNodes[0].nodeValue]
        else:
            return [woeid_ele.childNodes[0].nodeValue for woeid_ele in woeid_ele_list]
        
    except Exception, e:
        print e
        return None
    
    
def get_weather_information_by_woeid(woeid, place):
    '''
    docs
    '''
    try:
        url_str = "http://weather.yahooapis.com/forecastrss?w=" + woeid + "&u=c"
        xml_str = urllib.urlopen(url_str).read()
        
        dom = minidom.parseString(xml_str)
        root = dom.documentElement
        weather_condition_ele = root.getElementsByTagName("yweather:condition")[0]
        weather_condition = {}
        weather_condition["text"] = weather_condition_ele.getAttribute("text")
        weather_condition["code"] = weather_condition_ele.getAttribute("code")
        weather_condition["temp"] = weather_condition_ele.getAttribute("temp") + u"\u2103" 
        weather_condition["pic"] = code_icon_dict[int(weather_condition["code"])]
        
        weather_wind_ele = root.getElementsByTagName("yweather:wind")[0]
        wind_direction = weather_wind_ele.getAttribute("direction")
        wind_speed = weather_wind_ele.getAttribute("speed")
        weather_condition["wind"] = compute_wind(wind_speed, wind_direction)

        weather_atmosphere_ele = root.getElementsByTagName("yweather:atmosphere")[0]
        weather_condition["humidity"] = weather_atmosphere_ele.getAttribute("humidity")
        weather_condition["visibility"] = weather_atmosphere_ele.getAttribute("visibility")
        if weather_condition["visibility"] == u"":
            weather_condition["visibility"] = "Unknown"
        
        weather_forecast_eles = root.getElementsByTagName("yweather:forecast")
        for index, ele in enumerate(weather_forecast_eles):
            index += 1
            weather_condition["forecast" + str(index)] = {}
            weather_condition["forecast" + str(index)]["low"] = ele.getAttribute("low")
            weather_condition["forecast" + str(index)]["high"] = ele.getAttribute("high") + u"\u2103"
            weather_condition["forecast" + str(index)]["text"] = ele.getAttribute("text")
            weather_condition["forecast" + str(index)]["code"] = ele.getAttribute("code")
            weather_condition["forecast" + str(index)]["pic"] = code_icon_dict[int(ele.getAttribute("code"))]
        
        weather_condition["woeid"] = woeid        
        weather_condition["location"] = place

        config_dir = os.path.expanduser(r"~/.config/deepin-weather/")
        weather_info_file = open(config_dir + "weather_info_file", "w")
        pickle.dump(weather_condition, weather_info_file)
        weather_info_file.close()
        return weather_condition
    except Exception, e:
        print e
        return None

def get_place_by_woeid(woeid):
    '''
    docs
    '''
    try:
        url_str = "http://where.yahooapis.com/v1/place/" + woeid + "?appid=" + appid
        # i'm so proud of myself that i finally found out the problem and solved it :-)
        rq = urllib2.Request(url_str)
        rq.add_header("Accept-Language", "zh-CN,zh;q=0.8")
        xml_str = urllib2.urlopen(rq).read()

        dom = minidom.parseString(xml_str)
        root = dom.documentElement
        place_dict = {
            "country" : "",
            "admin1" : "",
            "admin2" : "",
            "admin3" : "",
            "locality1" : ""
            }
        if(root.getElementsByTagName("country")[0].childNodes):
            place_dict["country"] = root.getElementsByTagName("country")[0].childNodes[0].nodeValue
        if(root.getElementsByTagName("admin1")[0].childNodes):
            place_dict["admin1"] = root.getElementsByTagName("admin1")[0].childNodes[0].nodeValue
        if(root.getElementsByTagName("admin2")[0].childNodes):
            place_dict["admin2"] = root.getElementsByTagName("admin2")[0].childNodes[0].nodeValue
        if(root.getElementsByTagName("admin3")[0].childNodes):
            place_dict["admin3"] = root.getElementsByTagName("admin3")[0].childNodes[0].nodeValue
        if(root.getElementsByTagName("locality1")[0].childNodes):
            place_dict["locality1"] = root.getElementsByTagName("locality1")[0].childNodes[0].nodeValue

        place_dict["all"] = place_dict["country"] + place_dict["admin1"] + place_dict["admin2"] + \
            (place_dict["locality1"] if place_dict["locality1"] else place_dict["admin3"])
        
        return place_dict
    except Exception, e:
        print e
        return None    
