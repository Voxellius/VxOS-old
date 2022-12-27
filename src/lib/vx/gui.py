# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import displayio
from adafruit_display_shapes.rect import Rect

import vx.display

class Element:
    def __init__(self, x, y):
        self._x = 0
        self._y = 0

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

    def render(self):
        if self.parent == None:
            return

        self._computedX = self.parent._computedX + self._x
        self._computedY = self.parent._computedY + self._y

    def _get(self, rebuild = False):
        if rebuild or self._cachedBuild == None:
            self._cachedBuild = self._build()

        return self._cachedBuild

    def _build(self):
        return displayio.Group()

    def _updateBuild(self):
        pass

    def _addParent(self, parent):
        self.parent = parent

class Container(Element):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self._cachedBuild = None

        self.parent = None

        self._children = []

        self._width = 0
        self._height = 0
        self._computedX = 0
        self._computedY = 0
        self._computedWidth = 0
        self._computedHeight = 0

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
        print(self, self.parent)
        if self.parent != None:
            self._computedWidth = self.parent._width if self.width == None else self.width
            self._computedHeight = self.parent._height if self.height == None else self.height

            self._computedX = self.parent._computedX + self.x + self.xMargin
            self._computedY = self.parent._computedY + self.y + self.yMargin
            self._computedWidth -= 2 * self.xMargin
            self._computedHeight -= 2 * self.yMargin
        else:
            self._computedWidth = self.width
            self._computedHeight = self.height

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
        return displayio.Group()

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

        width = self._computedWidth
        height = self._computedHeight

        if not width: width = self.borderThickness
        if not height: height = self.borderThickness

        print(width, height)

        self._rect = Rect(
            self._computedX,
            self._computedY,
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
        width = self._computedWidth
        height = self._computedHeight

        if not width: width = self.borderThickness
        if not height: height = self.borderThickness

        del self._get()[0]

        self._rect = Rect(
            self._computedX,
            self._computedY,
            width,
            height,
            fill = self.background,
            outline = self.border,
            stroke = self.borderThickness
        )

        self._get().append(self._rect)

        print("new", self._computedX, self._computedY, width, height)

rootContainer = Container(0, 0, vx.display.WIDTH, vx.display.HEIGHT)

vx.display.rootGroup.append(rootContainer._get())