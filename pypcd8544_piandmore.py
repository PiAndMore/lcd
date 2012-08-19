#!/usr/bin/python
# -*- coding: utf-8 -*-

# Library für PCD8544-kompatible Displays am MCP23016-Portexpander
# Portiert aus den C-Quelltexten der beiden Projekte
#  https://github.com/adafruit/Adafruit-PCD8544-Nokia-5110-LCD-library
#  https://github.com/adafruit/Adafruit-GFX-Library

# Konfiguration der Pins
# (vgl. LCD-Aufdruck und Pinbelegung des MCP23016)
SCLK = 4
DIN = 5
DC = 6
RST = 7
LED = 4
# 0x00 für Pins 0.0-0.7, 0x01 für Pins 1.0-1.7
PORT = 0x00

# 1/0 Vertauschen um das Display zu invertieren
BLACK = 1
WHITE = 0

LCDWIDTH = 84
LCDHEIGHT = 48

import smbus
from time import sleep
from grafix import *

# Beispielbild (von Sparkfun) für das Display
# Eigene Grafiken erzeugen:
#  http://www.sparkfun.com/tutorials/300 (Abschnitt "Displaying Bitmap Images")
LOGO = [
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xC0, 0xE0, 0xF0, 0xF8, 0xFC, 0xFC, 0xFE, 0xFF, 0xFC, 0xE0,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8,
0xF8, 0xF0, 0xF0, 0xE0, 0xE0, 0xC0, 0x80, 0xC0, 0xFC, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x3F, 0x7F,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0F, 0x1F, 0x3F, 0x7F, 0xFF, 0xFF,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xE7, 0xC7, 0xC7, 0x87, 0x8F, 0x9F, 0x9F, 0xFF, 0xFF, 0xFF,
0xC1, 0xC0, 0xE0, 0xFC, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFC, 0xFC, 0xFC, 0xFC, 0xFE, 0xFE, 0xFE,
0xFC, 0xFC, 0xF8, 0xF8, 0xF0, 0xE0, 0xC0, 0xC0, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x80, 0xC0, 0xE0, 0xF1, 0xFB, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x1F, 0x0F, 0x0F, 0x87,
0xE7, 0xFF, 0xFF, 0xFF, 0x1F, 0x1F, 0x3F, 0xF9, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xF8, 0xFD, 0xFF,
0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x3F, 0x0F, 0x07, 0x01, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0xF0, 0xFE, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFE,
0x7E, 0x3F, 0x3F, 0x0F, 0x1F, 0xFF, 0xFF, 0xFF, 0xFC, 0xF0, 0xE0, 0xF1, 0xFF, 0xFF, 0xFF, 0xFF,
0xFF, 0xFC, 0xF0, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x01,
0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x0F, 0x1F, 0x3F, 0x7F, 0x7F,
0xFF, 0xFF, 0xFF, 0xFF, 0x7F, 0x7F, 0x1F, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
]

xUpdateMin, xUpdateMax, yUpdateMin, yUpdateMax = 0, 0, 0, 0


bus = smbus.SMBus(0)
status = 0


def output(pin, value):
  global status
  if value:
    status |= (1 << pin)
  else:
    status = (status & ~(1<<pin))
  bus.write_byte_data(0x20,PORT,status)

def updateBoundingBox(xmin, ymin, xmax, ymax):
  global xUpdateMin, xUpdateMax, yUpdateMin, yUpdateMax
  if xmin < xUpdateMin: xUpdateMin = xmin
  if xmax > xUpdateMax: xUpdateMax = xmax
  if ymin < yUpdateMin: yUpdateMin = ymin
  if ymax > yUpdateMax: yUpdateMax = ymax


MEMORY = [0x00 for x in xrange((LCDWIDTH*LCDHEIGHT)/8)]

PCD8544_POWERDOWN = 0x04
PCD8544_ENTRYMODE = 0x02
PCD8544_EXTENDEDINSTRUCTION = 0x01

PCD8544_DISPLAYBLANK = 0x0
PCD8544_DISPLAYNORMAL = 0x4
PCD8544_DISPLAYALLON = 0x1
PCD8544_DISPLAYINVERTED = 0x5

# H = 0
PCD8544_FUNCTIONSET = 0x20
PCD8544_DISPLAYCONTROL = 0x08
PCD8544_SETYADDR = 0x40
PCD8544_SETXADDR = 0x80

# H = 1
PCD8544_SETTEMP = 0x04
PCD8544_SETBIAS = 0x10
PCD8544_SETVOP = 0x80

def _BV(i):
    return 1 << i

def switchBacklight(status):
  print "Backlight is now %s" % ("on" if status else "off")
  output(LED, status)

def drawPixel(x, y, color):
  if (x < 0) or (x >= LCDWIDTH) or (y < 0) or (y >= LCDHEIGHT):
    return

  # x is which column
  if color:
    MEMORY[x+ (y/8)*LCDWIDTH] |= _BV(y%8)
  else:
    MEMORY[x+ (y/8)*LCDWIDTH] &= ~_BV(y%8)

  updateBoundingBox(x,y,x,y)


# the most basic function, get a single pixel
def getPixel(x, y):
  if ((x < 0) or (x >= LCDWIDTH) or (y < 0) or (y >= LCDHEIGHT)):
    return 0

  return (MEMORY[x+ (y/8)*LCDWIDTH] >> (7-(y%8))) & 0x1


def setup():
  # set pin directions
  bus.write_byte_data(0x20,0x06,0x00)
  bus.write_byte_data(0x20,0x07,0x00)  

def begin(contrast, showLogo = True):
  init(LCDWIDTH, LCDHEIGHT, drawPixel) # Initialize grafix
  setup()
  # toggle RST low to reset
  output(RST, False)
  sleep(0.100)
  output(RST, True)

  # get into the EXTENDED mode!
  command(PCD8544_FUNCTIONSET | PCD8544_EXTENDEDINSTRUCTION )

  # LCD bias select (4 is optimal?)
  command(PCD8544_SETBIAS | 0x4)

  # set VOP
  if contrast > 0x7f:
    contrast = 0x7f

  command( PCD8544_SETVOP | contrast) # Experimentally determined


  # normal mode
  command(PCD8544_FUNCTIONSET)

  # Set display to Normal
  command(PCD8544_DISPLAYCONTROL | PCD8544_DISPLAYNORMAL)

  # initial display line
  # set page address
  # set column address
  # write display data
  # set up a bounding box for screen updates
  if showLogo:
    for x in xrange(len(MEMORY)):
      MEMORY[x] = LOGO[x]
    updateBoundingBox(0, 0, LCDWIDTH-1, LCDHEIGHT-1)
    # Push out MEMORY to the Display (will show the AFI logo)
    display()
  else: 
    # This only frees the memory.
    clearDisplay()
    pass


def slowSPIwrite(c):
  # data = DIN
  # clock = SCLK
  # MSB first
  # value = c
  for i in xrange(8):
    output(DIN, (c & (1 << (7-i))) > 0)
    output(SCLK, True)
    # Add delay here?
    output(SCLK, False)

def fastSPIwrite(c):
  slowSPIwrite(c)        

def command(c):
  output(DC, False)
  fastSPIwrite(c)

def data(c):
  output(DC, True)
  fastSPIwrite(c)

def setContrast(val): 
  if val > 0x7f:
    val = 0x7f

  command(PCD8544_FUNCTIONSET | PCD8544_EXTENDEDINSTRUCTION )
  command( PCD8544_SETVOP | val)
  command(PCD8544_FUNCTIONSET)

def display():
  global xUpdateMin, xUpdateMax, yUpdateMin, yUpdateMax
  col, maxcol, p = 0, 0, 0
  
  for p in xrange(6):
    if yUpdateMin >= ((p+1)*8):
      continue   # nope, skip it!
      
    if yUpdateMax < p*8:
      break

    command(PCD8544_SETYADDR | p)

    col = xUpdateMin
    maxcol = xUpdateMax

    command(PCD8544_SETXADDR | col)

    output(DC, True)
    for col in xrange(col, maxcol + 1):
      fastSPIwrite(MEMORY[(LCDWIDTH*p)+col])

  command(PCD8544_SETYADDR)  # no idea why this is necessary but it is to finish the last byte?
  xUpdateMin = LCDWIDTH - 1
  xUpdateMax = 0
  yUpdateMin = LCDHEIGHT-1
  yUpdateMax = 0

# clear everything
def clearDisplay():
  for x in xrange(len(MEMORY)):
    MEMORY[x] = 0x0
  updateBoundingBox(0, 0, LCDWIDTH-1, LCDHEIGHT-1)
  cursor_y = cursor_x = 0

if __name__ == "__main__":
  print "Please run pypcd-demo.py"

