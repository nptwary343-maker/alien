import threading
import time
import os
import sys
from flask import Flask
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.uix.label import Label

# Import the server app
from server import app as flask_app

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = app

    def run(self):
        # Disable the reloader so we don't spawn a new thread
        self.server.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

class CyberGuardianApp(App):
    def build(self):
        # Start Flask in a separate thread
        self.server_thread = ServerThread(flask_app)
        self.server_thread.daemon = True
        self.server_thread.start()

        # UI: Simple label telling user to open browser
        # In a real Kivy app, we might use a WebView, but for simplicity/compatibility:
        label = Label(text="CyberGuardian Server Running...\n\nOpen Chrome and go to:\nhttp://localhost:5000",
                      halign='center', valign='middle')
        
        # Try to open browser automatically
        Clock.schedule_once(self.open_browser, 2)
        return label

    def open_browser(self, *args):
        import webbrowser
        webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    CyberGuardianApp().run()
