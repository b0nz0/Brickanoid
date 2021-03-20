from kivy.vector import Vector
from time import perf_counter
import brickanoid_elements
import brickanoid_levels
from random import randint
import numpy as np
from kivy.storage.jsonstore import JsonStore

class LevelMatrix():
    _matrix = None
    def __init__(self, rows, columns):
        self._rows = rows
        self._columns = columns
        self._matrix = np.zeros((self._columns, self._rows), dtype=np.int8)
    
    @property
    def rows(self):
        return self._rows
    
    @property
    def columns(self):
        return self._columns

    def is_free(self, x, y, width, height):
        try:
            for i in range(x, x + width):
                for j in range (y, y + height):
                    if self._matrix[i][j] != 0:
                        return False
            return True
        except IndexError:
            return False

    def occupy(self, x, y, width, height):
        try:
            if self.is_free(x, y, width, height):
                for i in range(x, x + width):
                    for j in range (y, y + height):
                        self._matrix[i][j] = 1
        except IndexError:
            raise ValueError('Game screen out of bounds: (%d, %d)' % (x, y))
                
class BrickanoidLogic():
    # all the bricks
    _bricks=[]
    # all the balls
    _balls=[]
    # the pad
    _pad = None
    # for performance counting
    _starting_time = None

    # # of lives
    _lives = 3
    # gam eover status
    _game_over = False
    # score
    _score = 0
    # hiscore
    _hiscore = 0
    #current level
    _level = 0
    # max level reached
    _hilevel = 1
    # process a fire event
    _process_fire = False
    # waiting for next level
    _level_clear = True
    #paused
    _pause = False
    #true if animation for new level must start
    _starting_new_level = True

    # game properties from gfx
    _unitary_width = 0
    _unitary_height = 0
    _screen_top = 0
    _screen_right = 0
    _screen_width = 0
    _game_screen = None
    _boundaries_line_bottom = None
    _boundaries_line_top = None
    _lives_lbl = None
    _score_lbl = None

    # level mgmt
    _level_loader = None

    def __init__(self, game_screen):
        self._game_screen = game_screen
        self._level_loader = brickanoid_levels.load_levels(self)

    def game_start(self):
        self._starting_time = perf_counter()

        self._unitary_width = self._game_screen.gfx_properties['unitary_width']
        self._unitary_height = self._game_screen.gfx_properties['unitary_height']
        self._screen_top = self._game_screen.gfx_properties['screen_top'] 
        self._screen_right = self._game_screen.gfx_properties['screen_right'] 
        self._screen_width = self._game_screen.gfx_properties['screen_width'] 
        self._boundaries_line_bottom = self._game_screen.gfx_properties['boundaries_line_bottom']
        self._boundaries_line_top = self._game_screen.gfx_properties['boundaries_line_top']
        self._lives_lbl = self._game_screen.gfx_properties['lives_lbl']
        self._score_lbl = self._game_screen.gfx_properties['score_lbl']
        self._level_lbl = self._game_screen.gfx_properties['level_lbl']
        self._score_lbl_menu = self._game_screen.gfx_properties['score_lbl_menu']
        self._hiscore_lbl_menu = self._game_screen.gfx_properties['hiscore_lbl_menu'] 
        self._level_lbl_menu = self._game_screen.gfx_properties['level_lbl_menu']
        self._level_spinner_menu = self._game_screen.gfx_properties['level_spinner_menu']
        self._game_screen = self._game_screen.gfx_properties['game_screen']
        self._menu_screen = self._game_screen.menu_screen

        self._lives = 3
        self._game_over = False
        self._score = 0
        self._level = int(self._level_spinner_menu.text)       
        self._process_fire = False
        self._level_clear = True
        self._pause = False
        self._bricks=[]
        self._balls=[]
        self._pad = None
        self._level_matrix = LevelMatrix(16, 16)
        self._has_touch_down = False
        self._starting_new_level = True
        self._moving_left = False
        self._moving_right = False

        
        self._store = JsonStore('brickanoid.json')
        try:
            store = self._store.get('hiscore')
            self._hiscore = int(store['value'])
            store = self._store.get('hilevel')
            self._hilevel = int(store['value'])
        except KeyError:
            self._store.put('hiscore', value=0)
            self._store.put('hilevel', value=1)
            #self._store.put('hilevel', 1)
            self._hiscore = 0
            self._hilevel = 1
        # his = list(self._store.find(name='hiscore'))
        # if len(his) > 0:
        #     self._hiscore = his[0][1]['value']
        self._hiscore_lbl_menu.text = str(self._hiscore)
        self._update_level_spinner()

    def _update_level_spinner(self):        
        level_values = []
        for i in range(1, self._hilevel + 1):
            level_values.append(str(i))
        self._level_spinner_menu.values = level_values

        #self._check_end_level()

    # add a brick to level at column i (starting from left) and row j (starting from top)
    # uses next space avialable depending on previous bricks
    # if i = j = -1 simply find next space available
    def add_brick_to_screen(self, brick, i=-1, j=-1):
        if i == -1 or j == -1:
            for y, x in np.ndindex((self._level_matrix.columns, self._level_matrix.rows)):
                if self._level_matrix.is_free(x, y, brick.bwidth, brick.bheight):
                    brick.pos = (self._screen_right + (x * self._unitary_width), 
                                 self._screen_top - (y * self._unitary_height)) 
                    self._level_matrix.occupy(x, y, brick.bwidth, brick.bheight)
                    self._bricks.append(brick)
                    return True
        else:
            brick.pos = (self._screen_right + (i * self._unitary_width), 
                         self._screen_top - (j * self._unitary_height)) 
            self._level_matrix.occupy(i, j, brick.bwidth, brick.bheight)
            self._bricks.append(brick)
            return True
        return False

    def _create_random_ball(self):
        ball = brickanoid_elements.BallAnoid()
        # put it at center of pad
        ball.pos = (self._pad.pos[0] + self._pad.widget.width / 2 - ball.radius, \
                    self._pad.pos[1] + self._pad.widget.height)
        ball.velocity = (0, 0)
        self._balls.append(ball)
    
    def _fire_balls(self):
        for ball in self._balls:
            if ball.is_idle():
                rr = randint(-15, +15)
                ball.velocity = Vector((0, self._unitary_height/4)).rotate(rr)
                print("vector: (%d) %s" % (rr, repr(ball.velocity)))

    def _check_collision_balls_bricks(self):
        bricks_to_remove=[]
        for ball in self._balls:
            if ball.is_idle():
                continue
            for brick in self._bricks:
                # horizontal collision from left
                if brick.widget.collide_point((ball.pos[0] + 2 * ball.radius), (ball.pos[1] + ball.radius)):
                    print("collisione LEFT in %d, %d - %d, %d" % 
                        (ball.pos[0], ball.pos[1], brick.pos[0], brick.pos[1]))
                    vx, vy = ball.velocity
                    ball.velocity = - vx, vy
                    ball.pos[0] -= 2
                    self._game_screen.play_sound('brick_hit')
                    if brick.collided():
                        bricks_to_remove.append(brick)
                        self._score += brick.points
                    
                # horizontal collision from right
                elif brick.widget.collide_point((ball.pos[0]), (ball.pos[1] + ball.radius)):
                #if ball.widget.collide_widget(brick.widget):
                    print("collisione RIGHT in %d, %d - %d, %d" % 
                        (ball.pos[0], ball.pos[1], brick.pos[0], brick.pos[1]))
                    vx, vy = ball.velocity
                    ball.velocity = - vx, vy
                    ball.pos[0] += 2
                    self._game_screen.play_sound('brick_hit')
                    if brick.collided():
                        bricks_to_remove.append(brick)
                        self._score += brick.points
                    
                # vertical collision from bottom
                elif brick.widget.collide_point((ball.pos[0] + ball.radius), (ball.pos[1] + 2 * ball.radius)):
                    print("collisione BOTTOM in %d, %d - %d, %d" % 
                        (ball.pos[0], ball.pos[1], brick.pos[0], brick.pos[1]))
                    vx, vy = ball.velocity
                    ball.velocity = vx, - vy
                    ball.pos[1] -= 2
                    self._game_screen.play_sound('brick_hit')
                    if brick.collided():
                        bricks_to_remove.append(brick)
                        self._score += brick.points
                    
                #vertical collision from top
                elif brick.widget.collide_point((ball.pos[0] + ball.radius), (ball.pos[1])):
                    print("collisione TOP in %d, %d - %d, %d" % 
                        (ball.pos[0], ball.pos[1], brick.pos[0], brick.pos[1]))
                    vx, vy = ball.velocity
                    ball.velocity = vx, - vy
                    ball.pos[1] += 2
                    self._game_screen.play_sound('brick_hit')
                    if brick.collided():
                        bricks_to_remove.append(brick)
                        self._score += brick.points
                    
        return bricks_to_remove
                
    def _check_collision_balls_border(self):
        deadballs = []

        for ball in self._balls:
            vx, vy = ball.velocity
            # right border
            if (ball.pos[0]) <= self._screen_right:
                vx *= -1
                ball.pos[0] += 1
                print("collisione X in %d, %d" % 
                        (ball.pos[0], ball.pos[1]))
            # right border
            elif (ball.pos[0] + 2 * ball.radius) >= self._screen_width - (2 * self._screen_right):
                vx *= -1
                ball.pos[0] -= 1
                print("collisione X in %d, %d" % 
                        (ball.pos[0], ball.pos[1]))            
            # top bar
            elif ball.widget.collide_widget(self._boundaries_line_top):
                vy *= -1
                ball.pos[1] -= 1
                print("collisione Y in %d, %d" % 
                        (ball.pos[0], ball.pos[1]))
            # bottom
            elif ball.widget.collide_widget(self._boundaries_line_bottom):
                print("morte Y in %d, %d" % 
                        (ball.pos[0], ball.pos[1]))
                deadballs.append(ball)
            ball.velocity = vx, vy       
        return deadballs

    def _check_collision_balls_pad(self):
        for ball in self._balls:
            if ball.is_idle():
                continue
            vx, vy = ball.velocity
            # if somehow the ball is going up, ignore this event
            if vy > 0.:
                continue
            # check if collision happens only from top
            # if self._pad.widget.collide_point(ball.pos[0] + ball.radius, ball.pos[1]) and \
            #     not self._pad.widget.collide_point(ball.pos[0], ball.pos[1] + ball.radius) and \
            #     not self._pad.widget.collide_point(ball.pos[0] + 2 * ball.radius, ball.pos[1] + ball.radius):
            if self._pad.widget.collide_widget(ball.widget) and \
                (self._pad.pos[1] + self._pad.widget.height) - ball.pos[1] < 10:
                print("preso pad in %d, %d" % 
                        (ball.pos[0], ball.pos[1]))
                vy *= -1
                offset = self._pad.pos[0] + (self._pad.widget.width / 2) - (ball.pos[0] + ball.radius)
                ball.velocity = vx - offset / 4, vy       
                self._game_screen.play_sound('pad_hit')

    def _check_end_life(self):
        if len(self._balls) == 0:
            print("MORTO!")
            self._game_screen.play_sound('game_over')
            if self._lives > 0:
                self._create_random_ball()
                self._lives -= 1
            return True
    
    def _check_end_level(self):
        # count only non-indestructible bricks
        actbricks = [brick for brick in self._bricks if brick.strength > 0]
        if len(actbricks) == 0 and not self._pause:
            # no more bricks
            print("VITTORIA!")

            self._level_matrix = LevelMatrix(16, 16)
            self._game_screen.clear_gfx()
            self._balls = []
            self._bricks = []
            self._pad = None
            self._level_clear = True
            self._level += 1
            self._starting_new_level = True
            return True
        return False

    def pause(self):
        self._pause = True

    def continue_level(self):
        self._pause = False
        if self._game_over:
            self.game_start()
        elif not self._level_clear:
            return
        self._game_screen.clear_gfx()
        if self._level == 0:
            self._level = 1 
        self._level_loader.load_level(self._level)

        self._pad = brickanoid_elements.PadYellow_2()
        self._pad.pos = (self._screen_width // 2 - self._pad._widget.width // 2, 
                                self._screen_top - (24.5 * self._unitary_height))

        self._create_random_ball()
        self._level_clear = False

    def _check_fire(self):
        if self._process_fire:
            self._fire_balls()
            self._process_fire = False

    def touch_move(self, x, y):
        if not self._pad:
            return
        newx, newy = self._pad.pos
        newx = x - self._pad.widget.width / 2
        if newx < 0:
            newx = 0
        elif newx + self._pad.widget.width > self._screen_width:
            newx = self._screen_width - self._pad.widget.width
        self._pad.pos = (newx, newy)
        self._has_touch_down = False

        # see if any ball is stick to the pad and in case move it
        for ball in self._balls:
            if ball.is_idle():
                ball.pos = (newx + self._pad.widget.width / 2 - ball.radius, \
                    ball.pos[1])


    def touch_down(self, x, y):
        self._has_touch_down = True

    def touch_up(self, x, y):
        # touched and released.... a tap?
        if self._has_touch_down:
            self.fire()

    def move_left(self):
        self._moving_left = True
        self._moving_right = False

    def move_right(self):
        self._moving_left = False
        self._moving_right = True

    def stop_left(self):
        self._moving_left = False

    def stop_right(self):
        self._moving_right = False

    def fire(self):
        self._process_fire = True

    def game_update(self):
        '''
        1. muovo palline (secondo posizione e velocità) OK
        3. verifico collisione pad-pallina OK
        4. verifico collissione pallina-bricks OK
        5. verifica collisione pallina-nemici
        6. verifica collisione proiettili-bricks
        7. verifica collisione proiettili-nemici
        8. verifica collisione potenziamento-pad
        6. disegna sfondo
        7. disegna bricks OK
        8. disegna nemici
        9. disegna pad OK
        10. disegna proiettili
        11. verifica perdita vita OK
        11. verifica fine vite OK
        12. verifica vittoria livello OK
        '''

        #secs = int(perf_counter() - _starting_time)
        #game_screen.count_lbl.text = str(secs)
        #game_screen.score_lbl.text = str(secs*123)

        # game_screen.clear_gfx()
        if self._game_over:
            self._game_screen.to_menu()
            return

        self._score_lbl_menu.text = str(self._score)
        self._level_lbl_menu.text = str(self._level)

        # if self._game_screen.is_showing_banner():
        #     return

        if self._level == 0:
           self._check_end_level()

        if self._starting_new_level:
            self.continue_level()
            self._game_screen.show_banner("Level %d" % self._level)
            self._game_screen.play_sound('game_start')
            self._starting_new_level = False
            return

        elif self._check_end_level():
            #self._game_screen.to_menu()
            self._score += (self._level - 1) * 100
            #self.pause()
            self._starting_new_level = True
            if self._level > self._hilevel:
                self._hilevel = self._level
                self._store.put('hilevel', value=self._hilevel)
                self._update_level_spinner()
            self._game_screen.show_banner("Level %d clear" % (self._level-1))
            return

        if self._pause:
            return

        self._check_fire()

        # move every ball
        for elem in self._balls:
            elem.move()

        # move te pad accoringly to its speed        
        if self._pad:
            self._pad.move()
            if self._moving_left:
                self.touch_move(self._pad.pos[0]-5 + self._pad.widget.width / 2, self._pad.pos[1])
            elif self._moving_right:
                self.touch_move(self._pad.pos[0]+5 + self._pad.widget.width / 2, self._pad.pos[1])

        # check collision with bricks. Check if some brick has to be removed
        deadbricks = self._check_collision_balls_bricks()
        if len(deadbricks) > 0:
            for brick in deadbricks:
                self._game_screen.remove_gfx(brick.widget)
                self._bricks.remove(brick)

        # check if a ball reached bottom. If no balls remained it is Gave Over
        deadballs = self._check_collision_balls_border()
        if len(deadballs) > 0:
            for ball in deadballs:
                self._game_screen.remove_gfx(ball.widget)
                self._balls.remove(ball)
        if self._check_end_life():
            if self._lives == 0:
                self._game_screen.show_banner("Game Over")
                self._game_over = True
        
        self._check_collision_balls_pad()

        # show # of lives and score
        self._lives_lbl.text = str(self._lives)
        self._score_lbl.text = str(self._score)
        self._level_lbl.text = str(self._level)

        if self._score > self._hiscore:
            self._hiscore = self._score 
            self._hiscore_lbl_menu.text = str(self._hiscore)
            self._store.put('hiscore', value=self._hiscore)

        # draw bricks, balls and the pad
        for elem in self._bricks:
            self._game_screen.draw_gfx(elem.widget)
        for elem in self._balls:
            self._game_screen.draw_gfx(elem.widget)

        if self._pad:
            self._game_screen.draw_gfx(self._pad.widget)
        #print("aggiornato pad: %f" % perf_counter())

