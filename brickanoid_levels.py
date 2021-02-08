import brickanoid_elements


def create_level_1(logic):
    brick = brickanoid_elements.BrickRed_4_0()
    logic.add_brick_to_screen(brick)

def create_level_2(logic):
    brick = brickanoid_elements.BrickRed_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickSilv_4_0()
    logic.add_brick_to_screen(brick)

def create_level_3(logic):
    brick = brickanoid_elements.BrickRed_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickSilv_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGold_4_0()
    logic.add_brick_to_screen(brick)

def create_level_0(logic):
    brick = brickanoid_elements.BrickRed_1_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickRed_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickRed_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickRed_4_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickBlu_1_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickBlu_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickBlu_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickBlu_4_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGreen_1_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGreen_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGreen_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGreen_4_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickPink_1_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickPink_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickPink_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickPink_4_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickSilv_1_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickSilv_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickSilv_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickSilv_4_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGold_1_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGold_2_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGold_3_0()
    logic.add_brick_to_screen(brick)
    brick = brickanoid_elements.BrickGold_4_0()
    logic.add_brick_to_screen(brick)

def create_level_00(logic):
    for i in range(0, 32):
        brick = brickanoid_elements.BrickRed_1_0()
        logic.add_brick_to_screen(brick)
    for i in range(0, 8):
        brick = brickanoid_elements.BrickBlu_2_0()
        logic.add_brick_to_screen(brick)
    for i in range(0, 8):
        brick = brickanoid_elements.BrickRed_3_0()
        logic.add_brick_to_screen(brick)
    for i in range(0, 8):
        brick = brickanoid_elements.BrickBlu_4_0()
        logic.add_brick_to_screen(brick)
