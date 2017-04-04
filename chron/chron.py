from os import linesep
from datetime import datetime

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '3.0')
from gi.repository import GObject, Gio, Gtk, GtkSource, Gedit, PeasGtk


plugin_namespace = 'chron'
ns = lambda s : plugin_namespace + '.' + s


class ChronAppActivatable(GObject.Object, Gedit.AppActivatable, PeasGtk.Configurable):

    app = GObject.Property(type=Gedit.App)

    def __init__(self):
        GObject.Object.__init__(self)
        self._accls = []


    def _add_accl(self, accl, action):
        self.app.add_accelerator(accl, action, None)
        self._accls.append(action)


    def do_activate(self):
        self._add_accl("F2", "win." + ns("date"))
        self._add_accl("F3", "win." + ns("time"))
        self._add_accl("F4", "win." + ns("datetime"))


    def do_create_configure_widget(self):
        settings = Gio.Settings.new("org.gnome.gedit.plugins.chron")

        box = Gtk.Box(spacing=4, orientation=Gtk.Orientation.VERTICAL)

        chkNewline = Gtk.CheckButton("insert newline after date/time")
        chkNewline.set_border_width(6)
        box.pack_start(chkNewline, True, True, 0)
        settings.bind("newline-after", chkNewline, "active", Gio.SettingsBindFlags.DEFAULT)

        chkLowercase = Gtk.CheckButton("make all letters lower case")
        chkLowercase.set_border_width(6)
        box.pack_start(chkLowercase, True, True, 0)
        settings.bind("lower-case", chkLowercase, "active", Gio.SettingsBindFlags.DEFAULT)

        date_hbox = self._create_labeled_entry_hbox('Date format', 'date-format', settings)
        box.pack_start(date_hbox, True, True, 0)
        time_hbox = self._create_labeled_entry_hbox('Time format', 'time-format', settings)
        box.pack_start(time_hbox, True, True, 0)

        return box


    def _create_labeled_entry_hbox(self, label, setting_key, settings):
        hbox = Gtk.Box(spacing=6, orientation=Gtk.Orientation.HORIZONTAL)
        hbox.set_border_width(6)

        label = Gtk.Label(label + ':')
        entry = Gtk.Entry()

        settings.bind(setting_key, entry, "text", Gio.SettingsBindFlags.DEFAULT)

        hbox.pack_start(label, True, True, 0)
        hbox.pack_start(entry, True, True, 0)

        return hbox


    def do_deactivate(self):
        for a in self._accls:
            self.app.remove_accelerator(a, None)


class ChronWindowActivatable(GObject.Object, Gedit.WindowActivatable):

    window = GObject.Property(type=Gedit.Window)
    settings = Gio.Settings.new("org.gnome.gedit.plugins.chron")

    def __init__(self):
        GObject.Object.__init__(self)
        self._actions = []


    def do_activate(self):
        self._add_action('date', self.do_insert_date)
        self._add_action('time', self.do_insert_time)
        self._add_action('datetime', self.do_insert_datetime)


    def _add_action(self, name, method):
        action = Gio.SimpleAction(name=ns(name))
        action.connect('activate', lambda a, p: method())
        self.window.add_action(action)

        self._actions.append(name)


    def do_deactivate(self):
        for a in self._actions:
            self.window.remove_action(a)


    def do_insert_date(self):
        fmt = self.settings.get_string('date-format')
        date = datetime.now().strftime(fmt)
        self._insert_at_cursor(date)


    def do_insert_time(self):
        fmt = self.settings.get_string('time-format')
        time = datetime.now().strftime(fmt)
        self._insert_at_cursor(time)


    def do_insert_datetime(self):
        fmt = self.settings.get_string('date-format') + ', ' + self.settings.get_string('time-format')
        date_t = datetime.now().strftime(fmt)
        self._insert_at_cursor(date_t)


    def _insert_at_cursor(self, text):
        if self.settings.get_value('lower-case'):
            text = text.lower()

        if self.settings.get_value('newline-after'):
            text += linesep

        view = self.window.get_active_view()
        buf = view.get_buffer()
        buf.insert_at_cursor(text)
        view.scroll_to_cursor()

