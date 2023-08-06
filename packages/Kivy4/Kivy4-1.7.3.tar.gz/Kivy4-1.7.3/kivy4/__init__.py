from kivy import Config
import os, darkdetect

Config.set('graphics', 'resizable', 0)
Config.set('input', 'mouse', 'mouse, multitouch_on_demand')
Config.set('kivy', 'exit_on_escape', 0)
Config.write()

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.settings import ContentPanel
from kivymd.app import MDApp
from screeninfo import get_monitors
from kivy.properties import StringProperty


def getSpec(name: str, filename: str = 'main.py', icon: str = '', path: str = os.getcwd()):

    path = path.replace("\\", r"\\")

    with open(filename.replace('.py', '.spec'), 'w') as f:
        f.write(fr"""
from kivy_deps import sdl2, glew

# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

a = Analysis(['{filename}'],
             pathex=['{path}'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={{}},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='{name}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None, icon='{icon}')

coll = COLLECT(exe, Tree('{path}'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               upx_exclude=[],
               name='{name}')""")


class Kivy4(MDApp):

    dark_mode_icon = StringProperty('')

    def __init__(self, string: str = '', app_name: str = '', dict_of_files: dict = None,
                 screen_size=None, minimum: list = [0.1, 0.1], center: bool = True,
                 sun_icon: str = 'white-balance-sunny', moon_icon: str = 'weather-night',
                 main_color: str = 'Blue', icon: str = '', toolbar = False, app_data: bool = True,
                 custom_classes: bool = True, disable_x: bool = False, **kwargs):

        super().__init__(**kwargs)

        self.app_name = app_name

        if app_data:
            app_data_path = os.getenv('APPDATA') + '/' + app_name
            self.appdata_path = app_data_path
            self.create_files(dict_of_files)

            self.moon_icon = moon_icon
            self.sun_icon = sun_icon
            self.isDarkMode()

        self.theme_cls.primary_palette = main_color
        self.disable_x = disable_x
        self.icon = icon

        screen = get_monitors()[0]
        self.width = screen.width
        self.height = screen.height

        self.screen_positions(screen_size, minimum, center)

        self.builder_string = ''

        if custom_classes:
            self.builder_string += self.custom_classes()

        if toolbar:
            self.builder_string += self.getToolbar(toolbar)
            string = '\n            '.join(string.split('\n'))

        self.builder_string += string

        self.run()

    def build(self):
        self.use_kivy_settings = False
        self.settings_cls = ContentPanel
        self.title = self.app_name

        Window.bind(on_request_close=lambda x: self.on_request_close(self.disable_x))
        Window.bind(on_drop_file=self.on_drop_file)

        self.Build()

        return Builder.load_string(self.builder_string)

    def Build(self):
        pass

    def screen_positions(self, screen_size, minimum, center):

        min_x, min_y = minimum
        if screen_size is None:
            x, y = 0.6, 0.6

        else:
            x, y = screen_size[0], screen_size[1]

        if x <= 1 or y <= 1:
            Window.size = (self.width * x, self.height * y)
            Window.minimum_height = self.height * min_y
            Window.minimum_width = self.width * min_x


        else:
            Window.size = (x, y)
            Window.minimum_height = min_y
            Window.minimum_width = min_x

            if center:
                Window.left = (self.width - x) / 2
                Window.top = (self.height - y) / 2
                return

            else:
                return

        if center:
            Window.left = (self.width - (self.width * x)) / 2
            Window.top = (self.height - (self.height * y)) / 2

    def create_files(self, list_of_files):

        try:
            if not os.path.isdir(self.appdata_path):
                os.mkdir(self.appdata_path)

            if list_of_files:
                for file in list_of_files:
                    self.setFile(file, list_of_files[file], check_if_file_exist=True)

        except Exception as e:
            return e

    def setFile(self, file, value, check_if_file_exist=False, extension='.txt'):

        path_to_create = f'{self.appdata_path}/{file}{extension}'

        try:
            if not check_if_file_exist or not os.path.isfile(path_to_create):
                with open(path_to_create, 'w') as f:
                    f.write(value)

        except Exception as e:
            print(e)
            return e

    def getFile(self, file, default=None, create_file_if_not_exist=False, extension='.txt'):

        path_of_file = f'{self.appdata_path}/{file}.{extension}'

        try:
            with open(path_of_file, 'r') as f:
                return f.read()

        except FileNotFoundError:
            if create_file_if_not_exist:
                with open(path_of_file, 'w') as f:
                    f.write(default)
                    return default

            else:
                return default

        except Exception as e:
            print(e)
            return default

    def isDarkMode(self, filename='dark mode.txt'):
        try:
            with open(self.appdata_path + '/' + filename, 'r') as f:

                current_mode = f.read()
                self.setDarkModeIcon(current_mode)

                return current_mode == 'Dark'

        except FileNotFoundError:
            with open(self.appdata_path + '/' + filename, 'w') as f:
                default = darkdetect.theme()
                f.write(default)

                self.setDarkModeIcon(default)

                return default == 'Dark'

        except AttributeError:
            return False

    def setDarkMode(self, value=None, filename='dark mode'):
        if value is None:
            value = darkdetect.theme()

        self.setFile(filename, value)
        self.setDarkModeIcon(value)

    def reverseDarkMode(self, filename: str = 'dark mode.txt'):
        try:
            with open(self.appdata_path + '/' + filename, 'r') as f:

                current_mode = f.read()

                if current_mode == 'Dark':
                    self.setDarkMode('Light')
                    return 'Light'

                self.setDarkMode('Dark')
                return 'Dark'

        except FileNotFoundError:
            with open(self.appdata_path + '/' + filename, 'w') as f:
                default = darkdetect.theme()
                f.write(default)

                self.setDarkModeIcon(default)

                return default

        except AttributeError:
            return False

    def setDarkModeIcon(self, value):
        if value == 'Dark':
            self.dark_mode_icon = self.moon_icon

        else:
            self.dark_mode_icon = self.sun_icon

        self.theme_cls.theme_style = value

    @staticmethod
    def on_request_close(disable_x: bool = False):
        return disable_x

    def getToolbar(self, properties: list):
        if properties == True:
            right_icons, left_icons, name = '[[app.dark_mode_icon, lambda x: app.reverseDarkMode()]]', '[]', self.app_name

        elif len(properties) == 2:
            left_icons, right_icons, name = properties[0], properties[1], self.app_name
            name = self.app_name

        else:
            left_icons, right_icons, name = properties

        return f'''
Screen:
    MDToolbar:
        id: toolbar
        pos_hint: {{"top": 1}}
        elevation: 10
        title: "{name}"
        right_action_items: {right_icons}
        left_action_items: {left_icons}
    
    MDNavigationLayout:
        x: toolbar.height
        ScreenManager:
            id: screen_manager
'''

    @staticmethod
    def custom_classes():
        return '''
<Text@MDLabel>:
    halign: 'center'

<Input@MDTextField>:
    mode: "rectangle"
    text: ""
    size_hint_x: 0.5

<Check@MDCheckbox>:
    group: 'group'
    size_hint: None, None
    size: dp(48), dp(48)

<Btn@MDFillRoundFlatIconButton>:
    text: ""
    
    
<Img@Image>:    
    allow_stretch: True
'''

    @staticmethod
    def on_drop_file(_, path, x, y):
        print(path, x, y)