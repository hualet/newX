import gtk
import cairo
import pango
import pangocairo

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
        
        self.area = gtk.DrawingArea()
        self.area.add_events(gtk.gdk.ALL_EVENTS_MASK)
        self.area.connect("expose-event", self.area_expose, weather_info)
        
        self.add(self.area)
        self.show_all()

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
        layout.set_text("Visibility: " + weather_info["visibility"])
        cr.move_to(10, 130)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_text("Humidity: " + weather_info["humidity"])
        cr.move_to(10, 113)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_text("Wind: " + weather_info["wind"])
        cr.move_to(10, 96)
        context.update_layout(layout)
        context.show_layout(layout)

        cr.set_source_rgb(0, 0, 0)
        layout.set_text(weather_info["forecast1"]["text"])
        cr.move_to(30, 263)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_text(weather_info["forecast1"]["low"] + "~" + weather_info["forecast1"]["high"])
        cr.move_to(30, 280)
        context.update_layout(layout)
        context.show_layout(layout)

        layout.set_text(weather_info["forecast2"]["text"])
        cr.move_to(185, 263)
        context.update_layout(layout)
        context.show_layout(layout)
        
        layout.set_text(weather_info["forecast2"]["low"] + "~" + weather_info["forecast2"]["high"])
        cr.move_to(185, 280)
        context.update_layout(layout)
        context.show_layout(layout)

        pixbuf1 = gtk.gdk.pixbuf_new_from_file("../data/images/icons/" + weather_info["forecast1"]["pic"] + ".png")
        cr.set_source_pixbuf(pixbuf1, 10, 160)
        cr.paint()
        
        pixbuf2 = gtk.gdk.pixbuf_new_from_file("../data/images/icons/" + weather_info["forecast2"]["pic"] + ".png")
        cr.set_source_pixbuf(pixbuf2, 160, 160)
        cr.paint()