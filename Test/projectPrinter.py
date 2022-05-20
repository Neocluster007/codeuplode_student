import evdev
from PIL import Image, ImageDraw, ImageFont
import os
import time
import requests
from io import BytesIO
from barcode import Code128
from barcode.writer import ImageWriter

from threading import Thread
#time.sleep(10)
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

capscodes = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

device = evdev.InputDevice('/dev/input/event0')
print(device)
#print(device.capabilities(verbose=True))
#print(device.leds(verbose=True))

state_data = False
timestamp = 0
x = ''
key_lookup = ""
caps = False


def ReadScaner():
    global x
    global key_lookup
    global timestamp
    global state_data
    global caps

    for event in device.read_loop():

        if event.type == evdev.ecodes.EV_KEY:
            data = evdev.categorize(event)
            timestamp = time.time()
            # print(str(data.scancode) + " - " + str(data.keystate))

            if data.scancode == 42:
                if data.keystate == 1:
                    caps = True
                if data.keystate == 0:
                    caps = False

            if data.keystate == 1:

                if (data.scancode == 28):
                    print(x)
                    '''
                    try:
                    '''

                    ts = time.time()
                    timestamp = ts

                    URL = "https://maas-printer.azure-api.net/printer-gateway/v1/orders/label/" + str(x)
                    r = requests.get(url=URL,
                                     headers={"Ocp-Apim-Subscription-Key": "2b8f2197a7da4414a96c2c03335eaaa9"})

                    data = r.json()

                    print(data['shipments'])

                    imMainOriginal = Image.open(r"Mainimage.png")
                    imMainOriginal = imMainOriginal.resize((imMainOriginal.size[0], imMainOriginal.size[1]))

                    for n in range(len(data['shipments'])):


                        with open('barcode_ShipmentNumber.jpeg', 'wb') as f:
                            Code128(data['shipments'][n]['shipment_number'], writer=ImageWriter()).write(f)

                        imBarcode = Image.open(r"barcode_ShipmentNumber.jpeg")
                        imBarcode = imBarcode.resize((290, 220))

                        imMain = imMainOriginal.copy()
                        draw_imMain = ImageDraw.Draw(imMain)

                        Date_RAW = data['shipments'][n]['return_date'].split('T')[0].split('-')
                        Date = Date_RAW[2] + "/" + Date_RAW[1] + "/" + Date_RAW[0]
                        # print(Date)

                        Shipper_Addr_Raw = data['shipments'][n]['shipper_address'].split(' ')
                        Shipper_Addr_1 = ""
                        Shipper_Addr_2 = ""
                        Shipper_Addr_3 = ""
                        Shipper_Counter = 0

                        for kk in range(len(Shipper_Addr_Raw) - 1, -1, -1):
                            if Shipper_Counter < 1:
                                Shipper_Addr_3 = Shipper_Addr_Raw[kk] + " " + Shipper_Addr_3
                            elif Shipper_Counter < 3:
                                Shipper_Addr_2 = Shipper_Addr_Raw[kk] + " " + Shipper_Addr_2
                            else:
                                Shipper_Addr_1 = Shipper_Addr_Raw[kk] + " " + Shipper_Addr_1
                            Shipper_Counter = Shipper_Counter + 1
                        Shipper_Addr_All = Shipper_Addr_1 + "\n" + Shipper_Addr_2 + "\n" + Shipper_Addr_3

                        Reciepient_Addr_Raw = data['shipments'][n]['reciepient_address'].split(' ')
                        Reciepient_Addr_1 = ""
                        Reciepient_Addr_2 = ""
                        Reciepient_Addr_3 = ""
                        Reciepient_Counter = 0

                        for hh in range(len(Reciepient_Addr_Raw) - 1, -1, -1):
                            if Reciepient_Counter < 1:
                                Reciepient_Addr_3 = Reciepient_Addr_Raw[hh] + " " + Reciepient_Addr_3
                            elif Reciepient_Counter < 3:
                                Reciepient_Addr_2 = Reciepient_Addr_Raw[hh] + " " + Reciepient_Addr_2
                            else:
                                Reciepient_Addr_1 = Reciepient_Addr_Raw[hh] + " " + Reciepient_Addr_1
                            Reciepient_Counter = Reciepient_Counter + 1
                        Reciepient_Addr_All = Reciepient_Addr_1 + "\n" + Reciepient_Addr_2 + "\n" + Reciepient_Addr_3 + "\n" + \
                                              data['shipments'][n]['reciepient_phone']

                        font = ImageFont.truetype(r'browa.ttf', 26)
                        font2 = ImageFont.truetype(r'browa.ttf', 35)
                        font3 = ImageFont.truetype(r'browa.ttf', 75)

                        draw_imMain.text((50, 225), "ผู้ส่ง : " + data['shipments'][n][
                            'shipper_name'] + "\n" + Shipper_Addr_All, fill="black", align="center", font=font)
                        draw_imMain.text((540, 290), "วันที่ส่งคืน : " + Date, fill="black", align="center",
                                         font=font)
                        draw_imMain.text((290, 440), "ผู้รับ : " + data['shipments'][n][
                            'reciepient_name'] + "\n" + Reciepient_Addr_All, fill="black", align="center",
                                         font=font2)

                        draw_imMain.text((24, 615), data['shipments'][n]['order_sequence'], fill="black",
                                         align="center", font=font3)

                        draw_imMain.text((305 + (94 * 0), 615), data['shipments'][n]['reciepient_zipcode'][0],
                                         fill="black", align="center", font=font3)
                        draw_imMain.text((305 + (94 * 1), 615), data['shipments'][n]['reciepient_zipcode'][1],
                                         fill="black", align="center", font=font3)
                        draw_imMain.text((305 + (94 * 2), 615), data['shipments'][n]['reciepient_zipcode'][2],
                                         fill="black", align="center", font=font3)
                        draw_imMain.text((305 + (94 * 3), 615), data['shipments'][n]['reciepient_zipcode'][3],
                                         fill="black", align="center", font=font3)
                        draw_imMain.text((305 + (94 * 4), 615), data['shipments'][n]['reciepient_zipcode'][4],
                                         fill="black", align="center", font=font3)

                        new_image = Image.new('RGB', (imMain.size[0], imMain.size[1]), (255, 255, 255))
                        new_image.paste(imMain, (0, 0))
                        new_image.paste(imBarcode, (830, 220))

                        #new_image.show()
                        new_image.save("Print_" + str(n) + ".png")

                        # print("Print_"+str(n)+".png")

                        os.system("lp -d Xprinter-XP-420B Print_" + str(n) + ".png")
                    '''
                    except:
                        print("Data Error")
                    '''
                    # print(data['order_code'])
                    x = ""



                else:
                    if caps:
                        key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)
                    else:
                        key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(data.scancode)

                    if (data.scancode != 42):
                        x += key_lookup
                        state_data = True

ReadScaner()

