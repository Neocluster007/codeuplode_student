import serial
import code128
#import evdev
from PIL import Image, ImageDraw, ImageFont
import os
import time
import requests
from io import BytesIO
from barcode import Code128
from barcode.writer import ImageWriter
import paho.mqtt.client as paho
import threading

from threading import Thread

data_str_number = ""
path_location = "/home/pi/MAASProject/"
#path_location = "E:/Google_Drive/Neocluster/Neocluster/Neocluster_RD/Project 2022/010 Priter Sticker/Printer/18052022_VersionFixBug_error/MAASProject"

def Print_ter():
    global data_str_number

    try:

        # ts = time.time()
        # timestamp = ts

        # print(str(len(x)))
        print(data_str_number)

        URL = "https://maas-printer.azure-api.net/printer-gateway/v1/orders/label/" + \
              str(data_str_number)
        r = requests.get(url=URL,
                         headers={"Ocp-Apim-Subscription-Key": "2b8f2197a7da4414a96c2c03335eaaa9"})

        data = r.json()

        print(data['shipments'])

        imMainOriginal = Image.open(path_location+ r"Mainimage.png")
        imMainOriginal = imMainOriginal.resize( (imMainOriginal.size[0], imMainOriginal.size[1]))

        for n in range(len(data['shipments'])):

            with open(path_location+ 'barcode_ShipmentNumber.jpeg', 'wb') as f:
                Code128(
                    data['shipments'][n]['shipment_number'], writer=ImageWriter()).write(f)

            #imBarcode = Image.open(path_location+  r"barcode_ShipmentNumber.jpeg")
            #imBarcode = imBarcode.resize((360, 220))

            imMain = imMainOriginal.copy()
            draw_imMain = ImageDraw.Draw(imMain)

            imBarcode = code128.image(data['shipments'][n]['shipment_number'], height=180)
            imBarcode = imBarcode.resize((350, 180))
            #imBarcode = imBarcode.resize((360, 220))

            Date_RAW = data['shipments'][n]['return_date'].split('T')[
                0].split('-')
            Date = Date_RAW[2] + "/" + \
                   Date_RAW[1] + "/" + Date_RAW[0]
            # print(Date)
            Shipper_Addr_Raw = "-"
            Shipper_Addr_All = "-"
            Reciepient_Addr_Raw = "-"
            Reciepient_Addr_All = "-"

            if data['shipments'][n]['shipper_address'] is None:
                pass
            else:
                Shipper_Addr_Raw = data['shipments'][n]['shipper_address'].split(' ')

                Shipper_Addr_1 = ""
                Shipper_Addr_2 = ""
                Shipper_Addr_3 = ""
                Shipper_Counter = 0

                for kk in range(len(Shipper_Addr_Raw) - 1, -1, -1):
                    if Shipper_Counter < 1:
                        Shipper_Addr_3 = Shipper_Addr_Raw[kk] + \
                                         " " + Shipper_Addr_3
                    elif Shipper_Counter < 3:
                        Shipper_Addr_2 = Shipper_Addr_Raw[kk] + \
                                         " " + Shipper_Addr_2
                    else:
                        Shipper_Addr_1 = Shipper_Addr_Raw[kk] + \
                                         " " + Shipper_Addr_1
                    Shipper_Counter = Shipper_Counter + 1
                Shipper_Addr_All = Shipper_Addr_1 + "\n" + \
                                   Shipper_Addr_2 + "\n" + Shipper_Addr_3

            if data['shipments'][n]['reciepient_address'] is None:
                pass
            else:

                Reciepient_Addr_Raw = data['shipments'][n]['reciepient_address'].split(
                    ' ')
                Reciepient_Addr_1 = ""
                Reciepient_Addr_2 = ""
                Reciepient_Addr_3 = ""
                Reciepient_Counter = 0

                for hh in range(len(Reciepient_Addr_Raw) - 1, -1, -1):
                    if Reciepient_Counter < 1:
                        Reciepient_Addr_3 = Reciepient_Addr_Raw[hh] + \
                                            " " + Reciepient_Addr_3
                    elif Reciepient_Counter < 3:
                        Reciepient_Addr_2 = Reciepient_Addr_Raw[hh] + \
                                            " " + Reciepient_Addr_2
                    else:
                        Reciepient_Addr_1 = Reciepient_Addr_Raw[hh] + \
                                            " " + Reciepient_Addr_1
                    Reciepient_Counter = Reciepient_Counter + 1
                Reciepient_Addr_All = Reciepient_Addr_1 + "\n" + Reciepient_Addr_2 + "\n" + Reciepient_Addr_3 + "\n" + \
                                      data['shipments'][n]['reciepient_phone']

            #font = ImageFont.truetype(path_location+ r'browa.ttf', 26)
            font = ImageFont.truetype(path_location + r'browa.ttf', 35)
            font2 = ImageFont.truetype(path_location+
                r'browa.ttf', 35)
            font3 = ImageFont.truetype(path_location+
                r'browa.ttf', 75)

            if data['shipments'][n]['shipper_name'] is None:
                draw_imMain.text((30, 155), "ผู้ส่ง :-\n" + Shipper_Addr_All, fill="black", align="center", font=font)
            else:
                draw_imMain.text((30, 155),
                                 "ผู้ส่ง : " + data['shipments'][n]['shipper_name'] + "\n" + Shipper_Addr_All,
                                 fill="black", align="center", font=font)

            draw_imMain.text((510, 190), "วันที่ส่งคืน : " + Date, fill="black", align="center",
                             font=font)
            draw_imMain.text((300, 450), "ผู้รับ : " + data['shipments'][n][
                'reciepient_name'] + "\n" + Reciepient_Addr_All, fill="black", align="center",
                             font=font2)

            draw_imMain.text((18, 620), data['shipments'][n]['order_sequence'], fill="black",
                             align="center", font=font3)

            draw_imMain.text((255 + (93 * 0), 620), data['shipments'][n]['reciepient_zipcode'][0],
                             fill="black", align="center", font=font3)
            draw_imMain.text((255 + (93 * 1), 620), data['shipments'][n]['reciepient_zipcode'][1],
                             fill="black", align="center", font=font3)
            draw_imMain.text((255 + (93 * 2), 620), data['shipments'][n]['reciepient_zipcode'][2],
                             fill="black", align="center", font=font3)
            draw_imMain.text((255 + (93 * 3), 620), data['shipments'][n]['reciepient_zipcode'][3],
                             fill="black", align="center", font=font3)
            draw_imMain.text((255 + (93 * 4), 620), data['shipments'][n]['reciepient_zipcode'][4],
                             fill="black", align="center", font=font3)

            fontbarcode = ImageFont.truetype(path_location + r'browa.ttf', 60)
            draw_imMain.text((785, 400), data['shipments'][n]['shipment_number'], fill="black",
                             align="center",
                             font=fontbarcode)

            new_image = Image.new(
                'RGB', (imMain.size[0], imMain.size[1]), (255, 255, 255))
            new_image.paste(imMain, (0, 0))
            new_image.paste(imBarcode, (760, 220))

            # new_image.show()
            new_image.save("Print_" + str(n) + ".png")

            print("Print_"+str(n)+".png")
            os.system( "lp -d Xprinter-XP-420B Print_" + str(n) + ".png")

    except Exception:
        print("Data Error --> ")


def on_message(client, userdata, message):
    global data_str_number
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    
    x = str(message.payload.decode("utf-8"))
    data_str_number = x
    Print_ter()

broker="127.0.0.1"
port=1883

client1= paho.Client("keybroad_2")
client1.connect(broker,port)
client1.on_message=on_message
client1.subscribe("data/keybroad")

def thread_function(name):
    global client1
    print('start t')
    client1.loop_start()

x = threading.Thread(target=thread_function, args=(1,))
x.start()

ser = serial.Serial(
    port='/dev/ttyACM0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
count=1

data_str = ""

while True:
    for line in ser.read():

        #print(chr(line) + " - " + str(line))
        #count = count+1
        if(line == 13):
            print(data_str)
            data_str_number = data_str 
            Print_ter()
            #ret = client1.publish("data/keybroad", data_str)
            data_str = ""
        else:
            data_str = data_str + chr(line)
ser.close()