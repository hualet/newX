import gtk
import cairo
import pango
import pangocairo
import gobject

import gettext
from gettext import gettext as _
gettext.bindtextdomain("newX", "../locale")
gettext.textdomain("newX")

from utils import (fade_in, fade_out, fancy_move_x)

class WeatherForecastWindow(gtk.Window):
    '''
    class docs
    '''
	
    def __init__(self, weather_info, x, y):
        '''
        init docs
        '''
        gtk.Window.__init__(self)
        self.set_size_request(300, 300)
        self.move(x, y)
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_colormap(gtk.gdk.Screen().get_rgba_colormap())        
        
        self.DRAG_POS_X = 0
        
        self.area = gtk.DrawingArea()
        self.area.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.area.connect("expose-event", self.area_expose, weather_info)
        self.area.connect("enter-notify-event", self.enter_notify_callback)
        self.area.connect("leave-notify-event", lambda w, e : self.self_fade_out_destroy(self.master_win))
        self.area.connect("button-press-event", self.button_press_callback)
        self.area.connect("button-release-event", self.button_release_callback)
        
        self.add(self.area)
        self.show_all()
        
    def enter_notify_callback(self, widget, event):
        if hasattr(self, "fade_out_id"):
            gobject.source_remove(self.fade_out_id)
        if hasattr(self, "destroy_id"):
            gobject.source_remove(self.destroy_id)
        self.set_opacity(1)
        
    def button_press_callback(self, widget, event):
        coord_x = event.x
        coord_y = event.y

        if 0 <= coord_x <= 300 and 150 <= coord_y <= 300:
            self.drag_begin_pos = coord_x
            self.drag_begin_time = event.time
        
    def button_release_callback(self, widget, event):
        v = (event.x - self.drag_begin_pos) / (event.time - self.drag_begin_time)
        gobject.timeout_add(10, fancy_move_x, 10, v, self, -450, 0)

    def area_expose(self, widget, event, weather_info):
        cr = widget.window.cairo_create()
        cr.rectangle(0, 0, 300, 300)
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.set_source_rgb(0, 0, 0)
        cr.fill()
        
        cr.set_operator(cairo.OPERATOR_OVER)
        bg_pixbuf = gtk.gdk.pixbuf_new_from_file("../data/images/detail.png")
        cr.set_source_pixbuf(bg_pixbuf, 0, 0)
        cr.paint()
        
        context = pangocairo.CairoContext(cr)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("Monaco 45"))
        layout.set_text(weather_info["temp"])
        cr.set_source_rgb(1, 1, 1)
        cr.move_to(10, 10)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_font_description(pango.FontDescription("Monaco 9"))
        layout.set_text(_("Visibility") + ": " + weather_info["visibility"])
        cr.move_to(10, 130)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_text(_("Humidity") + ": " + weather_info["humidity"])
        cr.move_to(10, 113)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_text(_("Wind") + ": " + weather_info["wind"])
        cr.move_to(10, 96)
        context.update_layout(layout)
        context.show_layout(layout)
        
        pixbuf_sep = gtk.gdk.pixbuf_new_from_file("../data/images/seperator.png")
        
        for i in 1, 2, 3, 4, 5:
            cr.set_source_rgb(0, 0, 0)
            layout.set_text(weather_info["forecast" + str(i)]["text"])
            cr.move_to(self.DRAG_POS_X + 10 + 150 * (i - 1), 263)
            context.update_layout(layout)
            context.show_layout(layout)
        
            layout.set_text(weather_info["forecast" + str(i)]["low"] + weather_info["forecast" + str(i)]["high"])
            cr.move_to(self.DRAG_POS_X + 10 + 150 * (i - 1), 280)
            context.update_layout(layout)
            context.show_layout(layout)
        
            layout.set_text(weather_info["forecast" + str(i)]["day"])
            cr.move_to(self.DRAG_POS_X + 105 + 150 * (i - 1), 280)
            context.update_layout(layout)
            context.show_layout(layout)

            cr.set_source_pixbuf(pixbuf_sep, self.DRAG_POS_X + 149 * i, 175)
            cr.paint()


            pixbuf_forecast = gtk.gdk.pixbuf_new_from_file("../data/images/icons/" + 
                                                           weather_info["forecast" + str(i)]["pic"] + ".png")
            cr.set_source_pixbuf(pixbuf_forecast, self.DRAG_POS_X + 10 + 150 * (i - 1), 165)
            cr.paint()
        
        
    def self_fade_out_destroy(self, master_win):
        self.set_opacity(1)
        self.master_win = master_win
        self.fade_out_id = gobject.timeout_add(30, fade_out, self)
        self.destroy_id = gobject.timeout_add(700, self.destroy)
        if hasattr(master_win, "forecast_window"):
            del master_win.forecast_window
