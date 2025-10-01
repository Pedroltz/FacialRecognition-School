#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk
from src.views.main_window import MainWindow
from src.controllers.room_controller import RoomController

class RoomManagementApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.room.management")
        self.controller = RoomController()

    def do_activate(self):
        window = MainWindow(self, self.controller)
        window.present()

def main():
    app = RoomManagementApp()
    app.run()

if __name__ == "__main__":
    main()
