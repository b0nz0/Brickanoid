from kivy.vector import Vector
from kivy.animation import Animation
import brickanoid_gfx 

class BaseElem():
    _pos = (0, 0)
    _widget = None

    @property
    def widget(self):
        return self._widget

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        self._widget.pos = self._pos

class PadYellow_2(BaseElem):
    velocity = Vector((0, 0))

    def __init__(self):
        self._widget = brickanoid_gfx.PadYellow_2()

    @property
    def pos(self):
        return self._pos
    
    @pos.setter
    def pos(self, pos):
        self._pos = pos
        # deltax = pos[0] - self._pos[0]
        # if deltax < 20 or deltax > 20:
        #     Animation.cancel_all(self.widget)
        #     pad_anim = Animation(x=pos[0], y=pos[1], duration=0.1, t='out_sine')
        #     pad_anim.start(self.widget)
        # else:
        #     Animation.cancel_all(self.widget)
        self._widget.pos = self._pos

    # def move_to(self, target):
    #     deltax = target - self._pos[0]
    #     print ("target: %d, x: %d, deltax: %f" % (target, self._pos[0], deltax))
    #     self.velocity = Vector(deltax/2, 0)

    def move(self):
        pass
    #     self._pos = Vector(*self.velocity) + self._pos
    #     if self.widget:
    #         self.widget.pos = self._pos
    #         print("pad pos: %f" % self._pos[0])

class BallAnoid(BaseElem):
    velocity = (0, 0)

    def __init__(self):
        super(BallAnoid, self).__init__()
        self._widget = brickanoid_gfx.BallAnoid()

    @property
    def radius(self):
        return self._widget.size[0] // 2

    def move(self):
        self._pos = Vector(*self.velocity) + self._pos
        if self.widget:
#            self.widget.pos_hint = {'center_x': self.pos[0], 'center_y' : self.pos[1]}
            self.widget.pos = self._pos

    def is_idle(self):
        return self.velocity == (0, 0)

class BaseBrick(BaseElem):
    _points = 0
    _pos_hint = {}
    _bheight = 1
    _bwidth = 1
    _strength = 1 # remove after 1 hit. 0 means indestructible

    @property
    def points(self):
        return self._points

    @property
    def bheight(self):
        return self._bheight

    @property
    def bwidth(self):
        return self._bwidth

    # returns true if brick has to be removed and points assigned
    def collided(self):
        if self._strength == 0:
            return False
        else: 
            self._strength -= 1
        if self._strength > 0:
            return False
        else:
            return True

class BrickRed_1_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickRed_1_0()
        self._points = 2
        self._bheight = 1
        self._bwidth = 1

class BrickRed_2_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickRed_2_0()
        self._points = 4
        self._bheight = 1
        self._bwidth = 2

class BrickRed_3_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickRed_3_0()
        self._points = 6
        self._bheight = 1
        self._bwidth = 3

class BrickRed_4_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickRed_4_0()
        self._points = 8
        self._bheight = 1
        self._bwidth = 4

class BrickBlu_1_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickBlu_1_0()
        self._points = 2
        self._bheight = 1
        self._bwidth = 1

class BrickBlu_2_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickBlu_2_0()
        self._points = 4
        self._bheight = 1
        self._bwidth = 2

class BrickBlu_3_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickBlu_3_0()
        self._points = 6
        self._bheight = 1
        self._bwidth = 3

class BrickBlu_4_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickBlu_4_0()
        self._points = 8
        self._bheight = 1
        self._bwidth = 4

class BrickGreen_1_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGreen_1_0()
        self._points = 2
        self._bheight = 1
        self._bwidth = 1

class BrickGreen_2_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGreen_2_0()
        self._points = 4
        self._bheight = 1
        self._bwidth = 2

class BrickGreen_3_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGreen_3_0()
        self._points = 6
        self._bheight = 1
        self._bwidth = 3

class BrickGreen_4_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGreen_4_0()
        self._points = 8
        self._bheight = 1
        self._bwidth = 4

class BrickPink_1_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickPink_1_0()
        self._points = 2
        self._bheight = 1
        self._bwidth = 1

class BrickPink_2_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickPink_2_0()
        self._points = 4
        self._bheight = 1
        self._bwidth = 2

class BrickPink_3_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickPink_3_0()
        self._points = 6
        self._bheight = 1
        self._bwidth = 3

class BrickPink_4_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickPink_4_0()
        self._points = 8
        self._bheight = 1
        self._bwidth = 4

class BrickSilv_1_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickSilv_1_0()
        self._points = 5
        self._bheight = 1
        self._bwidth = 1

class BrickSilv_2_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickSilv_2_0()
        self._points = 10
        self._bheight = 1
        self._bwidth = 2

class BrickSilv_3_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickSilv_3_0()
        self._points = 15
        self._bheight = 1
        self._bwidth = 3

class BrickSilv_4_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickSilv_4_0()
        self._points = 20
        self._bheight = 1
        self._bwidth = 4

class BrickGold_1_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGold_1_0()
        self._points = 10
        self._bheight = 1
        self._bwidth = 1
        self._strength = 2

class BrickGold_2_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGold_2_0()
        self._points = 20
        self._bheight = 1
        self._bwidth = 2
        self._strength = 2

class BrickGold_3_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGold_3_0()
        self._points = 30
        self._bheight = 1
        self._bwidth = 3
        self._strength = 2

class BrickGold_4_0(BaseBrick):
    def __init__(self):
        self._widget = brickanoid_gfx.ImgBrickGold_4_0()
        self._points = 40
        self._bheight = 1
        self._bwidth = 4
        self._strength = 2
