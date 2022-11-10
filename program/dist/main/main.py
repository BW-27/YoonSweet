# app version 2.1
#
# kivy 2.1.0, python 3.7, pyinstaller 5.6.1
# last_update: 2022-11-10 7:04 UTC+1
#
# in case if you find any problems duuring running this app
# or trying to compile/build with pyinstaller you can contanct me by email: schaehun@student.42.fr
#
# warning: this app is made only for YoonSweet (https://www.twitch.tv/yoonsweet_)
# do not share this content to any person even for individual purpose
# all (c)copyright to schaehun



# kivymd app
from kivymd.app import MDApp
from kivy.lang import Builder

# kivy window
from kivy.core.window import Window

# start window size
Window.size = (500,800)
# set the minimal window size
Window.minimum_width, Window.minimum_height = (250, 200)

# kivy uix
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen, ScreenManager
# kivymd uix
from kivymd.uix.bottomnavigation.bottomnavigation import MDBottomNavigation

# do not call 'from kivymd.uix.list import MDList,OneLineListItem'
# causes error on pyinstaller: "Unable to import package 'kivymd.icon_definitions.md_icons'"
from kivymd.uix.list.list import MDList
from kivymd.uix.list.list import OneLineListItem

# kivy configuration
from kivy.config import Config

# disable right mouse click button
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# disable exit on 'esc' key
Config.set('kivy', 'exit_on_escape', '0')

# for timestamp of history file
from datetime import datetime
# call exit on critical error
from sys import exit
# regex for string
import re
# difflib for comparing strings
import difflib
# webbrowser
import webbrowser as wb
# logging module for debugging
import logging
# python garbage collector to reduce ram usage
import gc

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

# on search to store previous user_input
old_input = ""

# store items to remove after use
result_list_info = []

# setting lists: url, filepath
list_url = get_source.type_url()
list_filepath = get_source.type_data_list_filepath()
url_list_filepath = get_source.type_url_list_filepath()

# data read check
if ((not list_url) or (not list_filepath)):
    logger.critical("couldn't get data from source/filepath, source/url")
    exit(3)

# data read check
if (not url_list_filepath):
    logger.critical("couldn't get data: url_list_url")
    exit(4)

# data download
if (not get_data.scrape_list_file_csv(list_url, list_filepath)):
    logger.error("not all required files are loaded")

# Builder.load_file('main.kv')

# main screen
class Main(Screen):
    def __init__(self, **kwargs):
        super(Main, self).__init__(**kwargs)
        # create item widgets on MDList and display on screen
        self.load_data_kpop()
        self.load_data_pop()
        self.load_data_jpop()

    # add list items to MDList by id: kpop
    def load_data_kpop(self):
        file_id = 0
        mdlist = MDList()
        for i in range(1, 512):
            song_info = get_data.get_song_info(i, list_filepath[file_id])
            if (not song_info):
                break
            item = self.create_item(song_info, file_id, i)
            # add item to MDList
            mdlist.add_widget(item)
        # add mdlist to ScrollView
        self.ids.kpop.add_widget(mdlist)

    # add list items to MDList by id: _pop
    def load_data_pop(self):
        file_id = 1
        mdlist = MDList()
        for i in range(1, 512):
            song_info = get_data.get_song_info(i, list_filepath[file_id])
            if (not song_info):
                break
            item = self.create_item(song_info, file_id, i)
            # add item to MDList
            mdlist.add_widget(item)
        # add mdlist to ScrollView
        self.ids._pop.add_widget(mdlist)

    # add list items to MDList by id: jpop
    def load_data_jpop(self):
        file_id = 2
        mdlist = MDList()
        for i in range(1, 512):
            song_info = get_data.get_song_info(i, list_filepath[file_id])
            if (not song_info):
                break
            item = self.create_item(song_info, file_id, i)
            # add item to MDList
            mdlist.add_widget(item)
        # add mdlist to ScrollView
        self.ids.jpop.add_widget(mdlist)

    # create item and assign id
    def create_item(self, song_info, file_id, i):
        item = OneLineListItem(
            text=font_open
            + song_info[0].strip(' ') + " - "
            + song_info[1].strip(' ') + font_close,
            on_release = lambda *args: self.onRelease(*args)
        )
        self.ids[str(file_id) + '_label_' + str(i)] = item
        return item

    # on 'click' list item: output result to result.txt
    def onRelease(self, *args):
        instance = args[0]

        # write song_info to result.txt file
        try:
            with open("result/result.txt", "w", encoding="utf-8") as result_fd:
                # write data format: song_artist - song_name
                result_fd.write(instance.text[len(font_open):len(font_close)*-1])
        except Exception as Arguments:
            logger.error(Arguments)
            return

        # add song_info to history.txt file with timestamp
        try:
            with open("result/history.txt", "a", encoding="utf-8") as history_fd:
                # write data format: [$(timestamp)] song_artist - song_name
                timestamp = "[{0}] ".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                history_fd.write(timestamp + instance.text[len(font_open):len(font_close)*-1] + '\n')
        except Exception as Arguments:
            logger.error(Arguments)
            return

        # find index of result_list_info matching with instance
        for line, index in zip(result_list_info, range(0, 512)):
            if (instance.text == line[0].text):
                break

        if instance in self.ids.values():
            file_id = int(list(self.ids.keys())[list(self.ids.values()).index(instance)][0])
        else:
            file_id = int(result_list_info[index][1])
        try:
            with open(url_list_filepath[file_id], "r", encoding="utf-8") as url_list_fd:
                for line in url_list_fd:
                    line = line.split(',')

                    # get text from user selected OneLineListItem
                    song_info = instance.text[len(font_open):len(font_close)*-1].replace(',', '')

                    if (song_info in line):
                        # check if url starts with https://
                        if (line[1][:8] == "https://"):
                            # open url with default webbrowser
                            wb.open_new(line[1].replace('\n', ''))
                        else:
                            logger.error("url must start with https://")
        except Exception as Arguments:
            logger.error(Arguments)
            return

    # call when user types something on text-input:search
    def on_enter(self):
        # global variables
        global old_input
        global result_list_info

        # set user_input
        user_input = re.sub(' +', '', self.ids.search.text).upper()

        # prevent rendering same result multiple times in a row
        if (user_input == old_input):
            return

        # clear widgets before assigning new
        for i in range(0, 512):
            try:
                self.ids.result_list.remove_widget(result_list_info[i][0])
            except:
                self.ids.result_list.clear_widgets()
                result_list_info.clear()
                gc.collect()
                break

        # empty input entered
        if (not user_input):
            old_input = ""
            return

        result = []
        for index in range(0, 3):
            for i in range(1, 512):
                song_info = get_data.get_song_info(i, list_filepath[index])
                if (not song_info):
                    break
                # set current song info
                search_info = ''.join(song_info)
                search_info = re.sub(' +', '', search_info).upper()

                # removing star unicode character
                search_info = re.sub('\u2605', '', search_info)

                # add to result list to render after searching
                if (user_input in search_info):
                    song_info.append(index)
                    result.append(song_info)

        for line, i in zip(result, range(0, len(result) + 1)):
            # create OneLineListItem without assigning id to it
            item = OneLineListItem(
                text=font_open
                + line[0].strip(' ') + " - "
                + line[1].strip(' ') + font_close,
                on_release = lambda *args: self.onRelease(*args)
            )
            # to remove current item widgets when new user input incomes
            # line[-1] for saving file_id to use it on onRelease() function
            info = [item, line[-1]]
            result_list_info.append(info)

            # add item to MDList
            self.ids.result_list.add_widget(item)

        # save old_input for the next input
        old_input = user_input



# edit screen
class Edit(Screen):
    def __init__(self, **kwargs):
        super(Edit, self).__init__(**kwargs)
        self.check_url_list_files()
        self.load_edit_kpop()
        self.load_edit_pop()
        self.load_edit_jpop()

    # check for existance of url_list files
    def check_url_list_files(self):
        for filename in url_list_filepath:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    logger.debug(filename + ": successfully accessed")
            except:
                # create if doesn't exists
                logger.error(filename + ": couldn't open or find file. creating new files")
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        logger.debug(filename + " was created")
                except:
                    logger.error("cannot create file: " + filename)

    # add widgets to gridlayout with id edit_kpop
    def load_edit_kpop(self):
        file_id = 0
        for i in range(1, 512):
            _layout = BoxLayout(orientation="horizontal")
            song_info = get_data.get_song_info(i, list_filepath[file_id])
            if (not song_info):
                break

            # create label and give id
            _label = self.create_label(song_info)
            self.ids[str(file_id) + '_label_' + str(i)] = _label

            # create textinput and give id
            _textinput = self.create_textinput(i, file_id)
            self.ids[str(file_id) + '_textinput_' + str(i)] = _textinput

            # foreground_color: red, if url does not begin with https://
            self.check_input_on_start(self.get_url(i, file_id), str(file_id) + '_textinput_' + str(i))

            # add widgets
            _layout.add_widget(_label)
            _layout.add_widget(_textinput)
            self.ids.edit_kpop.add_widget(_layout)

    # add widgets to gridlayout with id edit_pop
    def load_edit_pop(self):
        file_id = 1
        for i in range(1, 512):
            _layout = BoxLayout(orientation="horizontal")
            song_info = get_data.get_song_info(i, list_filepath[file_id])
            if (not song_info):
                break

            # create label and give id
            _label = self.create_label(song_info)
            self.ids[str(file_id) + '_label_' + str(i)] = _label

            # create textinput and give id
            _textinput = self.create_textinput(i, file_id)
            self.ids[str(file_id) + '_textinput_' + str(i)] = _textinput

            # foreground_color: red, if url does not begin with https://
            self.check_input_on_start(self.get_url(i, file_id), str(file_id) + '_textinput_' + str(i))

            # add widgets
            _layout.add_widget(_label)
            _layout.add_widget(_textinput)
            self.ids.edit_pop.add_widget(_layout)

    # add widgets to gridlayout with id edit_jpop
    def load_edit_jpop(self):
        file_id = 2
        for i in range(1, 512):
            _layout = BoxLayout(orientation="horizontal")
            song_info = get_data.get_song_info(i, list_filepath[file_id])
            if (not song_info):
                break

            # create label and give id
            _label = self.create_label(song_info)
            self.ids[str(file_id) + '_label_' + str(i)] = _label

            # create textinput and give id
            _textinput = self.create_textinput(i, file_id)
            self.ids[str(file_id) + '_textinput_' + str(i)] = _textinput

            # foreground_color: red, if url does not begin with https://
            self.check_input_on_start(self.get_url(i, file_id), str(file_id) + '_textinput_' + str(i))

            # add widgets
            _layout.add_widget(_label)
            _layout.add_widget(_textinput)
            self.ids.edit_jpop.add_widget(_layout)

    # create edit_list label
    def create_label(self, song_info):
        _label = Label(
            color = (0, 0, 0, 1),
            size_hint = (1, 1),
            text = (song_info[0] + ' - ' + song_info[1]),
            text_size = (200, self.size[1]),
            font_name = 'font/NanumGothicBold.ttf',
            halign = 'left',
            valign = 'middle',
            shorten = True,
            shorten_from = 'right',
            padding_x = 0
        )
        return _label
    
    # create edit_list textinput
    def create_textinput(self, index, file_id):
        _textinput = TextInput(
            font_name = 'font/NanumGothicBold.ttf',
            text = self.get_url(index, file_id),
            hint_text = "URL:",
            foreground_color = (0, 0, 0, 1),
            focus = False,
            multiline = False,
            write_tab = False,
            cursor_blink = True,
            allow_copy = True,
            cursor_color = (0, 0, 0, 1),
            background_active = '',
            on_text_validate = lambda *args: self.on_edit_enter(file_id, *args)
        )
        return _textinput

    # get existing url from url_list file, if not return empty string
    def get_url(self, index, file_id):
        try:
            with open(url_list_filepath[file_id], 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.split(',')
                    line[1] = line[1].replace('\n', '')
                    # if edit_list label contained in url_list return that urL_list line
                    if (line[0] in self.ids[str(file_id) + '_label_' + str(index)].text.replace(',', '')):
                        if (not line[1]):
                            return ""
                        return (line[1])
        except Exception as Arguments:
            logger.error(Arguments)
        return ""

    # when user press enter on textinput in edit screen
    def on_edit_enter(self, file_id, *args):
        instance = args[0]
        # find self_id by instance
        if instance in self.ids.values():
            self_id = list(self.ids.keys())[list(self.ids.values()).index(instance)]

        if (not instance.text.strip(' ').replace(',', '')):
            song_url = ""
        else:
            song_url = instance.text
            song_url = song_url.strip(' ').replace(',', '')

        # get song info from edit_list:label by id
        song_info = self.ids[str(file_id) + '_label_' + self_id.split('_')[-1]].text
        song_info = song_info.replace(',', '')

        # read all the data from url_list
        try:
            with open(url_list_filepath[file_id], "r", encoding="utf-8") as url_list_fd:
                url_list = url_list_fd.read().splitlines()
        except Exception as Arguments:
            logger.error(Arguments)
            return

        # check for duplicated cases
        for line in url_list:
            line = line.split(',')
            if (line[0] == song_info):
                if (song_url == line[1]):
                    return

        # open url_list file to append results
        try:
            url_list_fd = open(url_list_filepath[file_id], "a", encoding="utf-8")
        except Exception as Arguments:
            logger.error(Arguments)
            return

        # at very beginning if url_list file is empty
        if (not url_list):
            url_list_fd.write(song_info + ',' + song_url + '\n')
            self.is_valid_input(song_url, self_id)
            return

        # if url has changed find that line and replace that url
        for line in url_list:
            line = line.split(',')
            if (song_info == line[0]):
                if (line[1] != song_url):
                    with open(url_list_filepath[file_id], 'r', encoding='utf-8') as f:
                        data = f.read()
                        data = data.replace(','.join(line), line[0] + ',' + song_url.replace('\n', ''))
                    with open(url_list_filepath[file_id], 'w', encoding='utf-8') as f:
                        f.write(data)
                        self.is_valid_input(song_url, self_id)
                    return

        # if url_list do not contain current song add at the end
        url_list_fd.write(song_info + ',' + song_url + '\n')
        self.is_valid_input(song_url, self_id)
        url_list_fd.close()

    # if url does not begin with https:// change foreground_color to red else to green
    def is_valid_input(self, song_url, self_id):
        if (not song_url):
            self.ids[self_id].foreground_color = (0, 0, 0, 1)
            return
        if (song_url[:8] == "https://"):
            self.ids[self_id].foreground_color = (0, 153/255, 0, 1)
        else:
            self.ids[self_id].foreground_color = (153/255, 0, 0, 1)

    # when user launches app check urls
    def check_input_on_start(self, song_url, self_id):
        if (not song_url):
            self.ids[self_id].foreground_color = (0, 0, 0, 1)
            return
        if (song_url[:8] == "https://"):
            self.ids[self_id].foreground_color = (0, 0, 0, 1)
        else:
            self.ids[self_id].foreground_color = (153/255, 0, 0, 1)

    # when user exits from edit mode check urls and turn green to default but remain red
    def on_confirm(self):
        for i in range(0, 3):
            for index in range(1, 512):
                try:
                    if (not self.ids[str(i) + '_textinput_' + str(index)].text):
                        self.ids[str(i) + '_textinput_' + str(index)].foreground_color = (0, 0, 0, 1)
                        continue
                    if (self.ids[str(i) + '_textinput_' + str(index)].text[:8] == "https://"):
                        self.ids[str(i) + '_textinput_' + str(index)].foreground_color = (0, 0, 0, 1)
                    else:
                        self.ids[str(i) + '_textinput_' + str(index)].foreground_color = (153/255, 0, 0, 1)
                except:
                    break



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
        self.theme_cls.primary_palette = "LightBlue"

        # define screen manager and assign screens into it
        sm = ScreenManager()
        sm.add_widget(Main(name='main'))
        sm.add_widget(Edit(name='edit'))

        # set default screen to main
        sm.current = 'main'

        return sm



# running app
if (__name__ == "__main__"):
    MainApp().run()
