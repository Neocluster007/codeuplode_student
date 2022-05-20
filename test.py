import os
from PIL import Image
import zpl

l = zpl.Label(60,100)
height = 0
l.origin(0,0)
l.write_text("Neocluster1992", char_height=10, char_width=8, line_width=60, justification='C')
l.endorigin()

height += 5
l.origin(22, height)
l.write_barcode(height=70, barcode_type='U', check_digit='Y')
l.write_text('07000002198')
l.endorigin()


with open('print.txt', 'w') as f:
    f.write(l.dumpZPL())

print(l.dumpZPL())
l.preview()

os.system("lp -d Xprinter-XP-420B -o raw print.txt")