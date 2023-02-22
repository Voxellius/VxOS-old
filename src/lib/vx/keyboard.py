# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import vx.platform

heldKeys = []
pressedKeys = []
releasedKeys = []

ctrlHeld = False
shiftHeld = False
symbolHeld = False

class Key:
    def __init__(self, name, text = None):
        self.name = name
        self.text = text if text != None else name

    def __repr__(self):
        return "[%s]" % (self.text)

class PrintingKey(Key):
    def __init__(self, name, text = None):
        super().__init__(name, text)

_K = Key
_PK = PrintingKey

_selectKey = Key("select")
_ctrlKey = Key("ctrl")
_shiftKey = Key("shift")
_symbolKey = Key("symbol")

KEYMAP_DEFAULT = [
    _ctrlKey, _PK("comma", ","), _K("left"), _K("up"), _K("down"), _K("right"), _PK("dot", "."), _K("home"),
    _PK("w"), _PK("e"), _PK("r"), _PK("t"), _PK("y"), _PK("u"), _PK("i"), _PK("o"),
    _PK("s"), _PK("d"), _PK("f"), _PK("g"), _PK("h"), _PK("j"), _PK("k"), _PK("l"),
    _PK("z"), _PK("x"), _PK("c"), _PK("v"), _PK("b"), _PK("n"), _PK("m"), _symbolKey,
    _K("back"), _PK("q"), _PK("a"), _shiftKey, _PK("space", " "), _K("backspace"), _PK("p"), _K("power"),
    _selectKey
]

KEYMAP_SHIFT = [
    _ctrlKey, _PK("apostrophe", "'"), _K("left"), _K("up"), _K("down"), _K("right"), _PK("exclamationMark", "!"), _K("home"),
    _PK("W"), _PK("E"), _PK("R"), _PK("T"), _PK("Y"), _PK("U"), _PK("I"), _PK("O"),
    _PK("S"), _PK("D"), _PK("F"), _PK("G"), _PK("H"), _PK("J"), _PK("K"), _PK("L"),
    _PK("Z"), _PK("X"), _PK("C"), _PK("V"), _PK("B"), _PK("N"), _PK("M"), _symbolKey,
    _K("back"), _PK("Q"), _PK("A"), _shiftKey, _PK("space", " "), _K("backspace"), _PK("P"), _K("power"),
    _selectKey
]

KEYMAP_SYMBOL = [
    _K("auto2"), _K("auto3"), _K("left"), _K("up"), _K("down"), _K("right"), _K("emoji"), _K("help"),
    _PK("2"), _PK("3"), _PK("4"), _PK("5"), _PK("6"), _PK("7"), _PK("8"), _PK("9"),
    _PK("colon", ":"), _PK("pound", "£"), _PK("dollar", "$"), _PK("percent", "%"), _PK("caret", "^"), _PK("ampersand", "&"), _PK("asterisk", "*"), _PK("leftBracket", "("),
    _PK("semicolon", ";"), _PK("at", "@"), _PK("hash", "#"), _PK("slash", "/"), _PK("dash", "-"), _PK("equal", "="), _PK("questionMark", "?"), _symbolKey,
    _K("auto1"), _PK("1"), _PK("quotationMark", "\""), _shiftKey, _K("enter"), _PK("rightBracket", ")"), _PK("0"), _K("power"),
    _selectKey
]

KEYMAP_SHIFT_SYMBOL = [
    _K("auto5"), _K("auto6"), _K("left"), _K("up"), _K("down"), _K("right"), _K("search"), _K("help"),
    _PK("pi", "π"), _PK("pipe", "|"), _PK("registered", "®"), _PK("trademark", "™"), _PK("plusMinus", "±"), _PK("interpunct", "·"), _PK("bullet", "•"), _PK("leftBraceBracket", "{"),
    _PK("cent", "¢"), _PK("yen", "¥"), _PK("euro", "€"), _PK("permille", "‰"), _PK("degree", "°"), _PK("divide", "÷"), _PK("multiply", "×"), _PK("leftSquareBracket", "["),
    _PK("lessThan", "<"), _PK("greaterThan", ">"), _PK("copyright", "©"), _PK("backslash", "\\"), _PK("underscore", "_"), _PK("plus", "+"), _PK("tilde", "~"), _symbolKey,
    _K("auto4"), _PK("section", "§"), _PK("backtick", "`"), _shiftKey, _K("delete"), _PK("rightSquareBracket", "]"), _PK("rightBraceBracket", "}"), _K("power"),
    _selectKey
]

def keyBeingHeld(keyName):
    for key in heldKeys:
        if key.name == keyName:
            return True

    return False

def getKeymap():
    if keyBeingHeld("shift") and keyBeingHeld("symbol"):
        return KEYMAP_SHIFT_SYMBOL

    if keyBeingHeld("symbol"):
        return KEYMAP_SYMBOL

    if keyBeingHeld("shift"):
        return KEYMAP_SHIFT

    return KEYMAP_DEFAULT

def getKey(keyIndex):
    return getKeymap()[keyIndex]

def cleanHeldKeys():
    keyMap = getKeymap()

    for key in heldKeys[:]:
        if key != _selectKey and key not in keyMap:
            heldKeys.remove(key)

if vx.platform.IS_REAL_HARDWARE:
    import board
    import keypad
    import digitalio

    matrix = keypad.KeyMatrix(
        row_pins = (board.A1, board.A2, board.A3, board.A4, board.A5),
        column_pins = (board.RX, board.TX, board.D12, board.D11, board.D10, board.D9, board.D6, board.D5)
    )

    selectButton = digitalio.DigitalInOut(board.A0)
    selectButton.direction = digitalio.Direction.INPUT
    selectButton.pull = digitalio.Pull.UP

    def poll():
        global heldKeys, pressedKeys, releasedKeys

        pressedKeys = []
        releasedKeys = []

        while True:
            event = matrix.events.get()

            if not event:
                break

            key = getKey(event.key_number)

            if event.pressed and key not in heldKeys:
                heldKeys.append(key)
                pressedKeys.append(key)
            
            if not event.pressed and key in heldKeys:
                heldKeys.remove(key)
                releasedKeys.append(key)

        if not selectButton.value and _selectKey not in heldKeys:
            heldKeys.append(_selectKey)
            pressedKeys.append(_selectKey)

        if selectButton.value and _selectKey in heldKeys:
            heldKeys.remove(_selectKey)
            releasedKeys.append(_selectKey)

        cleanHeldKeys()

        return heldKeys
else:
    import pygame

    matrix = None

    keySimulationOrder = [
        pygame.K_F2, pygame.K_F3, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_F4, pygame.K_F5,
        pygame.K_w, pygame.K_e, pygame.K_r, pygame.K_t, pygame.K_y, pygame.K_u, pygame.K_i, pygame.K_o,
        pygame.K_s, pygame.K_d, pygame.K_f, pygame.K_g, pygame.K_h, pygame.K_j, pygame.K_k, pygame.K_l,
        pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v, pygame.K_b, pygame.K_n, pygame.K_m, pygame.K_COMMA,
        pygame.K_F1, pygame.K_q, pygame.K_a, pygame.K_LSHIFT, pygame.K_SPACE, pygame.K_BACKSPACE, pygame.K_p, pygame.K_F6,
        pygame.K_RETURN
    ]

    def poll():
        global heldKeys, pressedKeys, releasedKeys

        pressedKeys = []
        releasedKeys = []

        pygamePressedKeys = pygame.key.get_pressed()

        for i in range(0, len(keySimulationOrder)):
            j = keySimulationOrder[i]

            if j not in keySimulationOrder:
                continue

            key = getKey(keySimulationOrder.index(j))

            if pygamePressedKeys[j] == 1 and key not in heldKeys:
                heldKeys.append(key)
                pressedKeys.append(key)

            if pygamePressedKeys[j] == 0 and key in heldKeys:
                heldKeys.remove(key)
                releasedKeys.append(key)

        cleanHeldKeys()

        return heldKeys