from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import time
import webbrowser

from sharedfile import FileSharer

Builder.load_file('frontend.kv')



class CameraScreen(Screen):
    def start(self):
        """Starts camera and changes Button text"""
        self.ids.camera.opacity = 1
        self.ids.camera.play = True
        self.ids.camera_button.text = "Stop Camera"
        self.ids.camera.texture = self.ids.camera._camera.texture # Set text back to the default values

    def stop(self):
        """Stops camera and changes Button text"""
        self.ids.camera.opacity = 0
        self.ids.camera.play = False
        self.ids.camera_button.text = "Start Camera"
        self.ids.camera.texture = None

    def capture(self):
        """Creates a filename with the current time and captures and saves a photo image under that filename"""
        current_time = time.strftime('%Y%m%d-%H%H%S')
        self.filename = "images/" + current_time + ".png"
        self.ids.camera.export_to_png(self.filename)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = self.filename

class ImageScreen(Screen):
    link_message = "You MUST first generate the link!"
    def create_link(self):
        """Accesses the photo filename, uploads it to the web, and inserts the link in the Label widget"""
        filepath = App.get_running_app().root.ids.camera_screen.filename
        fileshare = FileSharer(filepath= filepath)
        self.url = fileshare.share()
        self.ids.link.text = self.url

    def copy_link(self):
        """Copy link to the clipboard available for pasting"""
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = self.link_message

    def open_link(self):
        """Open link with defauld browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = self.link_message

#Class inherits from ScreenManager
class RootWidget(ScreenManager):
    pass

class MainApp(App):

    def build(self):
      return RootWidget()

MainApp().run()  