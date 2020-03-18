#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog
import time

words = ['Hello']
text = 'Hello\n'

i = 0
delay = 0.2
status = 0
upd = 0


def change_speed():
    global delay, speed_val
    delay = 60 / int(speed_val.get())


def stop():
    global status
    status = status = 1 if status == 0 else 0


def close():
    global status
    status = -1


def sec_back():
    global i, delay
    i = max(0, i - int(1 / delay))


def set_text():
    global words, text, i, text_pane
    file = filedialog.askopenfile()
    text = file.read()
    words = text.split()
    text_pane.config(state=NORMAL)
    text_pane.delete(1.0, '1.end')
    text_pane.insert(1.0, text)
    text_pane.config(state=DISABLED)
    i = 0


root = Tk()
root.title("Читалочка")
root.geometry("500x450+600+300")
root.resizable(0, 0)
root.protocol('WM_DELETE_WINDOW', close)

canvas = Canvas(root)
canvas.create_line(118, 75, 318, 75)
canvas.create_line(118, 115, 318, 115)
canvas.create_line(248, 75, 248, 115)
canvas.pack(fill=BOTH, expand=1)

label = Text(master=root, font='Courier 17', bd=0, bg=root['bg'], width=30, height=1)
label.config(state=DISABLED)
label.place(x=30, y=80)

text_pane = Text(master=root, font='Courier 13', wrap=WORD)
text_pane.place(x=20, y=300, width=450, height=130)
text_pane.insert(1.0, text)
text_pane.config(state=DISABLED)
scroll = Scrollbar(master=root, command=text_pane.yview)
scroll.place(x=470, y=300, width=15, height=130)
text_pane.config(yscrollcommand=scroll.set)

speed_val = StringVar()
speed_val.set('speed')

speed = Entry(master=root, textvariable=speed_val)
speed.place(x=100, y=250, width=100)

speed_btn = Button(master=root, text="Set speed", command=change_speed)
speed_btn.place(x=250, y=250)

pos_val = StringVar()
pos_val.set('0/0')
pos_label = Label(master=root, textvariable=pos_val, font='Courier 17', bd=0, bg=root['bg'],
                  width=10, height=1)
pos_label.place(x=270, y=150)

stop_btn = Button(master=root, text="Pause", command=stop)
stop_btn.place(x=200, y=150)

back_btn = Button(master=root, text="Second back", command=sec_back)
back_btn.place(x=70, y=150)

menubar = Menu(root)
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label='Open text', command=set_text)
menubar.add_cascade(menu=file_menu, label='File')
root.config(menu=menubar)


# text_pane.tag_add('back', '1.0', 'end.end')
# text_pane.tag_config('back', foreground='red')


def set_pane_view():
    global text_pane
    text_pane.tag_config()


def set_out_word(word):
    global label
    label.config(state=NORMAL)
    label.delete(1.0, '1.end')
    red = int(0.65 * len(word))
    outword = ' ' * (15 - red) + word
    label.insert(1.0, outword)
    label.tag_add('mid', '1.15', '1.16')
    label.tag_config('mid', foreground='red')
    label.config(state=DISABLED)


def update_root():
    global root
    root.update_idletasks()
    root.update()


def mainloop():
    global i, words, status
    last_time = time.time()
    while True:
        if status == 0 and time.time() - last_time > delay:
            if i >= len(words):
                status = 1
                continue
            last_time = time.time() + (len(words[i]) / 100)
            set_out_word(words[i])
            i += 1
        elif status == 1:
            if i < len(words):
                set_out_word(words[i])
            pos_val.set(str(i) + '/' + str(len(words)))
        elif status == -1:
            break
        update_root()
        time.sleep(1 / 40)


mainloop()
