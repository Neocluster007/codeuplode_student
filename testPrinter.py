import os


from PIL import Image, ImageDraw, ImageFont

#from PIL import Image
import zpl
import base64

def text(output_path):
    image = Image.new("RGB", (200, 200), "white")
    draw = ImageDraw.Draw(image)
    draw.text((10, 10), "ทดสอบ",fill ="black")
    draw.text((10, 25), "Pillow",fill ="black")
    image.save(output_path)

str_ = "text.bmp"
text(str_)

l = zpl.Label(60,100)

'''
height = 0
l.origin(0,0)
l.write_text("asdasd", char_height=10, char_width=8, line_width=60, justification='C')
l.endorigin()

height += 5
l.origin(22, height)
l.write_barcode(height=70, barcode_type='U', check_digit='Y')
l.write_text('07000002198')
l.endorigin()
'''

im = Image.open(str_)
im = im.rotate(90)

im2 = Image.open('Mainimage.png')
im2 = im2.rotate(90)
#im.show()

height = 0
image_width = 60

l.origin(0,0)
l.write_text("ดสอบ?", char_height=10, char_width=8, line_width=60, justification='C')
l.endorigin()

'''
l.origin((l.width-image_width)/2, height)
image_height = l.write_graphic( im, image_width)
l.endorigin()
'''


#l.origin(0, 0)
#l.write_graphic( im2, 60)
#l.endorigin()




print(l.dumpZPL())
#l.preview()