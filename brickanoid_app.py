import kivy
from kivy.config import Config 

Config.set('graphics', 'resizable', '0') 
Config.set('graphics', 'width', '360') 
Config.set('graphics', 'height', '640') 

from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition
from kivy.clock import Clock
from kivy.app import App

import brickanoid_logic 
from brickanoid_gfx import BrickanoidGameScreen, ScoreCanvas


class GameScreen(Screen):
    pass

class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class BrickanoidApp(App):

    game = None

    def on_start(self):
        pass

    def on_pause(self):
        if self.game:
            self.game.brickanoid_logic.pause()
            self.game.to_menu()
        return True

    def on_resume(self):
        # Here you can check if any data needs replacing (usually nothing)
        pass

    def build(self):
        sm = ScreenManager()
        sm.transition = NoTransition()
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.current = 'game'
        self.game = sm.current_screen.ids['brickanoid_game']
        self.game.menu_screen = sm.get_screen('menu')
        self.game.screen_manager = sm
        self.game.start()
        # sm.current = 'menu'
        Clock.schedule_interval(self.game.update, 1.0/60.0)

        return sm