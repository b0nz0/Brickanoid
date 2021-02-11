import brickanoid_elements

class LevelLoader():
    _logic = None
    _charbuffer = ''
    _level_strings = {}

    def __init__(self, logic):
        self._logic = logic
    
    @staticmethod
    def create_brick(chars):
        if len(chars) < 3:
            raise BufferError("String '{chars}' must contain exactly 3 chars")
        length = chars[0] 
        if length not in ['1', '2', '3', '4']:
            raise ValueError("'{length}' is not a valid brick length")
        color = chars[1]
        enhanc = chars[2]
        if enhanc not in ['n', 'l', 'g', 's']:
            raise ValueError("'{enhanc}' is not a valid brick enhancement")
        
        #dinamically create classname for brick
        classname = 'Brick'
        if color in ['r', 'R']:
            classname = classname + 'Red'
        elif color in ['b', 'B']:
            classname = classname + 'Blu'
        elif color in ['g', 'G']:
            classname = classname + 'Green'
        elif color in ['p', 'P']:
            classname = classname + 'Pink'
        elif color in ['s', 'S']:
            classname = classname + 'Silv'
        elif color in ['d', 'D']:
            classname = classname + 'Gold'
        else:
            raise ValueError("'{color}' is not a valid brick color")

        classname = classname + '_' + length + '_0'
        tt = getattr(brickanoid_elements, classname)
        return tt()

    def define_level(self, level, charbuffer):
        self._level_strings[level] = charbuffer

    def load_level(self, level):
        charbuffer = self._level_strings[level]
        self._current_column = 0
        self._add_from_chars(charbuffer)

    def _add_from_chars(self, charbuffer):
        row = 0
        column = 0
        # remove first empty lines
        while charbuffer[0] in ('\n', '\r'):
            charbuffer = charbuffer[1:]
        while len(charbuffer[3 * column:]) > 3:
            brick = LevelLoader.create_brick(charbuffer[3 * column:])
            if brick:
                # go over next 3 x brick-length chars in buffer
                self._logic.add_brick_to_screen(brick, column, row)
                column += brick.bwidth
                # newline if CR/LF found or end of string
                newrow = False
                while len(charbuffer[3 * column:]) > 0 and \
                      charbuffer[3 * column] in ('\n', '\r'):
                    newrow = True
                    charbuffer = charbuffer[(3 * column) + 1:]
                    column = 0
                if newrow:
                    row += 1


LVL1 = '''
4rnrrrrrrrrr
'''

LVL2 = '''
2rnrrr4snsssssssss
3snssssss3pnpppppp
'''

LVL3 = '''
2rnrrr3snssssss4dnddddddddd
'''

def load_levels(logic):
    level_loader = LevelLoader(logic)
    level_loader.define_level(1, LVL1)
    level_loader.define_level(2, LVL2)
    level_loader.define_level(3, LVL3)
    return level_loader

