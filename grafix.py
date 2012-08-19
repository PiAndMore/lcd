#!/usr/bin/python
# -*- coding: utf-8 -*-

# Grafiklibrary für PCD8544-kompatible Displays
# Portiert aus den C-Quelltexten des Projekts
#  https://github.com/adafruit/Adafruit-GFX-Library

from font import font

drawPixelFun = None

def init(w, h, drawPixel):
    global _width, WIDTH, _height, HEIGHT, drawPixelFun
    _width = w
    WIDTH = w
    _height = h
    HEIGHT = h
    drawPixelFun = drawPixel

rotation = 0x0
cursor_y = 0x0
cursor_x = 0x0
textsize = 0x1
textcolor = False
textbgcolor = True
wrap = True


# draw a circle outline

def drawCircle(
    x0,
    y0,
    r,
    color,
    ):
    f = 0x1 - r
    ddF_x = 0x1
    ddF_y = -0x2 * r
    x = 0x0
    y = r

    drawPixelFun(x0, y0 + r, color)
    drawPixelFun(x0, y0 - r, color)
    drawPixelFun(x0 + r, y0, color)
    drawPixelFun(x0 - r, y0, color)

    while x < y:
        if f >= 0x0:
            y -= 0x1
            ddF_y += 0x2
            f += ddF_y

        x += 0x1
        ddF_x += 0x2
        f += ddF_x

        drawPixelFun(x0 + x, y0 + y, color)
        drawPixelFun(x0 - x, y0 + y, color)
        drawPixelFun(x0 + x, y0 - y, color)
        drawPixelFun(x0 - x, y0 - y, color)
        drawPixelFun(x0 + y, y0 + x, color)
        drawPixelFun(x0 - y, y0 + x, color)
        drawPixelFun(x0 + y, y0 - x, color)
        drawPixelFun(x0 - y, y0 - x, color)


def drawCircleHelper(
    x0,
    y0,
    r,
    cornername,
    color,
    ):
    f = 0x1 - r
    ddF_x = 0x1
    ddF_y = -0x2 * r
    x = 0x0
    y = r

    while x < y:
        if f >= 0x0:
            y -= 0x1
            ddF_y += 0x2
            f += ddF_y

        x += 0x1
        ddF_x += 0x2
        f += ddF_x
        if cornername & 0x4:
            drawPixelFun(x0 + x, y0 + y, color)
            drawPixelFun(x0 + y, y0 + x, color)

        if cornername & 0x2:
            drawPixelFun(x0 + x, y0 - y, color)
            drawPixelFun(x0 + y, y0 - x, color)

        if cornername & 0x8:
            drawPixelFun(x0 - y, y0 + x, color)
            drawPixelFun(x0 - x, y0 + y, color)

        if cornername & 0x1:
            drawPixelFun(x0 - y, y0 - x, color)
            drawPixelFun(x0 - x, y0 - y, color)


def fillCircle(
    x0,
    y0,
    r,
    color,
    ):
    drawFastVLine(x0, y0 - r, 0x2 * r + 0x1, color)
    fillCircleHelper(
        x0,
        y0,
        r,
        3,
        0x0,
        color,
        )


# used to do circles and roundrects!

def fillCircleHelper(
    x0,
    y0,
    r,
    cornername,
    delta,
    color,
    ):

    f = 0x1 - r
    ddF_x = 0x1
    ddF_y = -0x2 * r
    x = 0x0
    y = r

    while x < y:
        if f >= 0x0:
            y -= 0x1
            ddF_y += 0x2
            f += ddF_y

        x += 0x1
        ddF_x += 0x2
        f += ddF_x

        if cornername & 0x1:
            drawFastVLine(x0 + x, y0 - y, 0x2 * y + 0x1 + delta, color)
            drawFastVLine(x0 + y, y0 - x, 0x2 * x + 0x1 + delta, color)

        if cornername & 0x2:
            drawFastVLine(x0 - x, y0 - y, 0x2 * y + 0x1 + delta, color)
            drawFastVLine(x0 - y, y0 - x, 0x2 * x + 0x1 + delta, color)


# bresenham's algorithm - thx wikpedia

def drawLine(
    x0,
    y0,
    x1,
    y1,
    color,
    ):

    steep = abs(y1 - y0) > abs(x1 - x0)
    if steep:
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    #(dx, dy)
    dx = x1 - x0
    dy = abs(y1 - y0)

    err = dx / 0x2
    ystep = 0

    if y0 < y1:
        ystep = 0x1
    else:
        ystep = -0x1

    while x0 <= x1:
        if steep:
            drawPixelFun(y0, x0, color)
        else:
            drawPixelFun(x0, y0, color)

        err -= dy
        if err < 0x0:
            y0 += ystep
            err += dx
        x0 += 0x1


# draw a rectangle

def drawRect(
    x,
    y,
    w,
    h,
    color,
    ):

    drawFastHLine(x, y, w, color)
    drawFastHLine(x, y + h - 0x1, w, color)
    drawFastVLine(x, y, h, color)
    drawFastVLine(x + w - 0x1, y, h, color)


def drawFastVLine(
    x,
    y,
    h,
    color,
    ):

  # stupidest version - update in subclasses if desired!

    drawLine(x, y, x, y + h - 0x1, color)


def drawFastHLine(
    x,
    y,
    w,
    color,
    ):

  # stupidest version - update in subclasses if desired!

    drawLine(x, y, x + w - 0x1, y, color)


def fillRect(
    x,
    y,
    w,
    h,
    color,
    ):

  # stupidest version - update in subclasses if desired!

    for i in xrange(x, x + w):
        drawFastVLine(i, y, h, color)


def fillScreen(color):
    fillRect(0x0, 0x0, _width, _height, color)


# draw a rounded rectangle!

def drawRoundRect(
    x,
    y,
    w,
    h,
    r,
    color,
    ):

  # smarter version

    drawFastHLine(x + r, y, w - 0x2 * r, color)  # Top
    drawFastHLine(x + r, y + h - 0x1, w - 0x2 * r, color)  # Bottom
    drawFastVLine(x, y + r, h - 0x2 * r, color)  # Left
    drawFastVLine(x + w - 0x1, y + r, h - 0x2 * r, color)  # Right

  # draw four corners

    drawCircleHelper(x + r, y + r, r, 0x1, color)
    drawCircleHelper(x + w - r - 0x1, y + r, r, 0x2, color)
    drawCircleHelper(x + w - r - 0x1, y + h - r - 0x1, r, 0x4, color)
    drawCircleHelper(x + r, y + h - r - 0x1, r, 0x8, color)


# fill a rounded rectangle!

def fillRoundRect(
    x,
    y,
    w,
    h,
    r,
    color,
    ):

  # smarter version

    fillRect(x + r, y, w - 0x2 * r, h, color)

  # draw four corners

    fillCircleHelper(
        x + w - r - 0x1,
        y + r,
        r,
        0x1,
        h - 0x2 * r - 0x1,
        color,
        )
    fillCircleHelper(
        x + r,
        y + r,
        r,
        0x2,
        h - 0x2 * r - 0x1,
        color,
        )


# draw a triangle!

def drawTriangle(
    x0,
    y0,
    x1,
    y1,
    x2,
    y2,
    color,
    ):

    drawLine(x0, y0, x1, y1, color)
    drawLine(x1, y1, x2, y2, color)
    drawLine(x2, y2, x0, y0, color)


# fill a triangle!

def fillTriangle(
    x0,
    y0,
    x1,
    y1,
    x2,
    y2,
    color,
    ):

    (a, b, y, last) = (0x0, 0x0, 0x0, 0x0)

  # Sort coordinates by Y order (y2 >= y1 >= y0)

    if y0 > y1:
        swap(y0, y1)
        swap(x0, x1)

    if y1 > y2:
        swap(y2, y1)
        swap(x2, x1)

    if y0 > y1:
        swap(y0, y1)
        swap(x0, x1)

    if y0 == y2:  # Handle awkward all-on-same-line case as its own thing
        a = b = x0
        if x1 < a:
            a = x1
        elif x1 > b:
            b = x1
        if x2 < a:
            a = x2
        elif x2 > b:
            b = x2
        drawFastHLine(a, y0, b - a + 0x1, color)
        return

        dx01 = (x1 - x0, )
        dy01 = (y1 - y0, )
        dx02 = (x2 - x0, )
        dy02 = (y2 - y0, )
        dx12 = (x2 - x1, )
        dy12 = (y2 - y1, )
        sa = (0x0, )
        sb = 0x0

  # For upper part of triangle, find scanline crossings for segments
  # 0-1 and 0-2.  If y1=y2 (flat-bottomed triangle), the scanline y1
  # is included here (and second loop will be skipped, avoiding a /0
  # error there), otherwise scanline y1 is skipped here and handled
  # in the second loop...which also avoids a /0 error here if y0=y1
  # (flat-topped triangle).

    if y1 == y2:
        last = y1  # Include y1 scanline
    else:
        last = y1 - 0x1  # Skip it

    for y in xrange(y0, last + 0x1):
        a = x0 + sa / dy01
        b = x0 + sb / dy02
        sa += dx01
        sb += dx02
        if a > b:
            swap(a, b)
        drawFastHLine(a, y, b - a + 0x1, color)

  # For lower part of triangle, find scanline crossings for segments
  # 0-2 and 1-2.  This loop is skipped if y1=y2.

    sa = dx12 * (y - y1)
    sb = dx02 * (y - y0)
    while y <= y2:
        a = x1 + sa / dy12
        b = x0 + sb / dy02
        sa += dx12
        sb += dx02
        if a > b:
            swap(a, b)
        drawFastHLine(a, y, b - a + 0x1, color)
        y += 0x1


def drawBitmap(
    x,
    y,
    bitmap,
    w,
    h,
    color,
    ):

    for j in xrange(0x0, h):
        for i in xrange(0x0, i < w):
            if pgm_read_byte(bitmap + i + j / 0x8 * w) & _BV(j % 0x8):
                drawPixelFun(x + i, y + j, color)


def writeChar(c):
    global cursor_x, cursor_y
    if c == '\n':
        cursor_y += textsize * 0x8
        cursor_x = 0x0
    elif c == '\r':

    # skip em

        pass
    else:
        drawChar(
            cursor_x,
            cursor_y,
            c,
            textcolor,
            textbgcolor,
            textsize,
            )
        cursor_x += textsize * 6
        if wrap and cursor_x > _width - textsize * 6:
            cursor_y += textsize * 0x8
            cursor_x = 0x0

    return 0x1

def write(s):
    for c in s:
        writeChar(c)

# draw a character

def drawChar(
    x,
    y,
    c,
    color,
    bg,
    size,
    ):

    if x >= _width \
       or y >= _height \
       or x + 5 * size - 0x1 < 0x0 \
       or y + 0x8 * size - 0x1 < 0x0:
        print "DEBUG: Skipping Character %s, size is %d, x is %d, y is %d, _width is %d, _height is %d" % (c, size, x, y, _width, _height)
        return

    for i in xrange(0x0, 6):
        line = 0x0
        if i == 5:
            line = 0x0
        else:
            line = font[ord(c) * 5 + i]#:ord(c) * 5 + i+4]
        for j in xrange(0x0, 0x8):
            if line & 0x1:
                if size == 0x1:  # default size
                    drawPixelFun(x + i, y + j, color)
                else:

                # big size

                    fillRect(x + i * size, y + j * size, size, size,
                             color)
            elif bg != color:

                if size == 0x1:  # default size
                    drawPixelFun(x + i, y + j, bg)
                else:

                # big size

                    fillRect(x + i * size, y + j * size, size, size, bg)

            line >>= 0x1

def setCursor(x, y):
    global cursor_x, cursor_y
    cursor_x = x
    cursor_y = y


def setTextSize(s):
    global textsize
    textsize = (s if s > 0x0 else 0x1)

def setTextColor(c, b):
    global textcolor, textbgcolor
    textcolor = c
    textbgcolor = b


def setTextWrap(w):
    global wrap
    wrap = w


def getRotation():
    global rotation
    rotation %= 0x4
    return rotation


def setRotation(x):
    global rotation
    x %= 0x4  # cant be higher than 3
    rotation = x
    if x == 0x0 or x == 0x2:
        _width = WIDTH
        _height = HEIGHT
    elif x == 0x1 or x == 3:
        _width = HEIGHT
        _height = WIDTH

# return the size of the display which depends on the rotation!

def width(void):
    return _width


def height(void):
    return _height


