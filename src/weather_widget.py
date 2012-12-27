import time
import gtk
import cairo
import pango
import pangocairo
import gobject

import yahoo_service

class WeatherPad(gtk.Window):
    '''
    class docs
    '''
	
    def __init__(self, weather_information):
        '''
        init docs
        '''
        gtk.Window.__init__(self)
        
#        self.old_weather_information = weather_information        
#        self.new_weather_information = None
        self.weather_information = weather_information
        self.pad = gtk.DrawingArea()
        self.pad.add_events(gtk.gdk.ALL_EVENTS_MASK)

        self.set_decorated(False) 
        self.set_size_request(300, 300)
        self.set_app_paintable(False)
        self.set_colormap(gtk.gdk.Screen().get_rgba_colormap())
        self.set_resizable(False)
        self.set_keep_below(True)
        self.move(1000, 100)
        self.stick()
        # self.set_skip_taskbar_hint(True)

        #To customizse location, but it will not be used recently
        #self.pad.connect("button_press_event", 
        #                 (lambda widget, event, window: 
        #                  window.begin_move_drag(
        #            event.button,
        #            int(event.x_root),
        #            int(event.y_root),
        #            event.time
        #            )), self )
        
        self.pad.connect("button_press_event", self.button_press_callback)
        self.pad_expose_connect_id = self.pad.connect("expose-event", self.pad_expose)

        self.add(self.pad)
        self.connect("destroy", gtk.main_quit)
        self.show_all()

    def button_press_callback(self, widget, event):
        '''
        docs
        '''
        coord_x = event.x
        coord_y = event.y
        if 210 <= coord_x <= 270 and 117 <= coord_y <= 134:
            self.open_preference()
        if 270 <= coord_x <= 300 and 110 <= coord_y <= 140:
            self.update_weather_information()
    

    def get_date_time_weekday(self):
        '''
        docs
        '''
        str_date_time_weekday = time.strftime("%H:%M %x %A")
        [str_time, str_date, str_weekday] = str_date_time_weekday.split(' ')
        
        return str_time, str_date, str_weekday
    
    def open_preference(self, places_dict=None):
        self.remove(self.pad)
        # self.set_border_width(5)
        main_box = gtk.VBox(False, 2)
        hbox = gtk.HBox(False, 3)
        text_entry = gtk.Entry()
        find_button = gtk.Button("Enter")
        cancel_button = gtk.Button("Cancel")
        hbox.pack_start(text_entry, True, True, 0)
        hbox.pack_start(find_button, False, False, 0)
        hbox.pack_start(cancel_button, False, False, 0)
        
        result_window = gtk.ScrolledWindow()
        result_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_NEVER)
        vbox = gtk.VBox()
        result_window.add_with_viewport(vbox)
        
        main_box.pack_start(hbox, False, False, 0)
        main_box.pack_start(result_window, True, True, 0)
        find_button.connect("clicked", self.find_button_clicked, text_entry, vbox)
        cancel_button.connect("clicked", self.cancel_button_clicked)
        self.add(main_box)
        self.show_all()
        
    def cancel_button_clicked(self):
        '''
        docs
        '''
        self.remove(self.get_children()[0])
        self.add(self.pad)
        self.show_all()
    
        
    # to provide a better UE, then the button would not something like dead :-)
    def find_button_clicked(self, widget, text_entry, vbox):
        if(text_entry.get_text()):
            gobject.timeout_add(1, self.preference_find_place, widget, text_entry, vbox)
    def preference_find_place(self, widget, text_entry, vbox):
        print "preference_find_place"
        woeid_list = yahoo_service.get_woeid_by_place(text_entry.get_text())
        for woeid in woeid_list:
            place_dict = yahoo_service.get_place_by_woeid(woeid)
            button = gtk.Button(place_dict["all"])
            button.connect("clicked", self.place_button_clicked, woeid, text_entry.get_text())
            vbox.pack_start(button, False, False, 0)
        self.show_all()
            
    def place_button_clicked(self, widget, woeid, place):
        '''
        docs
        '''
        self.woeid = woeid
        self.location = place
        # the same trick here :-)
        gobject.timeout_add(1, self.update_weather_information)
        self.remove(self.get_children()[0])
        self.add(self.pad)
        self.show_all()
    
        
    def update_weather_information(self):
        if(self.woeid):
            self.weather_information = yahoo_service.get_weather_information_by_woeid(self.woeid, self.location)
    
    def draw_weather_information(self, weather_information):
        '''
        docs
        '''
        weather_icon_path = "../data/images/icons/" + weather_information["pic"] + ".png"
        weather_icon_pixbuf = gtk.gdk.pixbuf_new_from_file(weather_icon_path)
        
        cr = self.pad.window.cairo_create()
        cr.set_source_pixbuf(weather_icon_pixbuf, 190, 0)
        cr.paint()
        
        context = pangocairo.CairoContext(cr)
        cr.set_source_rgb(1, 1, 1)
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("Monaco 8"))
        layout.set_text(weather_information["text"])
        
        cr.move_to(210, 85)
        context.update_layout(layout)
        context.show_layout(layout)
        cr.move_to(210, 100)
        layout.set_text(weather_information["temp"])
        context.update_layout(layout)
        context.show_layout(layout)
        
        cr.set_source_rgba(0, 0, 0, 0.3)
        cr.rectangle(210, 117, 60, 17)
        cr.fill()
        
        cr.set_source_rgb(1, 1, 1)
        layout.set_text(weather_information["location"])
        cr.move_to(212, 119)
        context.update_layout(layout)
        context.show_layout(layout)
        
        refresh_icon_pixbuf = gtk.gdk.pixbuf_new_from_file("../data/images/refresh.png")
        refresh_icon_pixbuf = refresh_icon_pixbuf.scale_simple(30, 30, gtk.gdk.INTERP_HYPER)
        cr.set_source_pixbuf(refresh_icon_pixbuf, 270, 110)
        cr.paint()

       # self.old_weather_information = weather_information
       # self.new_weather_information = None
        
    def pad_expose(self, widget, event):
        big_pad_pixbuf = gtk.gdk.pixbuf_new_from_file("../data/images/big_pad.png")
        rect = widget.allocation
        cr = widget.window.cairo_create()
        cr.set_operator(cairo.OPERATOR_CLEAR)
        cr.set_source_rgb(0, 0, 0)
        cr.rectangle(0, 0, rect.width, rect.height)
        cr.fill()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_pixbuf(big_pad_pixbuf, 0, 15)
        cr.paint()

        time_pad_pixbuf = gtk.gdk.pixbuf_new_from_file("../data/images/time_pad.png")
        cr.set_source_pixbuf(time_pad_pixbuf, 18, 0)
        cr.paint()

        # Create pangocairo context.
        context = pangocairo.CairoContext(cr)
        cr.set_source_rgb(0.3, 0.3, 0.3)
        
        (str_time, str_date, str_weekday) = self.get_date_time_weekday()
        # Set layout.
        layout = context.create_layout()
        layout.set_font_description(pango.FontDescription("Monaco 35"))
        layout.set_text(str_time)
            
        # Draw text.
        cr.move_to(35, 20)
        context.update_layout(layout)
        context.show_layout(layout)
        
        cr.set_source_rgb(1, 1, 1)
        layout.set_font_description(pango.FontDescription("Monaco 10"))
        layout.set_text(str_date + "  " + str_weekday)
        
        cr.move_to(30, 115)
        context.update_layout(layout)
        context.show_layout(layout)
        
#        if self.old_weather_information["from"] == "from_file":
#            self.draw_weather_information(self.old_weather_information)
#        if self.new_weather_information != None:
#            self.draw_weather_information(self.new_weather_information)
        self.draw_weather_information(self.weather_information)

        self.queue_draw()
