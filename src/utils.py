import os

import gettext
from gettext import gettext as _
gettext.bindtextdomain("newX", "../locale")
gettext.textdomain("newX")

CONFIG_DIR = os.path.expanduser("~/.config/newX/")

def fade_in(widget, step=0.05, callback=None, *user_data):
    if widget.get_opacity() < 1:
        widget.set_opacity(widget.get_opacity() + step)
    elif callable(callback):
        if(user_data):
            callback(*user_data)
        else:
            callback()
            return False
    else:
        return False
    return True

def fade_out(widget, step=0.05, callback=None, *user_data):
    if widget.get_opacity() > 0:
        widget.set_opacity(widget.get_opacity() - step)
    elif callable(callback):
        if(user_data):
            callback(*user_data)
        else:
            callback()
            return False
    else:
        return False
    return True

def compute_wind(wind_speed, wind_direction):
    level_list = [
        (1, 0),
        (6, 1),
        (12, 2),
        (20, 3),
        (29, 4),
        (39, 5),
        (50, 6),
        (62, 7),
        (75, 8),
        (89, 9),
        (103, 10),
        (117, 11),
        ]
    wind_level = 12
    for x in level_list:
        if float(wind_speed) < x[0]:
            wind_level = x[1]
            break
    
    direction = _("N")
    degrees = [11.25] * 16
    for index, ele in enumerate(degrees):
        degrees[index] += (index * 22.5)
    directions = [
        _("N"), _("NNE"), _("NE"), _("ENE"), _("E"), _("ESE"), _("SE"), _("SSE"),
        _("S"), _("SSW"), _("SW"), _("WSW"), _("W"), _("WNW"), _("NW"), _("NWN"),
        ]
    direction_list = zip(degrees, directions)

    for x in direction_list:
        if float(wind_direction) < x[0]:
            direction = x[1]
            break
    return direction + "  " + str(wind_level) + _("LEVEL")
