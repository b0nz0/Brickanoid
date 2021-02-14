from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.image import ImageLoader, Texture
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Canvas
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang.builder import Builder
from kivy.utils import platform
from time import perf_counter

import brickanoid_logic 

images_textures = dict()
main_game_screen = None

def load_resources():
    global images_textures
    images_textures['img_brick_red_1_0'] = ImageLoader.load('res/brick_red_1.png').texture
    images_textures['img_brick_red_2_0'] = ImageLoader.load('res/brick_red_2.png').texture
    images_textures['img_brick_red_3_0'] = ImageLoader.load('res/brick_red_3.png').texture
    images_textures['img_brick_red_4_0'] = ImageLoader.load('res/brick_red_4.png').texture
    images_textures['img_brick_blu_1_0'] = ImageLoader.load('res/brick_blu_1.png').texture
    images_textures['img_brick_blu_2_0'] = ImageLoader.load('res/brick_blu_2.png').texture
    images_textures['img_brick_blu_3_0'] = ImageLoader.load('res/brick_blu_3.png').texture
    images_textures['img_brick_blu_4_0'] = ImageLoader.load('res/brick_blu_4.png').texture
    images_textures['img_brick_green_1_0'] = ImageLoader.load('res/brick_green_1.png').texture
    images_textures['img_brick_green_2_0'] = ImageLoader.load('res/brick_green_2.png').texture
    images_textures['img_brick_green_3_0'] = ImageLoader.load('res/brick_green_3.png').texture
    images_textures['img_brick_green_4_0'] = ImageLoader.load('res/brick_green_4.png').texture
    images_textures['img_brick_pink_1_0'] = ImageLoader.load('res/brick_pink_1.png').texture
    images_textures['img_brick_pink_2_0'] = ImageLoader.load('res/brick_pink_2.png').texture
    images_textures['img_brick_pink_3_0'] = ImageLoader.load('res/brick_pink_3.png').texture
    images_textures['img_brick_pink_4_0'] = ImageLoader.load('res/brick_pink_4.png').texture
    images_textures['img_brick_silv_1_0'] = ImageLoader.load('res/brick_silv_1.png').texture
    images_textures['img_brick_silv_2_0'] = ImageLoader.load('res/brick_silv_2.png').texture
    images_textures['img_brick_silv_3_0'] = ImageLoader.load('res/brick_silv_3.png').texture
    images_textures['img_brick_silv_4_0'] = ImageLoader.load('res/brick_silv_4.png').texture
    images_textures['img_brick_gold_1_0'] = ImageLoader.load('res/brick_gold_1.png').texture
    images_textures['img_brick_gold_2_0'] = ImageLoader.load('res/brick_gold_2.png').texture
    images_textures['img_brick_gold_3_0'] = ImageLoader.load('res/brick_gold_3.png').texture
    images_textures['img_brick_gold_4_0'] = ImageLoader.load('res/brick_gold_4.png').texture
    images_textures['img_brick_concrete_1_0'] = ImageLoader.load('res/brick_concrete_1.png').texture
    images_textures['pad_plain'] = ImageLoader.load('res/pad_plain.png').texture
    images_textures['line_blu'] = ImageLoader.load('res/line_blu.png').texture
    images_textures['touch_area'] = ImageLoader.load('res/bkg_touch.png').texture
    images_textures['ball_plain'] = ImageLoader.load('res/ball_200x200.png').texture
    images_textures['pad_yellow_2_0'] = ImageLoader.load('res/pad_yel_2_0.png').texture
    images_textures['pad_yellow_2_1'] = ImageLoader.load('res/pad_yel_2_1.png').texture
    

def get_texture(texture_name):
    global images_textures
    if texture_name not in images_textures:
        load_resources()
    return images_textures[texture_name]
    
class GfxElement(Widget):
    texture_obj = ObjectProperty(None)
    unitary_height = NumericProperty(0)
    unitary_width = NumericProperty(0)
    anim_interval = 0.
    anim_loop = True
    anim_textures = []
    anim_frame = 0
    anim_time = 0.
    obj_to_animate = ObjectProperty(None)

    def __init__(self, **kwargs):
        global main_game_screen
        super(GfxElement, self).__init__(**kwargs)
        self.unitary_width = main_game_screen.gfx_properties['unitary_width']
        self.unitary_height = main_game_screen.gfx_properties['unitary_height']
        if self.anim_interval > 0.:
            self.texture_obj = self.anim_textures[0]
            self.anim_time = 0
    
    def animate(self, dt):
        if self.anim_interval == 0.:
            return
        self.anim_time += dt
        if (self.anim_time > self.anim_interval):
            self.anim_time = 0.
            self.anim_frame += 1
            if self.anim_frame == len(self.anim_textures):
                if not self.anim_loop:
                    self.anim_interval = 0.
                    self.anim_frame -= 1
                else:
                    self.anim_frame = 0
            self.texture_obj = self.anim_textures[self.anim_frame]
            self.obj_to_animate.texture = self.texture_obj

class TouchArea(Widget):
    texture_obj = get_texture('touch_area')
    def on_touch_move(self, touch):
        if self.collide_point(touch.x, touch.y):
            main_game_screen.brickanoid_logic.touch_move(touch.x, touch.y)
    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            main_game_screen.brickanoid_logic.touch_down(touch.x, touch.y)
        else:
            main_game_screen.brickanoid_logic.pause()
            main_game_screen.to_menu()
    def on_touch_up(self, touch):
        if self.collide_point(touch.x, touch.y):
            main_game_screen.brickanoid_logic.touch_up(touch.x, touch.y)

class ScoreCanvas(Widget):
    pass

class GameArea(FloatLayout):
    pass

class BoundariesLine(Widget):
    texture_obj = ObjectProperty(get_texture('line_blu'))

class BallAnoid(GfxElement):
    texture_obj = get_texture('ball_plain')

class PadYellow_2(GfxElement):

    def __init__(self, **kwargs):
        super(PadYellow_2, self).__init__(**kwargs)
        self.texture_obj = get_texture('pad_yellow_2_0')
        self.anim_interval = 0.2
        self.anim_textures = [get_texture('pad_yellow_2_0'), get_texture('pad_yellow_2_1')]
        self.obj_to_animate = self.canvas.children[-1]

class ImgBrick_1_0(GfxElement):
    pass

class ImgBrick_2_0(GfxElement):
    pass

class ImgBrick_3_0(GfxElement):
    pass

class ImgBrick_4_0(GfxElement):
    pass

class ImgBrickRed_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_red_1_0')

class ImgBrickRed_2_0(ImgBrick_2_0):
    texture_obj = get_texture('img_brick_red_2_0')

class ImgBrickRed_3_0(ImgBrick_3_0):
    texture_obj = get_texture('img_brick_red_3_0')

class ImgBrickRed_4_0(ImgBrick_4_0):
    texture_obj = get_texture('img_brick_red_4_0')

class ImgBrickBlu_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_blu_1_0')

class ImgBrickBlu_2_0(ImgBrick_2_0):
    texture_obj = get_texture('img_brick_blu_2_0')

class ImgBrickBlu_3_0(ImgBrick_3_0):
    texture_obj = get_texture('img_brick_blu_3_0')

class ImgBrickBlu_4_0(ImgBrick_4_0):
    texture_obj = get_texture('img_brick_blu_4_0')

class ImgBrickGreen_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_green_1_0')

class ImgBrickGreen_2_0(ImgBrick_2_0):
    texture_obj = get_texture('img_brick_green_2_0')

class ImgBrickGreen_3_0(ImgBrick_3_0):
    texture_obj = get_texture('img_brick_green_3_0')

class ImgBrickGreen_4_0(ImgBrick_4_0):
    texture_obj = get_texture('img_brick_green_4_0')

class ImgBrickPink_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_pink_1_0')

class ImgBrickPink_2_0(ImgBrick_2_0):
    texture_obj = get_texture('img_brick_pink_2_0')

class ImgBrickPink_3_0(ImgBrick_3_0):
    texture_obj = get_texture('img_brick_pink_3_0')

class ImgBrickPink_4_0(ImgBrick_4_0):
    texture_obj = get_texture('img_brick_pink_4_0')

class ImgBrickSilv_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_silv_1_0')

class ImgBrickSilv_2_0(ImgBrick_2_0):
    texture_obj = get_texture('img_brick_silv_2_0')

class ImgBrickSilv_3_0(ImgBrick_3_0):
    texture_obj = get_texture('img_brick_silv_3_0')

class ImgBrickSilv_4_0(ImgBrick_4_0):
    texture_obj = get_texture('img_brick_silv_4_0')

class ImgBrickGold_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_gold_1_0')

class ImgBrickGold_2_0(ImgBrick_2_0):
    texture_obj = get_texture('img_brick_gold_2_0')

class ImgBrickGold_3_0(ImgBrick_3_0):
    texture_obj = get_texture('img_brick_gold_3_0')

class ImgBrickGold_4_0(ImgBrick_4_0):
    texture_obj = get_texture('img_brick_gold_4_0')

class ImgBrickConcrete_1_0(ImgBrick_1_0):
    texture_obj = get_texture('img_brick_concrete_1_0')


class NotifyBanner(Label):
    pass

class BrickanoidGameScreen(Widget):
#    count_lbl = ObjectProperty(None)
    score_lbl = ObjectProperty(None)
    lives_lbl = ObjectProperty(None)    
    level_lbl = ObjectProperty(None)    
    score_lbl_menu = ObjectProperty(None)
    hiscore_lbl_menu = ObjectProperty(None)    
    level_lbl_menu = ObjectProperty(None)    
    game_area = ObjectProperty(None)
    menu_screen = ObjectProperty(None)
    screen_manager = ObjectProperty(None)
    boundaries_line_bottom = ObjectProperty(None)
    boundaries_line_top = ObjectProperty(None)
    brickanoid_logic = None
    gfx_properties = dict()
    brickanoid_logic = ObjectProperty(None)
    _banner = None

    def start(self):
        global main_game_screen 
        main_game_screen = self
        self.gfx_properties['game_screen'] = self
        self.gfx_properties['game_area'] = self.game_area
        self.gfx_properties['score_lbl'] = self.score_lbl
        self.gfx_properties['lives_lbl'] = self.lives_lbl
        self.gfx_properties['level_lbl'] = self.level_lbl
        self.gfx_properties['score_lbl_menu'] = self.menu_screen.score_lbl_menu
        self.gfx_properties['hiscore_lbl_menu'] = self.menu_screen.hiscore_lbl_menu
        self.gfx_properties['level_lbl_menu'] = self.menu_screen.level_lbl_menu
        self.gfx_properties['boundaries_line_bottom'] = self.boundaries_line_bottom
        self.gfx_properties['boundaries_line_top'] = self.boundaries_line_top
        self.gfx_properties['screen_width'] = Window.width
        self.gfx_properties['screen_height'] = Window.height
        self.gfx_properties['screen_top'] = int(Window.height * 11 / 12 - Window.height * 0.03)
        self.gfx_properties['screen_bottom'] = int(Window.height * 11 / 12 - 
                                              Window.height * 0.02 - Window.height / 6 * 5)
        self.gfx_properties['screen_right'] = (Window.width % 16) /2
        self.gfx_properties['unitary_width'] = Window.width // 16
        self.gfx_properties['unitary_height'] = Window.height // 30
        load_resources()

        if platform != 'android' and platform != 'ios':
            # linux/win/macos specific stuff. Keyboard binds for example
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)

        self.brickanoid_logic = brickanoid_logic.BrickanoidLogic(self)
        self.brickanoid_logic.game_start()
        self.brickanoid_logic.pause()
        self.to_menu()

    def to_menu(self):
        self.screen_manager.current = 'menu'

    def to_continue(self):
        self.screen_manager.current = 'game'
        self.brickanoid_logic.continue_level()

    def to_restart(self):
        self.screen_manager.current = 'game'
        self.brickanoid_logic = brickanoid_logic.BrickanoidLogic(self)
        self.brickanoid_logic.game_start()
        self.brickanoid_logic.continue_level()

    def show_banner(self, text):
        self._banner = NotifyBanner()
        self._banner.text = text
        self._banner.pos = (-self._banner.width * 2, self.gfx_properties['screen_height'] / 4)
        anim = Animation(x=self.gfx_properties['screen_width'], d=2.)
        #anim = Animation(pos_hint={'x': 1, 'y': 0.5}, d=1.)
        anim.start(self._banner)
        anim.bind(on_complete=self._stop_banner)
        self.draw_gfx(self._banner)

    def _stop_banner(self, animation, widget):
        if self._banner:
            self.remove_gfx(self._banner)
            self._banner = None

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print("premuto %s" % keycode[1])

        if keycode[1] == 'left':
            self.brickanoid_logic.move_left()
            return True

        elif keycode[1] == 'right':
            self.brickanoid_logic.move_right()
            return True

        elif keycode[1] == 'spacebar':
            self.brickanoid_logic.fire()
            return True

        return False

    def update(self, dt):
        if not self._banner:
            self.brickanoid_logic.game_update()
        for elem in self.game_area.children:
            if isinstance(elem, GfxElement):
                elem.animate(dt)
        #print("FPS: %f" % Clock.get_fps())

    def clear_gfx(self):
        self.game_area.clear_widgets()

    def draw_gfx(self, gfx_elem):
        if gfx_elem not in self.game_area.children:
            self.game_area.add_widget(gfx_elem)

    def remove_gfx(self, gfx_elem):
        if gfx_elem in self.game_area.children:
            self.game_area.remove_widget(gfx_elem)


