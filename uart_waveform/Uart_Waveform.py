# -*- coding: UTF-8 -*-
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import serial
import time
import re
import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from tkinter import Label
from tkinter import Entry
import sys
import os

valid_head = "lumi"
port_default = "11"
variable_default = "lumi"
baudrate = 115200

N = 500


''' Class of Serial '''
class SERIAL:
    def __init__(self, com, bps, timeout):
        self.port = com
        self.bps = bps
        self.timeout = timeout
        self.is_open = False

        try:
            self.ser = serial.Serial(self.port, self.bps, timeout=self.timeout)
            self.read_thread = threading.Thread(target=self.read_data)
            self.read_thread.start()
            self.is_open = True
            print("Uart open")

        except Exception as e:
            self.ser = None
            print("-----------Error------------", e)


    ''' Read data from uart '''
    def read_data(self):
        while True:
            try:
                if self.is_open:
                    '''Return the number of bytes currently in the input buffer.'''
                    if self.ser.in_waiting:
                        try:
                            raw_str = self.ser.readline()
                            raw_str = raw_str.decode()
                            raw_str = raw_str.strip()
                            str_match = re.match(valid_head + r".*" + r"-?\d+\.?\d*$", raw_str)
                            if str_match != None:
                                num = float(re.findall(r"-?\d+\.?\d*$", str_match.string)[0])
                                y.pop(0)
                                y.append(num)
                            else:
                                print(raw_str)

                        except Exception as e:
                            print("here is :", __file__,
                                  sys._getframe().f_lineno)
                            print("-----------Error------------ ", e)
                    else:
                        time.sleep(0.001)
                else:
                    time.sleep(0.1)

            except Exception as e:
                print("Uart read------Serial is None--------", e)


    '''Open Uart'''
    def open(self):
        try:
            if not self.ser.is_open:
                self.ser.open()
                self.is_open = True
                print("Uart open")
            else:
                print("Already open")

        except Exception as e:
            print("Uart open------Serial is None--------", e)


    '''Close Uart '''
    def close(self):
        try:
            if self.ser.is_open:
                self.is_open = False
                self.ser.close()
                print("Uart close")

        except Exception as e:
            print("Uart close-----Serial is None--------", e)


'''Class of UI window'''
class WINDOW:
    def __init__(self):
        self.window = tk.Tk()
        self.has_start = False
        self.open_serial = None
        self.base_show()
        self.window.protocol("WM_DELETE_WINDOW", self.exit)

    def base_show(self):
        self.window.title("Uart Waveform")
        weight = 300
        high = 150
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x_ = (ws / 2) - (weight / 2)
        y_ = (hs / 2) - (high / 2)
        self.window.geometry('%dx%d+%d+%d' % (weight, high, x_, y_))
        self.show_button()
        self.show_menu()
        self.show_label()
        self.show_entry()


    '''Label'''
    def show_label(self):
        Label(self.window, text="COM: ").grid(row=0, column=0)
        Label(self.window, text="Baudrate:").grid(row=0, column=2)
        Label(self.window, text="Variable:").grid(row=1, column=0)
        Label(self.window, text="Y ").grid(row=3, column=0)
        Label(self.window, text="Min").grid(row=2, column=1)
        Label(self.window, text="Max").grid(row=2, column=2)
        Label(self.window, text="Points:").grid(row=1, column=2)


    '''Entry'''
    def show_entry(self):
        self.port_entry = Entry(self.window, width=10)
        self.port_entry.insert(0, port_default)
        self.port_entry.grid(row=0, column=1)

        self.baudrate_entry = Entry(self.window, width=10)
        self.baudrate_entry.insert(0, 115200)
        self.baudrate_entry.grid(row=0, column=3)

        self.variable_entry = Entry(self.window, width=10)
        self.variable_entry.insert(0, variable_default)
        self.variable_entry.grid(row=1, column=1)

        self.ymin_entry = Entry(self.window, width=10)
        self.ymin_entry.insert(0, 0)
        self.ymin_entry.grid(row=3, column=1)

        self.ymax_entry = Entry(self.window, width=10)
        self.ymax_entry.insert(0, 100)
        self.ymax_entry.grid(row=3, column=2)

        self.points_entry = Entry(self.window, width=10)
        self.points_entry.insert(0, 500)
        self.points_entry.grid(row=1, column=3)


    '''Button'''
    def show_button(self):
        start_button = tk.Button(self.window,
                                 text='Start',
                                 width=5,
                                 height=1,
                                 command=self.start)
        start_button.grid(row=4, column=1)
        start_button = tk.Button(self.window,
                                 text='Pause',
                                 width=5,
                                 height=1,
                                 command=self.pause)
        start_button.grid(row=4, column=2)


    '''Menubar'''
    def show_menu(self):
        self.menubar = Menu(self.window)
        self.menubar.add_command(label='about', command=self.about)
        self.window.config(menu=self.menubar)


    '''About'''
    def about(self):
        messagebox.showinfo('About', 'Author:    Hammer\r\n')


    '''Handle for start button'''
    def start(self):
        global valid_head
        port = self.port_entry.get()
        valid_head = self.variable_entry.get()
        baudrate = int(self.baudrate_entry.get())

        if not self.has_start:
            self.open_serial = SERIAL("COM" + str(port), baudrate, None)
            if self.open_serial.is_open:
                self.has_start = True
                plt_init(int(self.points_entry.get()),
                         int(self.ymin_entry.get()),
                         int(self.ymax_entry.get()))
                draw_data()
            else:
                messagebox.showerror('Error:',
                                     'Can\'t open ' + "COM" + str(port))
        else:
            try:
                if not self.open_serial.ser.is_open:
                    self.open_serial.open()
                else:
                    print(self.open_serial.ser.name + " has already opened")

            except Exception as e:
                print("Button start-----Serial is None--------", e)

    '''Handle for start button'''
    def pause(self):
        try:
            if self.open_serial.ser.is_open:
                self.open_serial.close()
            else:
                print(self.open_serial.ser.name + " has already closed")

        except Exception as e:
            print("Button pause-----Serial is None--------", e)


    '''Exit all process'''
    def exit(self):
        print("Exit")
        try:
            self.open_serial.close()
            plt.close()
        except Exception as e:
            print(e)
        self.window.destroy()
        os._exit(0)


'''Initlization parameters of plt'''
def plt_init(point_nums, y_min, y_max):
    global x, y, fig, ax, line, N, avg_line
    N = point_nums
    y = np.zeros(N + 1).tolist()
    x = np.linspace(0, N, N + 1)
    fig, ax = plt.subplots()
    line, = ax.plot(x, y, 'blue', label = valid_head)
    avg_line = ax.axhline(y = 10, c = "c", ls = "--")
    plt.legend()  #添加图例
    ax.set_xlim(0, N)
    ax.set_ylim(y_min, y_max)


'''Update show data'''
def update(num):
    line.set_ydata(y)
    return line,


'''Draw data form uart'''
def draw_data():
    '''ani can't delete!'''
    ani = animation.FuncAnimation(fig,
                                  update,
                                  interval=10,
                                  blit=True,
                                  save_count=N)
    plt.grid()  #添加网格
    plt.show()


if __name__ == "__main__":
    main_window = WINDOW()
    main_window.window.mainloop()
