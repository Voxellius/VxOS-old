# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.platform

heldKeys = []

ctrlHeld = False
shiftHeld = False
symbolHeld = False

class Key:
    def __init__(self, key, text = None):
        self.key = key
        self.text = text if text != None else key

    def __repr__(self):
        return "[%s]" % (self.text)

class PrintingKey(Key):
    def __init__(self, key, text = None):
        super().__init__(key, text)

_K = Key
_PK = PrintingKey

_selectKey = Key("select")

KEYMAP_DEFAULT = [
    _K("back"), _K("ctrl"), _PK("comma", ","), _K("left"), _K("up"), _K("down"), _K("right"), _PK("dot", "."), _K("home"), _K("power"),
    _PK("q"), _PK("w"), _PK("e"), _PK("r"), _PK("t"), _PK("y"), _PK("u"), _PK("i"), _PK("o"), _PK("p"),
    _PK("a"), _PK("s"), _PK("d"), _PK("f"), _PK("g"), _PK("h"), _PK("j"), _PK("k"), _PK("l"), _K("backspace"),
    _K("shift"), _PK("z"), _PK("x"), _PK("c"), _PK("v"), _PK("b"), _PK("n"), _PK("m"), _K("symbol"), _PK("space", " "),
    _selectKey
]

KEYMAP_SHIFT = [
    _K("back"), _K("ctrl"), _PK("apostrophe", "'"), _K("left"), _K("up"), _K("down"), _K("right"), _PK("exclamationMark", "!"), _K("home"), _K("power"),
    _PK("Q"), _PK("W"), _PK("E"), _PK("R"), _PK("T"), _PK("Y"), _PK("U"), _PK("I"), _PK("O"), _PK("P"),
    _PK("A"), _PK("S"), _PK("D"), _PK("F"), _PK("G"), _PK("H"), _PK("J"), _PK("K"), _PK("L"), _K("backspace"),
    _K("shift"), _PK("Z"), _PK("X"), _PK("C"), _PK("V"), _PK("B"), _PK("N"), _PK("M"), _K("symbol"), _PK("space", " "),
    _selectKey
]

KEYMAP_SYMBOL = [
    _K("auto1"), _K("auto2"), _K("auto3"), _K("left"), _K("up"), _K("down"), _K("right"), _K("emoji"), _K("help"), _K("power"),
    _PK("1"), _PK("2"), _PK("3"), _PK("4"), _PK("5"), _PK("6"), _PK("7"), _PK("8"), _PK("9"), _PK("0"),
    _PK("quotationMark", "\""), _PK("colon", ":"), _PK("pound", "£"), _PK("dollar", "$"), _PK("percent", "%"), _PK("caret", "^"), _PK("ampersand", "&"), _PK("asterisk", "*"), _PK("leftBracket", "("), _PK("rightBracket", ")"),
    _PK("semicolon", ";"), _PK("semicolon", ";"), _PK("at", "@"), _PK("hash", "#"), _PK("slash", "/"), _PK("dash", "-"), _PK("equal", "="), _PK("questionMark", "?"), _K("symbol"), _K("enter"),
    _selectKey
]

KEYMAP_SHIFT_SYMBOL = [
    _K("auto4"), _K("auto5"), _K("auto6"), _K("left"), _K("up"), _K("down"), _K("right"), _K("search"), _K("help"), _K("power"),
    _PK("interrobang", "‽"), _PK("pi", "π"), _PK("pipe", "|"), _PK("registered", "®"), _PK("trademark", "™"), _PK("plusMinus", "±"), _PK("interpunct", "·"), _PK("emDash", "—"), _PK("leftBraceBracket", "{"), _PK("rightBraceBracket", "}"),
    _PK("backtick", "`"), _PK("cent", "¢"), _PK("yen", "¥"), _PK("euro", "€"), _PK("permille", "‰"), _PK("degree", "°"), _PK("divide", "÷"), _PK("multiply", "×"), _PK("leftSquareBracket", "["), _PK("rightSquareBracket", "]"),
    _K("shift"), _PK("lessThan", "<"), _PK("greaterThan", ">"), _PK("copyright", "©"), _PK("backslash", "\\"), _PK("underscore", "_"), _PK("plus", "+"), _PK("tilde", "~"), _K("symbol"), _K("delete"),
    _selectKey
]

def getKey(keyIndex):
    if shiftHeld and symbolHeld:
        return KEYMAP_SHIFT_SYMBOL[keyIndex]

    if symbolHeld:
        return KEYMAP_SYMBOL[keyIndex]

    if shiftHeld:
        return KEYMAP_SHIFT[keyIndex]

    return KEYMAP_DEFAULT[keyIndex]

if vx.platform.IS_REAL_HARDWARE:
    import board
    import keypad
    import digitalio

    matrix = keypad.KeyMatrix(
        row_pins = (board.A1, board.A2, board.A3, board.A4),
        column_pins = (board.A5, board.MISO, board.RX, board.TX, board.D12, board.D11, board.D10, board.D9, board.D6, board.D5)
    )

    selectButton = digitalio.DigitalInOut(board.A0)
    selectButton.direction = digitalio.Direction.INPUT
    selectButton.pull = digitalio.Pull.UP

    def poll():
        while True:
            event = matrix.events.get()

            if not event:
                break

            key = getKey(event.key_number)

            if event.pressed and key not in heldKeys:
                heldKeys.append(key)
            
            if not event.pressed and key in heldKeys:
                heldKeys.remove(key)

        if not selectButton.value and _selectKey not in heldKeys:
            heldKeys.append(_selectKey)

        if selectButton.value and _selectKey in heldKeys:
            heldKeys.remove(_selectKey)

        return heldKeys
else:
    import pygame

    matrix = None

    keySimulationOrder = [
        pygame.K_F1, pygame.K_F2, pygame.K_F3, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_F4, pygame.K_F5, pygame.K_F6,
        pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p,
        pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_BACKSPACE,
        pygame.K_LSHIFT, pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA, pygame.K_SPACE,
        pygame.K_RETURN
    ]

    def poll():
        global heldKeys

        pygamePressedKeys = pygame.key.get_pressed()

        for i in range(0, len(pygamePressedKeys)):
            if i not in keySimulationOrder:
                continue

            key = getKey(keySimulationOrder.index(i))

            if pygamePressedKeys[i] == 1 and key not in heldKeys:
                heldKeys.append(key)

            if pygamePressedKeys[i] == 0 and key in heldKeys:
                heldKeys.remove(key)

        return heldKeys