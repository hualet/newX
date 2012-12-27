import urllib
import os
import sys
import pickle
import xml.dom.minidom as minidom

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

def get_woeid_by_place(place):
    '''
    docs
    '''
    try:
        yql = 'select woeid from geo.places where text = "' + place + '"'
        print "yql : " + yql
        quoted_yql = urllib.quote_plus(yql.decode(sys.stdin.encoding).encode('utf8'))
        print "quoted_yql : " + quoted_yql
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
        print "url_str : " + url_str
        xml_str = urllib.urlopen(url_str).read()
        
        dom = minidom.parseString(xml_str)
        root = dom.documentElement
        weather_condition_ele = root.getElementsByTagName("yweather:condition")[0]
        weather_condition = {}
        weather_condition["text"] = weather_condition_ele.getAttribute("text")
        weather_condition["code"] = weather_condition_ele.getAttribute("code")
        weather_condition["temp"] = weather_condition_ele.getAttribute("temp") + u"\u2103" 
        weather_condition["pic"] = code_icon_dict[int(weather_condition["code"])]
        weather_condition["woeid"] = woeid        
        weather_condition["location"] = place

        config_dir = os.path.expanduser(r"~/.config/deepin-weather/")
        pickle.dump(weather_condition, open(config_dir + "weather_info_file", "w"))
        return weather_condition
    except Exception, e:
        print e
        return None
