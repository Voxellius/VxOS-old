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

def _updateBuildProfiler(element):
    pass # print(element)

class Element:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._visible = True
        self._focusable = False
        self._focused = False
        self._eventListeners = []

        self.containedX = 0
        self.containedY = 0

        self.parent = None
        self._cachedBuild = None
        self._holdingRender = False

        self.on(KeyPressEvent, self._checkFocusMove)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

        self.render(False)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

        self.render(False)

    @property
    def computedX(self):
        if self.parent == None:
            return self.containedX

        return self.parent.computedX + self.containedX

    @property
    def computedY(self):
        if self.parent == None:
            return self.containedY

        return self.parent.computedY + self.containedY

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

        self._triggerEvent(FocusEvent(self))

        if self.parent != None:
            self.parent._triggerEvent(ChildFocusEvent(self))

    def render(self, renderChildren = True):
        if self._holdingRender:
            return

        if self.parent != None:
            self.containedX = self._x
            self.containedY = self._y

        self._get()

        self._updateBuild()

    def holdRender(self):
        self._holdingRender = True

    def releaseRender(self, renderChildren = True):
        self._holdingRender = False

        self.render(renderChildren)

    def on(self, eventType, callback):
        self._eventListeners.append(EventListener(eventType, callback))

    def align(self, xAlignment = alignments.MIDDLE, yAlignment = alignments.MIDDLE):
        if xAlignment == alignments.MIDDLE:
            self.x = (self.parent.computedWidth - self.computedWidth) // 2

        if xAlignment == alignments.END:
            self.x = self.parent.computedWidth - self.computedWidth - self.computedX

        if yAlignment == alignments.MIDDLE:
            self.y = (self.parent.computedHeight - self.computedHeight) // 2

        if yAlignment == alignments.END:
            self.y = self.parent.computedHeight - self.computedHeight - self.computedY

    def place(self, element, side = sides.BELOW, gap = 0):
        if side == sides.BEFORE:
            self.x = element.computedX - element.parent.computedX - gap - self.computedWidth

        if side == sides.AFTER:
            self.x = element.computedX - element.parent.computedX + element.computedWidth + gap

        if side == sides.ABOVE:
            self.y = element.computedY - element.parent.computedY - gap - self.computedHeight

        if side == sides.BELOW:
            self.y = element.computedY - element.parent.computedY + element.computedHeight + gap

    def _get(self, rebuild = False):
        if rebuild or self._cachedBuild == None:
            self._cachedBuild = self._build()

        return self._cachedBuild

    def _build(self):
        group = displayio.Group()

        group.hidden = True

        return group

    def _updateBuild(self):
        _updateBuildProfiler(self)

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

    def _checkFocusMove(self, event):
        if event.isAnyKeys(["up", "down", "left", "right"]) and not event.hasKey("symbol") and self.focused:
            focusOrder = getVerticalFocusOrder() if event.isAnyKeys(["up", "down"]) else getFocusOrder()
            focusIndex = 0

            for i in range(0, len(focusOrder)):
                if focusOrder[i].focused:
                    focusIndex = i

            if len(focusOrder) > 0:
                if event.isKey("up") or event.isKey("left"):
                    focusOrder[focusIndex - 1].focus()

                if event.isKey("down") or event.isKey("right"):
                    focusOrder[(focusIndex + 1) % len(focusOrder)].focus()

class Text(Element):
    def __init__(self, x, y, text, font = fonts.SANS_REGULAR_16):
        self._cachedBuild = None
        self._holdingRender = False
        self._boundingBoxValid = False

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
            self._boundingBoxValid = False

            self.render()

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value
        self._boundingBoxValid = False

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
        if not self._boundingBoxValid:
            self.render()

            self._boundingBoxValid = True

        return self._get().bounding_box[0] + self._get().bounding_box[2]

    @property
    def computedHeight(self):
        if not self._boundingBoxValid:
            self.render()

            self._boundingBoxValid = True

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
            x = self.containedX,
            y = self.containedY + 5,
            scale = self._font[1],
            anchor_point = (0, 0),
            color = self.foreground
        )

        label.hidden = True

        return label

    def _updateBuild(self):
        _updateBuildProfiler(self)

        label = self._get()

        if label.font != _getFont(self._font[0]) or label.text != self.text:
            label.font = _getFont(self._font[0])
            label.text = self.text

        label.x = self.containedX
        label.y = self.containedY + 5
        label.scale = self._font[1]
        label.color = self.foreground
        label.hidden = not self._visible

class Image(Element):
    def __init__(self, x, y, path):
        self._cachedBuild = None
        self._holdingRender = False

        self.parent = None

        self._path = path
        self._bitmap = None

        super().__init__(x, y)

    @property
    def path(self):
        return self._path

    @property
    def computedWidth(self):
        if self._bitmap == None:
            self.render()

        return self._bitmap.width

    @property
    def computedHeight(self):
        if self._bitmap == None:
            self.render()

        return self._bitmap.height

    def _build(self):
        self._bitmap = displayio.OnDiskBitmap(self._path)

        image = displayio.TileGrid(
            bitmap = self._bitmap,
            pixel_shader = self._bitmap.pixel_shader,
            x = self.computedX,
            y = self.computedY
        )

        return image

    def _updateBuild(self):
        _updateBuildProfiler(self)

        self._get().x = self.containedX
        self._get().y = self.containedY

class Container(Element):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self._cachedBuild = None
        self._holdingRender = False

        self.parent = None

        self._children = []

        self.containedX = 0
        self.containedY = 0

        self._width = width
        self._height = height
        self._visible = True
        self._focused = False

        super().__init__(x, y)

        self.xMargin = xMargin
        self.yMargin = yMargin

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

    @property
    def computedWidth(self):
        if self.parent == None:
            return self.width

        return (self.parent._width if self.width == None else self.width) - (2 * self.xMargin)

    @property
    def computedHeight(self):
        if self.parent == None:
            return self.height

        return (self.parent._height if self.height == None else self.height) - (2 * self.yMargin)

    @property
    def contentsWidth(self):
        highestWidth = 0

        for child in self.children:
            width = child.x + child.computedWidth

            if width > highestWidth:
                highestWidth = width

        return highestWidth

    @property
    def contentsHeight(self):
        highestHeight = 0

        for child in self.children:
            height = child.y + child.computedHeight

            if height > highestHeight:
                highestHeight = height

        return highestHeight

    def render(self, renderChildren = True):
        if self._holdingRender:
            return

        if self.parent != None:
            self.containedX = self.x + self.xMargin
            self.containedY = self.y + self.yMargin

        self._get()

        self._updateBuild()

        if renderChildren:
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

    def add(self, child, render = True):
        self._children.append(child)
        self._getChildGroup().append(child._get())

        child.parent = self

        if render:
            child.render()

    def remove(self, child):
        self._children.remove(child)
        self._getChildGroup().remove(child._get())

        child.parent = None

    def _getChildGroup(self):
        return self._get()

    def _build(self):
        group = displayio.Group()

        group.hidden = True

        return group

    def _updateBuild(self):
        _updateBuildProfiler(self)

        self._get().hidden = not self._visible
        self._get().x = self.containedX
        self._get().y = self.containedY

    def _addParent(self, parent):
        super()._addParent(parent)

        self.resize()

class Screen(Container):
    def __init__(self):
        super().__init__(0, 0, vx.display.WIDTH, vx.display.HEIGHT)

        self.visible = False
        self.name = ""
        self.showStatusBar = True

class ScrollableScreen(Screen):
    def __init__(self):
        self.contents = Container(0, 0)
        self.horizontalScrollBar = HorizontalScrollBar(0, 0, 12, 12)
        self.verticalScrollBar = VerticalScrollBar(0, 0, 12, 12)

        self.scrollBarCorner = Box(0, 0, 12, 12)
        self.scrollBarCorner.border = vx.display.WHITE

        self._shouldUpdateFocusPosition = False

        super().__init__()

        self.add(self.contents, False)
        self.add(self.horizontalScrollBar, False)
        self.add(self.verticalScrollBar, False)
        self.add(self.scrollBarCorner, False)

        self.on(KeyPressEvent, self._checkManualScroll)
        self.on(ChildFocusEvent, self._checkAutoScroll)

    @property
    def scrollX(self):
        return -self.contents.x

    def _setScrollX(self, value):
        if value < 0:
            value = 0

        maxX = self.contents.contentsWidth - (self.computedWidth - self.verticalScrollBar.computedWidth)

        if value > maxX:
            value = max(maxX, 0)

        self.contents.x = -value

    def _setScrollY(self, value):
        if value < 0:
            value = 0

        maxY = self.contents.contentsHeight - (self.computedHeight - self.horizontalScrollBar.computedHeight)

        if value > maxY:
            value = max(maxY, 0)

        self.contents.y = -value

    @scrollX.setter
    def scrollX(self, value):
        self._setScrollX(value)
        self._updateBuild()

    @property
    def scrollY(self):
        return -self.contents.y

    @scrollY.setter
    def scrollY(self, value):
        self._setScrollY(value)
        self._updateBuild()

    def scrollTo(self, element):
        targetX = element.computedX - element.xMargin - self.contents.computedX
        targetY = element.computedY - element.yMargin - self.contents.computedY

        if self.scrollX + self.contents.computedWidth < targetX + element.computedWidth:
            self._setScrollX(targetX - self.contents.computedWidth + element.computedWidth)
        elif self.scrollX > targetX:
            self._setScrollX(targetX)

        if self.scrollY + self.contents.computedHeight < targetY + element.computedHeight:
            self._setScrollY(targetY - self.contents.computedHeight + element.computedHeight + self.horizontalScrollBar.computedHeight)
        elif self.scrollY > targetY:
            self._setScrollY(targetY)

        vx.display.display.refresh()
        vx.display.display.refresh()

        self._updateBuild()

    def update(self):
        self.render(False)

    def updateFocusPosition(self):
        if not self._shouldUpdateFocusPosition:
            return

        focusedElements = getElements(lambda element: element.focused)

        if len(focusedElements) > 0:
            vx.display.display.refresh()
            vx.display.display.refresh()

            self.scrollTo(focusedElements[0])

        self._shouldUpdateFocusPosition = False

    def _updateBuild(self):
        super()._updateBuild()

        self.contents.holdRender()
        self.horizontalScrollBar.holdRender()
        self.verticalScrollBar.holdRender()
        self.scrollBarCorner.holdRender()

        if self.parent != None:
            self.horizontalScrollBar.y = self.computedHeight - 12
            self.horizontalScrollBar.width = self.computedWidth
            self.horizontalScrollBar.height = 12

            self.verticalScrollBar.x = self.computedWidth - 12
            self.verticalScrollBar.width = 12
            self.verticalScrollBar.height = self.computedHeight

            viewportWidth = self.computedWidth - self.verticalScrollBar.computedWidth
            viewportHeight = self.computedHeight - self.horizontalScrollBar.computedHeight

            if self.contents.width != viewportWidth:
                self.contents.width = viewportWidth

            contentsWidth = self.contents.contentsWidth
            contentsHeight = self.contents.contentsHeight

            self.scrollBarCorner.visible = False

            if contentsWidth > viewportWidth:
                self.horizontalScrollBar.scrollPosition = clamp(-self.contents.x / (contentsWidth - viewportWidth))
                self.horizontalScrollBar.viewportRatio = clamp(viewportWidth / contentsWidth)
                self.horizontalScrollBar.visible = True
            else:
                self.horizontalScrollBar.visible = False

            if contentsHeight > viewportHeight:
                self.verticalScrollBar.scrollPosition = clamp(-self.contents.y / (contentsHeight - viewportHeight))
                self.verticalScrollBar.viewportRatio = clamp(viewportHeight / contentsHeight)
                self.verticalScrollBar.visible = True

                if self.horizontalScrollBar.visible:
                    self.horizontalScrollBar.width = self.computedWidth - self.verticalScrollBar.computedWidth
                    self.verticalScrollBar.height = self.computedHeight - self.horizontalScrollBar.computedHeight

                    self.scrollBarCorner.x = self.computedWidth - self.verticalScrollBar.computedWidth
                    self.scrollBarCorner.y = self.computedHeight - self.horizontalScrollBar.computedHeight

                    self.scrollBarCorner.visible = True
            else:
                self.verticalScrollBar.visible = False

        self.contents.releaseRender(False)
        self.horizontalScrollBar.releaseRender()
        self.verticalScrollBar.releaseRender()
        self.scrollBarCorner.releaseRender()

    def _checkManualScroll(self, event):
        if event.isAnyKeys(["up", "down", "left", "right"]) and event.hasKey("symbol"):
            if event.hasKey("shift"):
                if event.isKey("up"):
                    self.scrollY = 0

                if event.isKey("down"):
                    self.scrollY = self.contents.computedHeight

                if event.isKey("left"):
                    self.scrollX = 0

                if event.isKey("right"):
                    self.scrollX = self.contents.computedWidth
            else:
                if event.isKey("up"):
                    self.scrollY -= 16

                if event.isKey("down"):
                    self.scrollY += 16

                if event.isKey("left"):
                    self.scrollX -= 16

                if event.isKey("right"):
                    self.scrollX += 16

    def _checkAutoScroll(self, event):
        self._shouldUpdateFocusPosition = True

class Box(Container):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self.background = vx.display.WHITE
        self.border = vx.display.BLACK
        self.borderThickness = 2

        self._rect = None
        self._childGroup = None
        self._lastBorderThickness = 2

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
            0,
            0,
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
            self.computedHeight != self._rect.height or
            self.borderThickness != self._lastBorderThickness
        ):
            del self._get()[0]

            self._rect = Rect(
                0,
                0,
                width,
                height,
                fill = self.background,
                outline = self.border,
                stroke = self.borderThickness
            )

            self._get().insert(0, self._rect)

            self._lastBorderThickness = self.borderThickness
        else:
            self._rect.fill = self.background
            self._rect.outline = self.border
            self._rect.stroke = self.borderThickness

        super()._updateBuild()

class FocusableBox(Box):
    def __init__(self, x, y, width = 128, height = 32, xMargin = 0, yMargin = 0):
        super().__init__(x, y, width, height, xMargin, yMargin)

        self._focusable = True

    def _updateBuild(self):
        if self.focused:
            self.background = vx.display.BLACK
        else:
            self.background = vx.display.WHITE

        super()._updateBuild()

class Button(FocusableBox):
    def __init__(self, x, y, text, width = 128, height = 32, xMargin = 0, yMargin = 0):
        self._text = text

        self._textElement = Text(4, 12, text)
        self._textElement._foreground = vx.display.BLACK

        super().__init__(x, y, width, height, xMargin, yMargin)

        self.add(self._textElement, False)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

        self.render()

    def _updateBuild(self):
        super()._updateBuild()

        self._textElement.render() # This is so we can find the computed width for centering the text
        self._textElement.holdRender()

        if self.focused:
            self._textElement.foreground = vx.display.WHITE
        else:
            self._textElement.foreground = vx.display.BLACK

        if self.parent != None:
            self._textElement.text = self.text

            self._textElement.align(alignments.MIDDLE, alignments.MIDDLE)

        self._textElement.releaseRender()

class ScrollBar(Box):
    def __init__(self, x, y, width = None, height = None, xMargin = 0, yMargin = 0):
        self._indicatorElement = Box(0, 0, 12, 12, 2, 2)
        self._indicatorElement.background = vx.display.BLACK
        self._indicatorElement.borderThickness = 0

        self._scrollPosition = 0
        self._viewportRatio = 1

        super().__init__(x, y, width, height, xMargin, yMargin)

        self.background = vx.display.WHITE
        self.borderThickness = 0

        self.add(self._indicatorElement, False)

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
            fullWidth = self.computedWidth - self._indicatorElement.xMargin
            indicatorWidth = max(self.viewportRatio * fullWidth, 16)

            self._indicatorElement.x = round((fullWidth - indicatorWidth) * self.scrollPosition)
            self._indicatorElement.width = round(indicatorWidth)

class VerticalScrollBar(ScrollBar):
    def _updateBuild(self):
        super()._updateBuild()

        if self.parent != None:
            fullHeight = self.computedHeight - self._indicatorElement.yMargin
            indicatorHeight = max(self.viewportRatio * fullHeight, 16)

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
    def __init__(self, target, key = None, allKeys = None):
        self.key = key
        self.allKeys = allKeys

        super().__init__(target)

    def isKey(self, keyName):
        return self.key.name == keyName

    def isAnyKeys(self, keyNames):
        for keyName in keyNames:
            if keyName == self.key.name:
                return True

        return False

    def hasKey(self, keyName):
        for key in self.allKeys:
            if key.name == keyName:
                return True

        return False

class KeyPressEvent(KeyboardEvent): pass
class KeyReleaseEvent(KeyboardEvent): pass

class FocusEvent(Event):
    def __init__(self, target):
        super().__init__(target)

        self.shouldPropagate = False

class ChildFocusEvent(Event): pass

class EventListener:
    def __init__(self, eventType, callback):
        self.eventType = eventType
        self.callback = callback

rootContainer = Container(0, 0, vx.display.WIDTH, vx.display.HEIGHT)
screenContainer = Container(0, 0)
statusBar = None

rootContainer.add(screenContainer)
rootContainer.render()

def _getFont(fontType):
    if fontType not in loadedFonts:
        loadedFonts[fontType] = bitmap_font.load_font("assets/{}.bdf".format(fontType))

        loadedFonts[fontType].load_glyphs(b"abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 ")

    return loadedFonts[fontType]

def clamp(value, minValue = 0, maxValue = 1):
    return min(max(value, minValue), maxValue)

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

def getVerticalFocusOrder():
    focusedElements = getElements(lambda element: element.focused)
    focusedElement = None

    if len(focusedElements) > 0:
        focusedElement = focusedElements[0]

    focusableElements = getElements(lambda element: element.focusable)
    verticalElements = []

    if focusedElement != None:
        for element in focusableElements:
            if element.computedX + element.computedWidth <= focusedElement.computedX:
                continue

            if element.computedX >= focusedElement.computedX + focusedElement.computedWidth:
                continue

            verticalElements.append(element)

        verticalElements.sort(key = lambda element: element.computedY + (element.computedX - focusedElement.computedX))
    else:
        verticalElements = focusableElements

        verticalElements.sort(key = lambda element: element.computedY)

    return verticalElements

def getScreens():
    return getElements(lambda element: isinstance(element, Screen))

def getCurrentScreen():
    for screen in getScreens():
        if screen.visible:
            return screen

    return None

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
            target._triggerEvent(KeyPressEvent(target, key, vx.keyboard.heldKeys))

        for key in vx.keyboard.releasedKeys:
            target._triggerEvent(KeyReleaseEvent(target, key, vx.keyboard.heldKeys))

vx.display.rootGroup.append(rootContainer._get())