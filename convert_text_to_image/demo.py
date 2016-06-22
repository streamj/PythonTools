# -*- coding: utf-8 -*-
# only support python2
import Image, ImageFont, ImageDraw

text =u"this is a test paragraph"
FONT = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

im = Image.new("RGB", (300, 50), (255, 255, 255))
dr = ImageDraw.Draw(im)
font = ImageFont.truetype(FONT, 18)

dr.text((10, 5), text, font=font, fill="#000000")

im.show()
im.save("demo.png")
