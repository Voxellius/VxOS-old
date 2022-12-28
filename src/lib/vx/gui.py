# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect
from adafruit_display_text.label import Label

import vx.display

class fonts:
    SANS_REGULAR_16 = ("titilliumweb-regular-16", 1)
    SANS_REGULAR_32 = ("titilliumweb-regular-16", 2)
    SANS_REGULAR_64 = ("titilliumweb-regular-16", 4)
    SANS_NUMERALS_64 = ("titilliumweb-numerals-64", 1)

loadedFonts = {}

class Element:
    def __init__(self, x, y):
        self._x = 0
        self._y = 0
        self._visible = True
        self._focusable = False
        self._focused = False

        self.computedX = 0
        self.computedY = 0

        self.x = x
        self.y = y

        self.parent = None
        self._cachedBuild = None

        self.render()

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

        self.render()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

        self.render()

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value

        self.render()

    @property
    def focused(self):
        return self._focused

    def focus(self):
        self._focused = True

        self.render()

    def render(self):
        if self.parent != None:
            self.computedX = self.parent.computedX + self._x
            self.computedY = self.parent.computedY + self._y

        self._get()

        self._updateBuild()

    def _get(self, rebuild = False):
        if rebuild or self._cachedBuild == None:
            self._cachedBuild = self._build()

        return self._cachedBuild

    def _build(self):
        group = displayio.Group()

        group.hidden = True

        return group

    def _updateBuild(self):
        self._get().hidden = not self._visible

    def _addParent(self, parent):
        self.parent = parent

class Text(Element):
    def __init__(self, x, y, text, font = fonts.SANS_REGULAR_16):
        self._cachedBuild = None

        self.parent = None

        self._text = text
        self._font = font
        self._foreground = vx.display.BLACK

        super().__init__(x, y)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        self.render()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

        self.render()

    @property
    def foreground(self):
        return self._foreground

    @foreground.setter
    def foreground(self, value):
        self._foreground = value

        self.render()

    @property
    def computedWidth(self):
        self.render()

        return self._get().width

    @property
    def computedHeight(self):
        self.render()

        return self._get().height

    def _build(self):
        label = Label(
            font = _getFont(self._font[0]),
            text = self.text,
            x = self.computedX,
            y = self.computedY,
            scale = self._font[1],
            anchor_point = (0, 0),
            color = self.foreground
        )

        label.hidden = True

        return label

    def _updateBuild(self):
        label = self._get()

        label.font = _getFont(self._font[0])
        label.text = self.text
        label.x = self.computedX
        label.y = self.computedY
        label.scale = self._font[1]
        label.color = self.foreground
        label.hidden = not self._visible

class Container(Element):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self._cachedBuild = None

        self.parent = None

        self._children = []

        self.computedX = 0
        self.computedY = 0
        self.computedWidth = 0
        self.computedHeight = 0

        self._width = 0
        self._height = 0
        self._visible = True
        self._focused = False

        self.width = width
        self.height = height
        self.xMargin = xMargin
        self.yMargin = yMargin

        super().__init__(x, y)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

        self.render()

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

        self.render()

    def render(self):
        if self.parent != None:
            self.computedWidth = self.parent._width if self.width == None else self.width
            self.computedHeight = self.parent._height if self.height == None else self.height

            self.computedX = self.parent.computedX + self.x + self.xMargin
            self.computedY = self.parent.computedY + self.y + self.yMargin
            self.computedWidth -= 2 * self.xMargin
            self.computedHeight -= 2 * self.yMargin
        else:
            self.computedWidth = self.width
            self.computedHeight = self.height

        self._get()

        self._updateBuild()

        for child in self.children:
            child.render()

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        for child in self._children:
            child.parent = None

        self._children = value

        for child in self._children:
            child.parent = self

        self.render()

    def add(self, child):
        self._children.append(child)
        self._getChildGroup().append(child._get())

        child.parent = self

        self.render()

    def remove(self, child):
        self._children.remove(child)

        child.parent = None

        self.render()

    def _getChildGroup(self):
        return self._get()

    def _build(self):
        group = displayio.Group()

        group.hidden = True

        return group

    def _updateBuild(self):
        self._get().hidden = not self._visible

    def _addParent(self, parent):
        super()._addParent(parent)

        self.resize()

class Box(Container):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self.background = vx.display.WHITE
        self.border = vx.display.BLACK
        self.borderThickness = 2

        self._rect = None
        self._childGroup = None

        super().__init__(x, y, width, height, xMargin, yMargin)

    def _getChildGroup(self):
        if self._childGroup == None:
            self._get()

        return self._childGroup

    def _build(self):
        group = displayio.Group()

        group.hidden = True

        width = self.computedWidth
        height = self.computedHeight

        if not width: width = self.borderThickness
        if not height: height = self.borderThickness

        self._rect = Rect(
            self.computedX,
            self.computedY,
            width,
            height,
            fill = self.background,
            outline = self.border,
            stroke = self.borderThickness
        )

        group.append(self._rect)

        self._childGroup = displayio.Group()

        group.append(self._childGroup)

        return group

    def _updateBuild(self):
        self._get().hidden = not self._visible

        width = self.computedWidth
        height = self.computedHeight

        if not width: width = self.borderThickness
        if not height: height = self.borderThickness

        if (
            self.computedWidth != self._rect.width or
            self.computedHeight != self._rect.height
        ):
            del self._get()[0]

            self._rect = Rect(
                self.computedX,
                self.computedY,
                width,
                height,
                fill = self.background,
                outline = self.border,
                stroke = self.borderThickness
            )

            self._get().insert(0, self._rect)
        else:
            self._rect.x = self.computedX
            self._rect.y = self.computedY
            self._rect.fill = self.background
            self._rect.outline = self.border
            self._rect.stroke = self.borderThickness

class Button(Box):
    def __init__(self, x, y, text, width = 100, height = 32, xMargin = 0, yMargin = 0):
        self._text = text

        self._textElement = Text(4, 12, text)
        self._textElement.foreground = vx.display.BLACK

        super().__init__(x, y, width, height, xMargin, yMargin)

        self._focusable = True

        self.add(self._textElement)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

        self.render()

    def _updateBuild(self):
        if self.focused:
            self.background = vx.display.BLACK
            self._textElement.foreground = vx.display.WHITE
        else:
            self.background = vx.display.WHITE
            self._textElement.foreground = vx.display.BLACK

        super()._updateBuild()

        self._textElement.text = self.text
        self._textElement.x = int((self.computedWidth - self._textElement.computedWidth) / 2)

def _getFont(fontType):
    if fontType not in loadedFonts:
        loadedFonts[fontType] = bitmap_font.load_font("assets/%s.bdf" % (fontType))

    return loadedFonts[fontType]

rootContainer = Container(0, 0, vx.display.WIDTH, vx.display.HEIGHT)

vx.display.rootGroup.append(rootContainer._get())