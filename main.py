import os
os.environ["KIVY_GL_BACKEND"] = "angle_sdl2"

from kivymd.tools.hotreload.app import MDApp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel

from widgets.background_widget import BackgroundWidget


class ChineseWallApp(MDApp):
    DEBUG = True
    AUTORELOADER_PATHS = [
        (".", {"recursive": False}),
        ("widgets", {"recursive": True}),
    ]
    KV_DIRS = [
        "widgets"
    ]

    def __init__(self, **kwargs):
        super().__init__()
        self.background = None

    def build_app(self, first=False):
        self.background = BackgroundWidget()
        return self.background


if __name__ == "__main__":
    ChineseWallApp().run()
