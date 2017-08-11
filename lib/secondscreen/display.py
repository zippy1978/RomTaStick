import time
import RPi.GPIO as GPIO
import spidev
import textwrap
import os.path
from PIL import Image, ImageDraw, ImageFont

import ssd1331
from menu import *
import Adafruit_ILI9341 as TFT
import Adafruit_GPIO.SPI as SPI

from game.game import *

class BaseDisplay(object):

    width = 0
    height = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def show_game_info(self, game_info):
        raise NotImplementedError('Method not implemented')

    def show_game_details(self, game_info):
        target_size = self.width, self.height

        # Text settings
        max_line_size = 45
        line_height = self.height / 15

        # Colors
        text_color = (44, 44, 52)
        bg_color = (255, 255, 255)
        title_color = (83, 1, 147)

        # Font
        fnt_size = int(line_height * 0.9)
        fnt = ImageFont.truetype('/home/pi/RomTaStick/fonts/Roboto-Regular.ttf', fnt_size)
        title_fnt = ImageFont.truetype('/home/pi/RomTaStick/fonts/Roboto-Bold.ttf', fnt_size)

        img = Image.new("RGB", target_size, bg_color)
        draw = ImageDraw.Draw(img)

        x_offset = int(self.width * 0.02)
        y_offset = 0
        # Title
        draw.rectangle([0 , y_offset, target_size[0], line_height], fill=title_color)
        draw.text((x_offset, y_offset), game_info.name, font=fnt, fill=bg_color)
        y_offset += line_height
        y_offset += line_height
        # Developer
        if game_info.developer != None:
            dev_label = 'Developer: '
            draw.text((x_offset, y_offset), dev_label, font=title_fnt, fill=text_color)
            draw.text((x_offset + draw.textsize(dev_label, font=title_fnt)[0], y_offset), game_info.developer, font=fnt, fill=text_color)
            y_offset += line_height
        # Year
        if game_info.releasedate != None:
            year_label = 'Year: '
            draw.text((x_offset, y_offset), year_label, font=title_fnt, fill=text_color)
            draw.text((x_offset + draw.textsize(year_label, font=title_fnt)[0], y_offset), game_info.releasedate[:4], font=fnt, fill=text_color)
            y_offset += line_height
        # Genre
        if game_info.genre != None:
            genre_label = 'Genre: '
            draw.text((x_offset, y_offset), genre_label, font=title_fnt, fill=text_color)
            draw.text((x_offset + draw.textsize(genre_label, font=title_fnt)[0], y_offset), game_info.genre, font=fnt, fill=text_color)
            y_offset += line_height
        # Description
        if game_info.description != None:
            y_offset += line_height
            draw.text((x_offset, y_offset), textwrap.fill(game_info.description, max_line_size), font=fnt, fill=text_color)

        self.show_image(img)

    def show_splashscreen(self):
        self.show_image_from_file('/home/pi/RomTaStick/images/splash@%dx%d.bmp' % (self.width, self.height))

    def show_image_from_file(self, image_path):
        raise NotImplementedError('Method not implemented')

    def show_image(self, image):
        raise NotImplementedError('Method not implemented')

    def show_system_message(self, message):
        target_size = self.width, self.height

        # Colors
        bg_color = (83, 1, 147)
        text_color = (255, 255, 255)

        # Fonts
        fnt_size = int(self.width / 15)
        fnt = ImageFont.truetype('/home/pi/RomTaStick/fonts/Roboto-Bold.ttf', fnt_size)

        img = Image.new("RGBA", target_size, bg_color)
        draw = ImageDraw.Draw(img)

        txt = textwrap.fill(message, 20)
        w, h = draw.textsize(txt, font=fnt)
        draw.text(((target_size[0] / 2) - (w / 2), (target_size[1] / 2) - (h / 2)), txt, font=fnt, fill=text_color, align="center")


        # Convert to BMP
        img = img.convert("RGB")

        # Show image
        self.show_image(img)

    def show_menu(self, menu):
        target_size = self.width, self.height
        max_number_of_lines = 7
        line_height = self.height / max_number_of_lines
        # Font
        fnt = ImageFont.truetype('/home/pi/RomTaStick/fonts/Roboto-Regular.ttf', int(line_height * 0.9))
        # Colors
        bg_color = (255, 255, 255)
        title_color = (83, 1, 147)
        highlight_color = (44, 44, 52)

        img = Image.new("RGB", target_size, bg_color)
        draw = ImageDraw.Draw(img)
        x_offset = int(self.width * 0.02)
        y_offset = 0
        # Title
        draw.rectangle([0 , y_offset, target_size[0], line_height], fill=title_color)
        draw.text((x_offset, y_offset), menu.title, font=fnt, fill=bg_color)
        y_offset += line_height
        # Items
        symbol_margin = line_height * 0.25
        x_symbol_offset = self.width * 0.9
        for index, item in enumerate(menu.items):

            text_color = highlight_color
            if menu.get_selected_index() == index:
                draw.rectangle([0 , y_offset, self.width, y_offset + line_height], fill=highlight_color)
                text_color = bg_color

            # Draw text
            draw.text((x_offset, y_offset), item.name, font=fnt, fill=text_color)

            # Draw symbol
            if item.symbol == MenuItem.SYMBOL_ARROW:
                draw.polygon([(x_symbol_offset, y_offset + symbol_margin), (self.width - symbol_margin, y_offset + (line_height/2)), (x_symbol_offset, y_offset + line_height - symbol_margin)], fill=text_color)

            y_offset += line_height

        self.show_image(img)

    def show_game_info(self, game_info):
        target_size = self.width, self.height
        img = Image.new("RGBA", target_size, "black")

        # Fonts
        fnt_size = int(self.width / 15)
        title_fnt = ImageFont.truetype('/home/pi/RomTaStick/fonts/Roboto-Bold.ttf', fnt_size)
        fnt = ImageFont.truetype('/home/pi/RomTaStick/fonts/Roboto-Regular.ttf', fnt_size)

        # Colors
        text_color = (255, 255, 255)

        image_file = game_info.image

        if image_file != None and os.path.isfile(image_file):

            # Game image exists

            # Resize game image
    	    game_img = Image.open(image_file)
    	    original_size = game_img.size
            scale = 0.9
            height_ratio = float(target_size[1] * scale) / float(original_size[1])
            width_ratio = float(target_size[0] * scale) / float(original_size[0])
            ratio = width_ratio
            if height_ratio < width_ratio:
                ratio = height_ratio
            thumb_size = (int(original_size[0] * ratio), int(original_size[1] * ratio))
            game_img = game_img.resize(thumb_size, Image.ANTIALIAS)

            # Merge with background
            img.paste(game_img, ((target_size[0] / 2) - (thumb_size[0] / 2), ((target_size[1] / 2) - (thumb_size[1] / 2))))

        else:

            # No game image found: just display name
            draw = ImageDraw.Draw(img)
            name = game_info.name
            if name != None:
                txt = textwrap.fill(name, 20)
                w, h = draw.textsize(txt, font=title_fnt)
                draw.text(((target_size[0] / 2) - (w / 2), (target_size[1] / 2) - (h / 2)), txt, font=title_fnt, fill=text_color, align="center")

        # Convert to BMP
        img = img.convert("RGB")

        # Show image
        self.show_image(img)


class SSD1331Display(BaseDisplay):

    device = None

    def __init__(self):
        super(SSD1331Display, self).__init__(96, 64)
        self.device = self._device_init()

    # Device initialisation
    def _device_init(self):
        GPIO.setwarnings(False)
        SSD1331_PIN_CS  = 23
        SSD1331_PIN_DC  = 24
        SSD1331_PIN_RST = 25
        return ssd1331.SSD1331(SSD1331_PIN_DC, SSD1331_PIN_RST, SSD1331_PIN_CS)

    # Release Device
    def _device_release(self, device):
        self.device.EnableDisplay(False)
        self.device.Remove()

    def show_image_from_file(self, image_path):
        raw_data = ssd1331.GetRawPixelDataFromBmp24File(image_path)
        image_data = ssd1331.UnpackRawPixelBmp24Data(raw_data)
        self.device.EnableDisplay(True)
        time.sleep(0.1)
        self.device.DrawFullScreenBitMap(image_data)

    def show_image(self, image):
        tmp_bmp = "/tmp/img.bmp"
        image.save(tmp_bmp, "BMP")
        self.show_image_from_file(tmp_bmp)
        os.remove(tmp_bmp)


class ILI9341Display(BaseDisplay):

    # Attention : all images must be rotated as ILI9341 is 240x320

    device = None

    def __init__(self):
        super(ILI9341Display, self).__init__(320, 240)
        self._device_init()

    # Device initialisation
    def _device_init(self):
        GPIO.setwarnings(False)
        DC = 25
        RST = 24
        SPI_PORT = 0
        SPI_DEVICE = 0
        self.device = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
        self.device.begin()

    def show_image_from_file(self, image_path):
        self.show_image(Image.open(image_path))

    def show_image(self, image):
        image = image.rotate(90, expand=True).resize((self.height, self.width))
        self.device.display(image)
