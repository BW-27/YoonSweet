# kivy 2.1.0, python 3.7, pyinstaller 5.6.1
# last_update: 2022-10-30 19:56 UTC+1
#
# in case if you find any problems duuring running this app
# or trying to compile/build with pyinstaller you can contanct me by email: schaehun@student.42.fr
#
# warning: this app is made only for YoonSweet
# do not share this content to any person even for individual purpose
# all (c)copyright to schaehun







# kivymd app
from kivymd.app import MDApp
from kivy.lang import Builder

# kivy window
from kivy.core.window import Window

# start window size
Window.size = (500,800)

# kivy uix
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
# do not call 'from kivymd.uix.list import MDList,OneLineListItem'
# causes error on pyinstaller: "Unable to import package 'kivymd.icon_definitions.md_icons'"
# solved by calling it separately from 'kivymd.uix.list.list'
from kivymd.uix.list.list import MDList
from kivymd.uix.list.list import OneLineListItem

# kivy configuration
from kivy.config import Config

# disable right mouse click button
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# for timestamp of history file
from datetime import datetime

# call exit on critical error
from sys import exit

# logging module for debugging
import logging

# create and configure logger
logging.basicConfig(filename="debug.log",
                    format="%(asctime)s %(message)s",
                    filemode="a")
# creating an object
logger = logging.getLogger()
# setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# get_data.py
# get_song_info(): to get song_info in format: [%s - %s], artist, song_name
# scrape list_file_csv(): requesting google spreadsheet on app launch
try:
    import get_data
except Exception as Arguments:
    logger.critical(Arguments)
    exit(1)

# get_source.py
# type_url(): read data from source/url file - web url to download data file
# type_filepath(): read data from source/filepath file - filepath to access if multiple urls are found
try:
    import get_source
except Exception as Arguments:
    logger.critical(Arguments)
    exit(2)

# global variables
# font style to support ko letters
# by default kivy font is Roboto.ttf
font_open = "[size=14][font=font/NanumGothicBold]"
font_close = "[/font][/size]"
# setting lists: url, filepath
list_url = get_source.type_url()
list_filepath = get_source.type_filepath()

# data read check
if ((not list_url) or (not list_filepath)):
    logger.critical("couldn't get data from source/filepath, source/url")
    exit(3)

# data download
if (not get_data.scrape_list_file_csv(list_url, list_filepath)):
    logger.error("not all required files are loaded")
    pass

# main class 'main.kv'
# Builder.load_file('main.kv')
class Main(BoxLayout):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        # load data list to create MDList items
        self.load_data_kpop()
        self.load_data_pop()
        self.load_data_jpop()

    # add list items to MDList by id: kpop
    def load_data_kpop(self):
        for i in range(1, 512):
            song_info = get_data.get_song_info(i, list_filepath[0])
            if (not song_info):
                break
            item = OneLineListItem(
                text=font_open
                + song_info[0].strip(' ') + " - "
                + song_info[1].strip(' ') + font_close,
                on_release=self.onRelease
            )
            # add item to MDList widget
            self.ids.kpop.add_widget(item)

    # add list items to MDList by id: pop
    def load_data_pop(self):
        for i in range(1, 512):
            song_info = get_data.get_song_info(i, list_filepath[1])
            if (not song_info):
                break
            item = OneLineListItem(
                text=font_open
                + song_info[0].strip(' ') + " - "
                + song_info[1].strip(' ') + font_close,
                on_release=self.onRelease
            )
            # add item to MDList widget
            self.ids._pop.add_widget(item)

    # add list items to MDList by id: jpop
    def load_data_jpop(self):
        for i in range(1, 512):
            song_info = get_data.get_song_info(i, list_filepath[2])
            if (not song_info):
                break
            item = OneLineListItem(
                text=font_open
                + song_info[0].strip(' ') + " - "
                + song_info[1].strip(' ') + font_close,
                on_release=self.onRelease
            )
            # add item to MDList widget
            self.ids.jpop.add_widget(item)

    # on 'click' list item: output result to result.txt
    def onRelease(self, instance):
        # write song_info to result.txt file
        try:
            result_fd = open("result/result.txt", "w", encoding="utf-8")
        except Exception as Arguments:
            logger.error(Arguments)
            return

        # write data format: song_artist - song_name
        result_fd.write(instance.text[len(font_open):len(font_close)*-1])
        result_fd.close()

        # add song_info to history.txt file with timestamp
        try:
            history_fd = open("result/history.txt", "a", encoding="utf-8")
        except Exception as Arguments:
            logger.error(Arguments)
            return

        # write data format: [$(timestamp)] song_artist - song_name
        timestamp = "[{0}] ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))#
        history_fd.write(timestamp + instance.text[len(font_open):len(font_close)*-1] + '\n')
        history_fd.close()

# main class
class MainApp(MDApp):
    def build(self):
        # app title on window bar
        self.title = "YoonSweet"

        # app icon on window bar
        self.icon = "resources/mini_yoon.png"

        # app default theme mode: bg
        self.theme_cls.theme_style = "Light"

        # app default theme primary color: only in navbar
        self.theme_cls.primary_palette = "Blue"

        return Main()

# running app
if (__name__ == "__main__"):
    MainApp().run()