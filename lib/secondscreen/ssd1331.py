import struct
import spidev
import sys
import time
import random
import RPi.GPIO as gpio

ascii = [
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ],
    [ 0x00, 0x00, 0x00, 0x00, 0x00 ], # sp
    [ 0x00, 0x00, 0x2f, 0x00, 0x00 ], # !
    [ 0x00, 0x07, 0x00, 0x07, 0x00 ], # "
    [ 0x14, 0x7f, 0x14, 0x7f, 0x14 ], # #
    [ 0x24, 0x2a, 0x7f, 0x2a, 0x12 ], # $
    [ 0x62, 0x64, 0x08, 0x13, 0x23 ], # %
    [ 0x36, 0x49, 0x55, 0x22, 0x50 ], # &
    [ 0x00, 0x05, 0x03, 0x00, 0x00 ], # ' 
    [ 0x00, 0x1c, 0x22, 0x41, 0x00 ], # (
    [ 0x00, 0x41, 0x22, 0x1c, 0x00 ], # )
    [ 0x14, 0x08, 0x3E, 0x08, 0x14 ], # *
    [ 0x08, 0x08, 0x3E, 0x08, 0x08 ], # +
    [ 0x00, 0x00, 0xA0, 0x60, 0x00 ], # , 
    [ 0x08, 0x08, 0x08, 0x08, 0x08 ], # - 
    [ 0x00, 0x60, 0x60, 0x00, 0x00 ], # . 
    [ 0x20, 0x10, 0x08, 0x04, 0x02 ], # /
    [ 0x3E, 0x51, 0x49, 0x45, 0x3E ], # 0
    [ 0x00, 0x42, 0x7F, 0x40, 0x00 ], # 1
    [ 0x42, 0x61, 0x51, 0x49, 0x46 ], # 2
    [ 0x21, 0x41, 0x45, 0x4B, 0x31 ], # 3
    [ 0x18, 0x14, 0x12, 0x7F, 0x10 ], # 4
    [ 0x27, 0x45, 0x45, 0x45, 0x39 ], # 5
    [ 0x3C, 0x4A, 0x49, 0x49, 0x30 ], # 6
    [ 0x01, 0x71, 0x09, 0x05, 0x03 ], # 7
    [ 0x36, 0x49, 0x49, 0x49, 0x36 ], # 8
    [ 0x06, 0x49, 0x49, 0x29, 0x1E ], # 9
    [ 0x00, 0x36, 0x36, 0x00, 0x00 ], # :
    [ 0x00, 0x56, 0x36, 0x00, 0x00 ], # ;
    [ 0x08, 0x14, 0x22, 0x41, 0x00 ], # <
    [ 0x14, 0x14, 0x14, 0x14, 0x14 ], # =
    [ 0x00, 0x41, 0x22, 0x14, 0x08 ], # >
    [ 0x02, 0x01, 0x51, 0x09, 0x06 ], # ?
    [ 0x32, 0x49, 0x59, 0x51, 0x3E ], # @
    [ 0x7C, 0x12, 0x11, 0x12, 0x7C ], # A
    [ 0x7F, 0x49, 0x49, 0x49, 0x36 ], # B
    [ 0x3E, 0x41, 0x41, 0x41, 0x22 ], # C
    [ 0x7F, 0x41, 0x41, 0x22, 0x1C ], # D
    [ 0x7F, 0x49, 0x49, 0x49, 0x41 ], # E
    [ 0x7F, 0x09, 0x09, 0x09, 0x01 ], # F
    [ 0x3E, 0x41, 0x49, 0x49, 0x7A ], # G
    [ 0x7F, 0x08, 0x08, 0x08, 0x7F ], # H
    [ 0x00, 0x41, 0x7F, 0x41, 0x00 ], # I
    [ 0x20, 0x40, 0x41, 0x3F, 0x01 ], # J
    [ 0x7F, 0x08, 0x14, 0x22, 0x41 ], # K
    [ 0x7F, 0x40, 0x40, 0x40, 0x40 ], # L
    [ 0x7F, 0x02, 0x0C, 0x02, 0x7F ], # M
    [ 0x7F, 0x04, 0x08, 0x10, 0x7F ], # N
    [ 0x3E, 0x41, 0x41, 0x41, 0x3E ], # O
    [ 0x7F, 0x09, 0x09, 0x09, 0x06 ], # P
    [ 0x3E, 0x41, 0x51, 0x21, 0x5E ], # Q
    [ 0x7F, 0x09, 0x19, 0x29, 0x46 ], # R
    [ 0x46, 0x49, 0x49, 0x49, 0x31 ], # S
    [ 0x01, 0x01, 0x7F, 0x01, 0x01 ], # T
    [ 0x3F, 0x40, 0x40, 0x40, 0x3F ], # U
    [ 0x1F, 0x20, 0x40, 0x20, 0x1F ], # V
    [ 0x3F, 0x40, 0x38, 0x40, 0x3F ], # W
    [ 0x63, 0x14, 0x08, 0x14, 0x63 ], # X
    [ 0x07, 0x08, 0x70, 0x08, 0x07 ], # Y
    [ 0x61, 0x51, 0x49, 0x45, 0x43 ], # Z
    [ 0x00, 0x7F, 0x41, 0x41, 0x00 ], # [
    [ 0x02, 0x04, 0x08, 0x10, 0x20 ], # \
    [ 0x00, 0x41, 0x41, 0x7F, 0x00 ], # ]
    [ 0x04, 0x02, 0x01, 0x02, 0x04 ], # ^
    [ 0x40, 0x40, 0x40, 0x40, 0x40 ], # _
    [ 0x00, 0x03, 0x02, 0x04, 0x00 ], # ' 
    [ 0x20, 0x54, 0x54, 0x54, 0x78 ], # a
    [ 0x7F, 0x48, 0x44, 0x44, 0x38 ], # b
    [ 0x38, 0x44, 0x44, 0x44, 0x20 ], # c
    [ 0x38, 0x44, 0x44, 0x48, 0x7F ], # d
    [ 0x38, 0x54, 0x54, 0x54, 0x18 ], # e
    [ 0x08, 0x7E, 0x09, 0x01, 0x02 ], # f
    [ 0x18, 0xA4, 0xA4, 0xA4, 0x7C ], # g
    [ 0x7F, 0x08, 0x04, 0x04, 0x78 ], # h
    [ 0x00, 0x44, 0x7D, 0x40, 0x00 ], # i
    [ 0x40, 0x80, 0x84, 0x7D, 0x00 ], # j
    [ 0x7F, 0x10, 0x28, 0x44, 0x00 ], # k
    [ 0x00, 0x41, 0x7F, 0x40, 0x00 ], # l
    [ 0x7C, 0x04, 0x18, 0x04, 0x78 ], # m
    [ 0x7C, 0x08, 0x04, 0x04, 0x78 ], # n
    [ 0x38, 0x44, 0x44, 0x44, 0x38 ], # o
    [ 0xFC, 0x24, 0x24, 0x24, 0x18 ], # p
    [ 0x18, 0x24, 0x24, 0x18, 0xFC ], # q
    [ 0x7C, 0x08, 0x04, 0x04, 0x08 ], # r
    [ 0x48, 0x54, 0x54, 0x54, 0x20 ], # s
    [ 0x04, 0x3F, 0x44, 0x40, 0x20 ], # t
    [ 0x3C, 0x40, 0x40, 0x20, 0x7C ], # u
    [ 0x1C, 0x20, 0x40, 0x20, 0x1C ], # v
    [ 0x3C, 0x40, 0x30, 0x40, 0x3C ], # w
    [ 0x44, 0x28, 0x10, 0x28, 0x44 ], # x
    [ 0x1C, 0xA0, 0xA0, 0xA0, 0x7C ], # y
    [ 0x44, 0x64, 0x54, 0x4C, 0x44 ], # z
    [ 0x00, 0x08, 0x36, 0x41, 0x00 ], # {
    [ 0x00, 0x00, 0x77, 0x00, 0x00 ], # |
    [ 0x00, 0x41, 0x36, 0x08, 0x00 ], # }
    [ 0x02, 0x01, 0x02, 0x04, 0x02 ], # ~
    [ 0x55, 0x00, 0x55, 0x00, 0x55 ]
]

def Color656(r, g, b):
    c = 0
    c = r >> 3
    c = c << 6
    c = c | (g >> 2)
    c = c << 5
    c = c | (b >> 3)
    return c

def GetRawPixelDataFromBmp24File(name):
    with open(name, "rb") as f:
        signature = f.read(2)
        if signature == "BM":
            f.read(4) # Ignore data
            f.read(2) # Ignore data
            f.read(2) # Ignore data
            offset, = struct.unpack('<i', f.read(4))
            f.seek(offset)
            data = list()
            byte = f.read(1)
            while byte:
                data.append(ord(byte))
                byte = f.read(1)
    return data

def UnpackRawPixelBmp24Data(raw):
    i = 0
    data = list() # Rows.
    for y in xrange(0, MAX_HEIGHT, 1):
        data.append(list()) # Columns.
        for x in xrange(0, MAX_WIDTH, 1):
            data[y].append(list()) # Channels.
            data[y][x].append(raw[i + 2]) # Swap BGR to RGB formatted channels.
            data[y][x].append(raw[i + 1])
            data[y][x].append(raw[i + 0])
            i = i + 3
    data.reverse() # Bitmaps are stored up-side-down so let's flip the rows.
    return data

COLOR_BLACK  = Color656(  0,   0,   0)
COLOR_GREY   = Color656(192, 192, 192)
COLOR_WHITE  = Color656(255, 255, 255)
COLOR_RED    = Color656(255,   0,   0)
COLOR_PINK   = Color656(240, 100, 225)
COLOR_YELLOW = Color656(255, 255,   0)
COLOR_GOLDEN = Color656(255, 215,   0)
COLOR_BROWN  = Color656(128,  42,  42)
COLOR_BLUE   = Color656(  0,   0, 255)
COLOR_CYAN   = Color656(  0, 255, 255)
COLOR_GREEN  = Color656(  0, 255,   0)
COLOR_PURPLE = Color656(160,  32, 240)

MAX_WIDTH  = 0x60
MAX_HEIGHT = 0x40

FILL_RECT_DISABLE          = 0x00
FILL_RECT_ENABLE           = 0x01 

H_SCROLL_DISABLE           = 0x00
H_SCROLL_ENABLE            = 0x01

V_SCROLL_DISABLE           = 0x00
V_SCROLL_ENABLE            = 0x01

LOCK_MODE_DISABLE          = 0x12
LOCK_MODE_ENABLE           = 0x16

SET_COLUMN_ADDRESS         = 0x15
SET_ROW_ADDRESS            = 0x75

DRAW_LINE                  = 0x21
DRAW_RECT                  = 0x22
CLEAR_WINDOW               = 0x25
FILL_RECT                  = 0x26

CONTINUOUS_SCROLLING_SETUP = 0x27
DEACTIVE_SCROLLING         = 0x2E
ACTIVE_SCROLLING           = 0x2F

SET_CONTRAST_A             = 0x81
SET_CONTRAST_B             = 0x82
SET_CONTRAST_C             = 0x83

MASTER_CURRENT_CONTROL     = 0x87

SET_PRECHARGE_SPEED_A      = 0x8A
SET_PRECHARGE_SPEED_B      = 0x8B
SET_PRECHARGE_SPEED_C      = 0x8C

SET_REMAP                  = 0xA0
SET_DISPLAY_START_LINE     = 0xA1
SET_DISPLAY_OFFSET         = 0xA2
NORMAL_DISPLAY             = 0xA4
ENTIRE_DISPLAY_ON          = 0xA5
ENTIRE_DISPLAY_OFF         = 0xA6
INVERSE_DISPLAY            = 0xA7
SET_MULTIPLEX_RATIO        = 0xA8
DISPLAY_ON_DIM             = 0xAC
SET_MASTER_CONFIGURE       = 0xAD
DISPLAY_OFF                = 0xAE
DISPLAY_ON                 = 0xAF
POWER_SAVE_MODE            = 0xB0
PHASE_1_2_PERIOD           = 0xB1
CLOCK_DIVIDER              = 0xB3
SET_PRECHARGE_VOLTAGE      = 0xBB
SET_V_VOLTAGE              = 0xBE

LOCK_MODE                  = 0xFD

class SSD1331:
    COMMAND = gpio.LOW
    DATA    = gpio.HIGH

    def __init__(self, dc, rst, cs):
        self.rst = rst
        self.dc = dc
        self.cs = cs
        # Setup GPIO.
        gpio.setmode(gpio.BCM)
        gpio.setup(self.dc, gpio.OUT)
        gpio.output(self.dc, gpio.LOW)
        gpio.setup(self.rst, gpio.OUT)
        gpio.output(self.rst, gpio.HIGH)
        gpio.setup(self.cs, gpio.OUT)
        gpio.output(self.cs, gpio.HIGH)
        self.__OpenSPI() # Setup SPI.
        self.__Setup() # Setup device screen.
        self.Clear() # Blank the screen.
        return

    def __OpenSPI(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)
        self.spi.mode = 3
        self.spi.max_speed_hz = 6000000
        self.spi.cshigh = False
        return

    def __WriteCommand(self, data):
        gpio.output(self.dc, self.COMMAND)
        if isinstance(data, list) or isinstance(data, tuple):
            self.spi.xfer(data)
        return

    def __WriteData(self, data):
        gpio.output(self.dc, self.DATA)
        if isinstance(data, list) or isinstance(data, tuple):
            self.spi.xfer(data)
        return
    
    def __Setup(self):
        self.spi.cshigh = True
        self.spi.xfer([0])
        gpio.output(self.cs, gpio.LOW)
        time.sleep(0.1)
        gpio.output(self.rst, gpio.LOW)
        time.sleep(0.5)
        gpio.output(self.rst, gpio.HIGH)
        time.sleep(0.5)
        self.spi.cshigh = False
        self.spi.xfer([0])
        self.__WriteCommand([DISPLAY_OFF])
        self.__WriteCommand([SET_REMAP, 0x72])
        self.__WriteCommand([SET_DISPLAY_START_LINE, 0x00])
        self.__WriteCommand([SET_DISPLAY_OFFSET,     0x00])
        self.__WriteCommand([NORMAL_DISPLAY])
        self.__WriteCommand([SET_MULTIPLEX_RATIO,  0x3F])
        self.__WriteCommand([SET_MASTER_CONFIGURE, 0x8E])
        self.__WriteCommand([POWER_SAVE_MODE,  0x0B]) # Disabled.
        self.__WriteCommand([PHASE_1_2_PERIOD, 0x74]) # Default value.
        self.__WriteCommand([CLOCK_DIVIDER,    0xD0]) # Default value.
        self.__WriteCommand([SET_PRECHARGE_SPEED_A, 0x80])
        self.__WriteCommand([SET_PRECHARGE_SPEED_B, 0x80])
        self.__WriteCommand([SET_PRECHARGE_SPEED_C, 0x80])
        self.__WriteCommand([SET_PRECHARGE_VOLTAGE, 0x3E]) # Default value.
        self.__WriteCommand([SET_V_VOLTAGE, 0x3E]) # Default value.
        self.__WriteCommand([MASTER_CURRENT_CONTROL, 0x0F])
        self.__WriteCommand([SET_CONTRAST_A, 0xFF])
        self.__WriteCommand([SET_CONTRAST_B, 0xFF])
        self.__WriteCommand([SET_CONTRAST_C, 0xFF])
        self.__WriteCommand([DISPLAY_ON])
        return

    def Remove(self):
        gpio.cleanup()
        self.spi.close()
        return

    def DrawPixel(self, x, y, c):
        self.__WriteCommand([SET_COLUMN_ADDRESS, x, 0x5F, SET_ROW_ADDRESS, y, 0x3F])
        self.__WriteData([(c >> 8) & 0xFF, c & 0xFF])
        return

    def DrawLine(self, x0, y0, x1, y1, c):
        self.__WriteCommand([DRAW_LINE, x0 & 0xFF, y0 & 0xFF, x1 & 0xFF, y1 & 0xFF])
        self.__WriteCommand([(c >> 11) << 1, (c >> 5) & 0x3F, (c << 1) & 0x3F])
        return

    # Bresenham's line algorithm.
    def DrawLineBresenham(self, x0, y0, x1, y1, c):
        dx = x1 - x0
        if dx < 0:
            dx = x0 - x1
        sx = -1
        if x0 < x1:
            sx = 1
        dy = y1 - y0
        if dy < 0:
            dy = y0 - y1
        sy = -1
        if y0 < y1:
            sy = 1
        err = -dy / 2
        if dy < dx:
            err = dx / 2
        self.DrawPixel(x0, y0, c)
        while x0 != x1 or y0 != y1:
            e2 = err
            if e2 > -dx:
                err = err - dy
                x0 = x0 + sx
            if e2 < dy:
                err = err + dx
                y0 = y0 + sy
            self.DrawPixel(x0, y0, c)
        return

    def DrawTriangle(self, x0, y0, x1, y1, x2, y2, c):
        self.DrawLine(x0, y0, x1, y1, c)
        self.DrawLine(x1, y1, x2, y2, c)
        self.DrawLine(x0, y0, x2, y2, c)
        return

    def DrawRect(self, x0, y0, x1, y1, c, bg = 0):
        self.__WriteCommand([DRAW_RECT, x0 & 0xFF, y0 & 0xFF, x1 & 0xFF, y1 & 0xFF])
        self.__WriteCommand([(c >> 11) << 1, (c >> 5) & 0x3F, (c << 1) & 0x3F])
        self.__WriteCommand([(bg >> 11) << 1, (bg >> 5) & 0x3F, (bg << 1) & 0x3F])
        return

    def DrawCircle(self, x0, y0, r0, c):
        x = r0
        y = 0
        decision_over2 = 1 - x # Decision criterion divided by 2 evaluated at x = r, y = 0.
        while y <= x:
           self.DrawPixel( x + x0,  y + y0, c) # Octant 1.
           self.DrawPixel( y + x0,  x + y0, c) # Octant 2.
           self.DrawPixel(-x + x0,  y + y0, c) # Octant 4.
           self.DrawPixel(-y + x0,  x + y0, c) # Octant 3.
           self.DrawPixel(-x + x0, -y + y0, c) # Octant 5.
           self.DrawPixel(-y + x0, -x + y0, c) # Octant 6.
           self.DrawPixel( x + x0, -y + y0, c) # Octant 8.
           self.DrawPixel( y + x0, -x + y0, c) # Octant 7.
           y = y + 1
           if decision_over2 <= 0:
               decision_over2 = decision_over2 + 2 * y + 1 # Change in decision criterion for y -> y + 1.
           else:
               x = x - 1
               decision_over2 = decision_over2 + 2 * (y - x) + 1 # Change for y -> y + 1, x -> x - 1.
        return

    def DrawChar(self, x, y, ch, c):
        for i in xrange(0, 5, 1):
            line = ascii[ord(ch) & 0x7F][i]
            for j in xrange(0, 8, 1):
                if line & 0x1:
                    self.DrawPixel(x + i, y + j, c)
                line >>= 1
        return

    def DrawCharBg(self, x, y, ch, c, bg):
        for i in xrange(0, 5, 1):
            line = ascii[ord(ch) & 0x7F][i]
            self.DrawPixel(x + i, y, bg)
            y = y + 1
            for j in xrange(0, 8, 1):
                if line & 0x1:
                    self.DrawPixel(x + i, y + j, c)
                else:
                    self.DrawPixel(x + i, y + j, bg)
                line >>= 1
            y = y + 8
            self.DrawPixel(x + i, y, bg)
            y = y - 9
        return

    def DrawString(self, x, y, str, c):
        for i in str:
            if x > 0x5F:
                break
            self.DrawChar(x, y, i, c)
            x = x + 6
        return

    def DrawStringBg(self, x, y, str, c, bg):
        self.DrawLine(x, y, x, y + 9, bg)
        x = x + 1
        for i in str:
            if x > 0x5F:
                break
            self.DrawCharBg(x, y, i, c, bg)
            self.DrawLine(x + 5, y, x + 5, y + 9, bg)
            x = x + 6
        return

    def DrawFullScreenBitMap(self, data):
        self.__WriteCommand([SET_COLUMN_ADDRESS, 0, 0x5F, SET_ROW_ADDRESS, 0, 0x3F]) # Set the address to 0, 0.
        for y in xrange(0, len(data), 1):
            d = list() # Build up a list of pixel data to render an entire row per data write command.
            for x in xrange(0, len(data[y]), 1):
                c = Color656(data[y][x][0], data[y][x][1], data[y][x][2])
                d.append((c >> 8) & 0xFF)
                d.append(c & 0xFF)
            self.__WriteData(d)
        return

    def Blank(self):
        self.EnableFillMode(True)
        self.DrawRect(0x00, 0x00, 0x5F, 0x3F, COLOR_BLACK)
        self.EnableFillMode(False)
        return

    def Clear(self):
        self.__WriteCommand([CLEAR_WINDOW, 0x00, 0x00, 0x5F, 0x3F])
        return

    def TestEntireDisplay(self, enable):
        if enable:
            self.__WriteCommand([ENTIRE_DISPLAY_ON])
        else:
            self.__WriteCommand([ENTIRE_DISPLAY_OFF])
        return

    def EnableDisplay(self, enable):
        if enable:
            self.__WriteCommand([DISPLAY_ON])
        else:
            self.__WriteCommand([DISPLAY_OFF])
        return

    def EnableFillMode(self, enable):
        if enable:
           self.__WriteCommand([FILL_RECT, FILL_RECT_ENABLE])
        else:
           self.__WriteCommand([FILL_RECT, FILL_RECT_DISABLE])
        return

    def EnableLockMode(self, enable):
        if enable:
           self.__WriteCommand([LOCK_MODE, LOCK_MODE_ENABLE])
        else:
           self.__WriteCommand([LOCK_MODE, LOCK_MODE_DISABLE])
        return

    def SetScrollMode(self, horizontal, vertical):
        self.EnableScrollMode(False)
        self.__WriteCommand([CONTINUOUS_SCROLLING_SETUP, horizontal, 0x00, 0x3F, vertical, 0x00])
        return

    def EnableScrollMode(self, enable):
        if enable:
            self.__WriteCommand([ACTIVE_SCROLLING])
        else:
            self.__WriteCommand([DEACTIVE_SCROLLING])
        return

    def RectTest(self):
        self.Clear()
        time.sleep(0.01)
        self.EnableFillMode(True)
        for z in xrange(0, 10, 1):
            self.Clear()
            time.sleep(0.01)
            for x in xrange(0, 6, 1):
                for y in xrange(0, 4, 1):
                    r0 = random.randint(0, 255)
                    g0 = random.randint(0, 255)
                    b0 = random.randint(0, 255)
                    r1 = random.randint(0, 255)
                    g1 = random.randint(0, 255)
                    b1 = random.randint(0, 255)
                    self.DrawRect(1 + x * 16, 1 + y * 16, (x * 16) + 14, (y * 16) + 14, Color656(r0, g0, b0), Color656(r1, g1, b1))
            time.sleep(1)
        self.EnableFillMode(False)
        for z in xrange(0, 10, 1):
            self.Clear()
            time.sleep(0.01)
            for x in xrange(0, 6, 1):
                for y in xrange(0, 4, 1):
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    self.DrawRect(1 + x * 16, 1 + y * 16, (x * 16) + 14, (y * 16) + 14, Color656(r, g, b))
            time.sleep(1)
        self.EnableFillMode(True)
        for z in xrange(0, 10, 1):
            self.Clear()
            time.sleep(0.01)
            for x in xrange(0, 6, 1):
                for y in xrange(0, 4, 1):
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    self.DrawRect(1 + x * 16, 1 + y * 16, (x * 16) + 14, (y * 16) + 14, Color656(r, g, b), Color656(r, g, b))
            time.sleep(1)
        return

    def LineTest(self):
        self.Clear()
        time.sleep(0.01)
        for y in xrange(0, 32, 1):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            self.DrawLine(0x00, y * 2, 0x5F, y * 2, Color656(r, g, b))
        time.sleep(10)
        return

    def LockTest(self):
        self.Clear()
        time.sleep(0.01)
        self.DrawString(21, 16, "Lock Test", COLOR_WHITE)
        self.EnableLockMode(True)
        self.DrawString(0, 16, "Lock Test Failed", COLOR_RED)
        time.sleep(10)
        self.EnableLockMode(False)
        return

    def CharTest(self):
        self.Clear()
        time.sleep(0.01)
        i = 32
        for j in xrange(0, 6, 1):
            for k in xrange(0, 16, 1):
                self.DrawChar(k * 6, j * 8 + 4, chr(i), Color656(k * 16, 128, j * 36))
                i = i + 1
        time.sleep(10)
        return

    def ShapeTest(self):
        self.Clear()
        time.sleep(0.01)
        self.DrawStringBg(18, 4, "Shape Test", COLOR_BLACK, COLOR_WHITE)
        self.DrawCircle(16, 32, 10, COLOR_RED)
        self.DrawTriangle(38, 42, 58, 42, 48, 22, COLOR_GREEN)
        self.DrawRect(70, 22, 90, 42, COLOR_BLUE)
        time.sleep(10)
        return

    def BitMapTest(self, data):
        self.DrawFullScreenBitMap(data)
        time.sleep(10)
        return

    def ScrollTest(self):
        self.SetScrollMode(H_SCROLL_ENABLE, V_SCROLL_DISABLE)
        self.EnableScrollMode(True)
        time.sleep(10)
        self.EnableScrollMode(False)
        return

SSD1331_PIN_CS  = 23
SSD1331_PIN_DC  = 24
SSD1331_PIN_RST = 25

if __name__ == '__main__':
    raw_balloon  = GetRawPixelDataFromBmp24File("balloon.bmp")
    data_balloon = UnpackRawPixelBmp24Data(raw_balloon)
    device = SSD1331(SSD1331_PIN_DC, SSD1331_PIN_RST, SSD1331_PIN_CS)
    try:
        device.EnableDisplay(True)
        device.LockTest()
        device.LineTest()
        device.RectTest()
        device.ScrollTest()
        device.ShapeTest()
        device.CharTest()
        device.BitMapTest(data_balloon)
        device.EnableDisplay(False)
    finally:
        device.Remove()
