'''

from tkinter import *

top = Tk()
top.attributes("-fullscreen", True)
text=Text(top)

# Configure the alignment of the text
text.tag_configure("tag_name", justify='center')

# Insert a Demo Text
text.insert("1.0", "How do I center align the text " "in a Tkinter Text widget?")

# Add the tag in the given text
text.tag_add("tag_name", "1.0", "end")
text.pack()
# Code to add widgets will go here...
top.mainloop()
'''


from tkinter import *
import tkinter
import paho.mqtt.client as paho
import time
import threading


Keyboard_App = tkinter.Tk()

broker="127.0.0.1"
port=1883

Keyboard_App.attributes("-fullscreen", True)

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

client1= paho.Client("keybroad_1")
client1.on_publish = on_publish
client1.connect(broker,port)

#ret = client1.publish("data/keybroad", "Ready")

def thread_function(name):
    global client1
    print('start t')
    client1.loop_start()

xx = threading.Thread(target=thread_function, args=(1,))
xx.start()



def select(value):
    if value == "Del":
        input = entry.get("1.0", 'end-2c')
        entry.delete("1.0", END)
        entry.insert("1.0", input, 'tag-center',)
        #entry.insert('end', value, 'tag-center')

    elif value == "Enter":
        entry.insert(tkinter.END, ' ')
        input = entry.get("1.0", 'end-2c')
        str_1 = input.split('\n')
        ret = client1.publish("data/keybroad", input)
        entry.delete(1.0, END)
        print(input)
        #entry.insert("1.0", input, 'tag-center', )

    elif value == "Tab":
        entry.insert(tkinter.END, '   ')

    else:
        entry.tag_configure('tag-center', justify='center')
        entry.insert('end', value, 'tag-center')
        #entry.insert(tkinter.END, value)


buttons = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M', 'Del','Enter'
]
entry = Text(Keyboard_App, width=18, height=1, font=("Helvetica", 32))
entry.grid(row=1, columnspan=15)
#entry.config(state= "disabled")


#entry.grid(row=1, columnspan=15)

varRow = 2
varColumn = 0

for button in buttons:
    command = lambda x=button: select(x)
    if button != "Enter":
        tkinter.Button(Keyboard_App, text=button, width=4, bg="#000000", fg="#ffffff", activebackground="#ffffff", activeforeground="#000000", relief="raised", padx=0, pady=15, bd=6, command=command).grid(row=varRow, column=varColumn)

    if button == "Enter":
        tkinter.Button(Keyboard_App, text=button, width=16, bg="#000000", fg="#ffffff",
                       activebackground="#ffffff", activeforeground="#000000", relief="raised", padx=0,
                       pady=15, bd=6, command=command).grid(row=5, columnspan=3,column=7)

    varColumn += 1
    if varColumn > 9:
        varColumn = 0
        varRow += 1

Keyboard_App.mainloop()
