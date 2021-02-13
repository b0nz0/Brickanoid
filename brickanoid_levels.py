import brickanoid_elements

LVL0 = '''
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
'''

LVL1 = '''
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
------------------------------------------------
------------------------------------------------
------------------4rnrrrrrrrrr------------------
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
'''

LVL2 = '''
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
------------------------------------------------
------------------3bnbbbbbb---------------------
------------3bnbbbbbb1pn3bnbbbbbb---------------
------------------3bnbbbbbb---------------------
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
'''

LVL3 = '''
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
------------3rnrrrrrr------3rnrrrrrr------------
---------4rnrrrrrrrrr2rnrrr4rnrrrrrrrrr---------
------------3rnrrrrrr2snsss3rnrrrrrr------------
---------------2rnrrr2snsss2rnrrr---------------
---------------3rnrrrrrr3rnrrrrrr---------------
------------------4rnrrrrrrrrr------------------
---------------------2rnrrr---------------------
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
'''

LVL4 = '''
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
---------------1cn------------1cn---------------
---------------1cn4gnggggggggg1cn---------------
---------------1cn---2gnggg---1cn---------------
---------------1cn4gnggggggggg1cn---------------
---------------1cn------------1cn---------------
---------------1cn------------1cn---------------
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
'''

LVL5 = '''
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
------------------------------------------------
---------------1dn4bnbbbbbbbbb1dn---------------
------------------------------------------------
------1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn------
-  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  
'''

LVLEND = '''
------------------4rnrrrrrrrrr------------------
1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn1cn
------------------------------------------------
'''

class LevelLoader():
    _logic = None
    _charbuffer = ''
    _level_strings = {}

    def __init__(self, logic):
        self._logic = logic
    
    @staticmethod
    def create_brick(chars):
        if len(chars) < 3:
            raise BufferError(f"String '{chars}' must contain exactly 3 chars")
        length = chars[0]
        if length not in ['1', '2', '3', '4']:
            raise ValueError(f"'{length}' is not a valid brick length")
        color = chars[1]
        enhanc = chars[2]
        if enhanc not in ['n', 'l', 'g', 's']:
            raise ValueError(f"'{enhanc}' is not a valid brick enhancement")
        
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
        elif color in ['c', 'C']:
            classname = classname + 'Concrete'
        else:
            raise ValueError(f"'{color}' is not a valid brick color")

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
            while charbuffer[3 * column] in ('-', ' '):
                column += 1
                continue
            newrow = False
            while len(charbuffer[3 * column:]) > 0 and \
                    charbuffer[3 * column] in ('\n', '\r'):
                newrow = True
                charbuffer = charbuffer[(3 * column) + 1:]
                column = 0
            if newrow:
                row += 1
                continue
            brick = LevelLoader.create_brick(charbuffer[3 * column:])
            if brick:
                # go over next 3 x brick-length chars in buffer
                self._logic.add_brick_to_screen(brick, column, row)
                column += brick.bwidth
                # newline if CR/LF found or end of string


def load_levels(logic):
    level_loader = LevelLoader(logic)
    level_loader.define_level(1, LVL1)
    level_loader.define_level(2, LVL2)
    level_loader.define_level(3, LVL3)
    level_loader.define_level(4, LVL4)
    level_loader.define_level(5, LVL5)
    level_loader.define_level(6, LVLEND)
    return level_loader

