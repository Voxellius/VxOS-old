# VxOS
# 
# Copyright (C) Voxellius Systems. All Rights Reserved.
# Please refer to LICENCE.md for licensing information.
# 
# https://voxellius.com

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect

import vx.platform
import vx.display
import vx.keyboard

if vx.platform.IS_REAL_HARDWARE:
    from adafruit_display_text.bitmap_label import Label
else:
    from adafruit_display_text.label import Label

class fonts:
    SANS_REGULAR_16 = ("titilliumweb-regular-16", 1, 20)
    SANS_REGULAR_32 = ("titilliumweb-regular-16", 2, 40)
    SANS_REGULAR_64 = ("titilliumweb-regular-16", 4, 80)
    SANS_NUMERALS_64 = ("titilliumweb-numerals-64", 1, 80)

loadedFonts = {}

class alignments:
    START = 0
    MIDDLE = 1
    END = 2

class sides:
    ABOVE = 0
    BELOW = 1
    BEFORE = 2
    AFTER = 3

class Element:
    def __init__(self, x, y):
        self._x = 0
        self._y = 0
        self._visible = True
        self._focusable = False
        self._focused = False
        self._eventListeners = []

        self.computedX = 0
        self.computedY = 0

        self.x = x
        self.y = y

        self.parent = None
        self._cachedBuild = None

        self.on(KeyPressEvent, self._onKeyPress)

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
    def focusable(self):
        return self._focusable

    @property
    def focused(self):
        return self._focused

    def focus(self):
        for element in getElements(lambda element: element.focused):
            element._focused = False

            element.render()

        self._focused = True

        self.render()

    def render(self):
        if self.parent != None:
            self.computedX = self.parent.computedX + self._x
            self.computedY = self.parent.computedY + self._y

        self._get()

        self._updateBuild()

    def on(self, eventType, callback):
        self._eventListeners.append(EventListener(eventType, callback))

    def align(self, xAlignment = alignments.MIDDLE, yAlignment = alignments.MIDDLE):
        if xAlignment == alignments.MIDDLE:
            self.x = int((self.parent.computedWidth - self.computedWidth) / 2)

        if xAlignment == alignments.END:
            self.x = self.parent.computedWidth - self.computedWidth - self.computedX

        if yAlignment == alignments.MIDDLE:
            self.y = int((self.parent.computedHeight - self.computedHeight) / 2)

        if yAlignment == alignments.END:
            self.y = self.parent.computedHeight - self.computedHeight - self.computedY

    def place(self, element, side = sides.BELOW, gap = 0):
        if side == sides.BEFORE:
            self.x = element.computedX - gap - self.computedWidth

        if side == sides.AFTER:
            self.x = element.computedX + element.computedWidth + gap

        if side == sides.ABOVE:
            self.y = element.computedY - gap - self.computedHeight

        if side == sides.BELOW:
            self.y = element.computedY + element.computedHeight + gap

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

    def _triggerEvent(self, event):
        for eventListener in reversed(self._eventListeners):
            if not event.shouldContinue:
                break

            if not isinstance(event, eventListener.eventType):
                continue

            eventListener.callback(event)

        event.shouldContinue = True

        if event.shouldPropagate and self.parent != None:
            self.parent._triggerEvent(event)

    def _onKeyPress(self, event):
        if (event.key.name == "left" or event.key.name == "right") and self.focused:
            focusOrder = getFocusOrder()
            focusIndex = 0

            for i in range(0, len(focusOrder)):
                if focusOrder[i].focused:
                    focusIndex = i

            if event.key.name == "left":
                focusOrder[focusIndex - 1].focus()

            if event.key.name == "right":
                focusOrder[(focusIndex + 1) % len(focusOrder)].focus()

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
        if value != self._text:
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

        return self._get().bounding_box[0] + self._get().bounding_box[2]

    @property
    def computedHeight(self):
        self.render()

        return self._font[2]

    def cut(self, width = None):
        if width == None:
            width = self.parent.computedWidth - (2 * self.xMargin)

        cutText = self._text

        while self.computedWidth > width and cutText != "":
            cutText = cutText[:-1]

            self._text = cutText + "..."

            self.render()

        if self.computedWidth > width:
            self._text = ""

            self.render()

    def _build(self):
        label = Label(
            font = _getFont(self._font[0]),
            text = "",
            x = self.computedX,
            y = self.computedY + 5,
            scale = self._font[1],
            anchor_point = (0, 0),
            color = self.foreground
        )

        label.hidden = True

        return label

    def _updateBuild(self):
        label = self._get()

        if label.font != _getFont(self._font[0]) or label.text != self.text:
            label.font = _getFont(self._font[0])
            label.text = self.text

        label.x = self.computedX
        label.y = self.computedY + 5
        label.scale = self._font[1]
        label.color = self.foreground
        label.hidden = not self._visible

class Image(Element):
    def __init__(self, x, y, path):
        self._cachedBuild = None

        self.parent = None

        self._path = path
        self._bitmap = None

        super().__init__(x, y)

    @property
    def path(self):
        return self._path

    @property
    def computedWidth(self):
        self.render()

        return self._bitmap.width

    @property
    def computedHeight(self):
        self.render()

        return self._bitmap.height

    def _build(self):
        self._bitmap = displayio.OnDiskBitmap(self._path)

        image = displayio.TileGrid(
            bitmap = self._bitmap,
            pixel_shader = displayio.ColorConverter(),
            x = self.computedX,
            y = self.computedY
        )

        return image

    def _updateBuild(self):
        self._get().x = self.computedX
        self._get().y = self.computedY

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

    def shrinkWidth(self):
        highestWidth = 0

        for child in self.children:
            width = child.y + child.computedWidth

            if width > highestWidth:
                highestWidth = width

        self.width = highestWidth

    def shrinkHeight(self):
        highestHeight = 0

        for child in self.children:
            height = child.y + child.computedHeight

            if height > highestHeight:
                highestHeight = height

        self.height = highestHeight

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
        self._getChildGroup().remove(child._get())

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

class Screen(Container):
    def __init__(self):
        super().__init__(0, 0, vx.display.WIDTH, vx.display.HEIGHT)

        self.visible = False
        self.showStatusBar = True

class ScrollableScreen(Screen):
    def __init__(self):
        self.contents = Container(0, 0)
        self.horizontalScrollBar = HorizontalScrollBar(0, 0, 16, 16)
        self.verticalScrollBar = VerticalScrollBar(0, 0, 16, 16)

        super().__init__()

        self.add(self.contents)
        self.add(self.horizontalScrollBar)
        self.add(self.verticalScrollBar)

    def _updateBuild(self):
        super()._updateBuild()

        if self.parent != None:
            self.horizontalScrollBar.y = self.computedHeight - 16
            self.horizontalScrollBar.width = self.computedWidth
            self.horizontalScrollBar.height = 16

            self.horizontalScrollBar.scrollPosition = 0.5
            self.horizontalScrollBar.viewportRatio = 0.3

            self.verticalScrollBar.x = self.computedWidth - 16
            self.verticalScrollBar.width = 16
            self.verticalScrollBar.height = self.computedHeight

            self.verticalScrollBar.scrollPosition = 0.5
            self.verticalScrollBar.viewportRatio = 0.3

        self.contents.shrinkWidth()
        self.contents.shrinkHeight()

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
        self._textElement.y = int((self.computedHeight - self._textElement.computedHeight) / 2)

class ScrollBar(Box):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self._indicatorElement = Box(0, 0, 16, 16, 2, 2)
        self._indicatorElement.background = vx.display.BLACK
        self._indicatorElement.borderThickness = 0

        self._scrollPosition = 0
        self._viewportRatio = 1

        super().__init__(x, y, width, height, xMargin, yMargin)

        self.background = vx.display.WHITE
        self.borderThickness = 0

        self.add(self._indicatorElement)

    @property
    def scrollPosition(self):
        return self._scrollPosition

    @scrollPosition.setter
    def scrollPosition(self, value):
        self._scrollPosition = value

        self.render()

    @property
    def viewportRatio(self):
        return self._viewportRatio

    @viewportRatio.setter
    def viewportRatio(self, value):
        self._viewportRatio = value

        self.render()

class HorizontalScrollBar(ScrollBar):
    def _updateBuild(self):
        super()._updateBuild()

        if self.parent != None:
            fullWidth = self.computedWidth - (2 * self._indicatorElement.xMargin)
            indicatorWidth = max(self.viewportRatio * fullWidth, 20)

            self._indicatorElement.x = round((fullWidth - indicatorWidth) * self.scrollPosition)
            self._indicatorElement.width = round(indicatorWidth)

class VerticalScrollBar(ScrollBar):
    def _updateBuild(self):
        super()._updateBuild()

        if self.parent != None:
            fullHeight = self.computedHeight - (2 * self._indicatorElement.yMargin)
            indicatorHeight = max(self.viewportRatio * fullHeight, 20)

            self._indicatorElement.y = round((fullHeight - indicatorHeight) * self.scrollPosition)
            self._indicatorElement.height = round(indicatorHeight)

class Event:
    def __init__(self, target):
        self.target = target
        self.shouldContinue = True
        self.shouldPropagate = True

    def cancel(self):
        self.shouldContinue = False

    def cancelPropagation(self):
        self.shouldPropagate = False

class KeyboardEvent(Event):
    def __init__(self, target, key = None):
        self.key = key

        super().__init__(target)

class KeyPressEvent(KeyboardEvent):
    pass

class KeyReleaseEvent(KeyboardEvent):
    pass

class EventListener:
    def __init__(self, eventType, callback):
        self.eventType = eventType
        self.callback = callback

rootContainer = Container(0, 0, vx.display.WIDTH, vx.display.HEIGHT)
screenContainer = Container(0, 0)
statusBar = None

rootContainer.add(screenContainer)

def _getFont(fontType):
    if fontType not in loadedFonts:
        loadedFonts[fontType] = bitmap_font.load_font("assets/{}.bdf".format(fontType))

        loadedFonts[fontType].load_glyphs(b"abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ")

    return loadedFonts[fontType]

def getElements(condition = lambda element: True, parentCondition = lambda element: element.visible, root = rootContainer):
    if not isinstance(root, Container):
        return []

    elements = []

    for element in root.children:
        if condition(element):
            elements.append(element)

        if parentCondition(element):
            elements += getElements(condition, parentCondition, element)

    return elements

def getFocusOrder():
    focusableElements = getElements(lambda element: element.focusable)

    focusableElements.sort(key = lambda element: (element.computedY * vx.display.WIDTH) + element.computedX)

    return focusableElements

def getScreens():
    return getElements(lambda element: isinstance(element, Screen))

def switchToScreen(screen):
    for otherScreen in getScreens():
        otherScreen.visible = False

    if statusBar != None:
        statusBar.visible = screen.showStatusBar

    if screen.showStatusBar and statusBar != None:
        screen.y = statusBar.y + statusBar.computedHeight
    else:
        screen.y = 0

    screen.height = vx.display.HEIGHT - screen.y

    screen.visible = True

def updateEvents():
    vx.keyboard.poll()

    focusedElements = getElements(lambda element: element.focused)

    if len(focusedElements) > 0:
        target = focusedElements[0]

        for key in vx.keyboard.pressedKeys:
            target._triggerEvent(KeyPressEvent(target, key))

        for key in vx.keyboard.releasedKeys:
            target._triggerEvent(KeyReleaseEvent(target, key))

vx.display.rootGroup.append(rootContainer._get())