import pyautogui as pag
from tkinter import *
import threading
import time
from tkinter import messagebox

#==============================================================

interval = 10

position_target_list = []

is_start = 0
#==============================================================
class MainWindow:
    def __init__(self, root):

        self.root = root
        
        self.root.title('你瞅啥')
        
        self.mouse_position = StringVar()
        
        self.mouse_target_position = StringVar()

        self.get_position_thread = threading.Thread(target = self.get_mouse_position, daemon=True)

        self.click_button_thread = threading.Thread(target = self.click_button, daemon=True)

        self.menubar = Menu(self.root)

    def show(self):

        w = 260

        h = 120
        
        ws = self.root.winfo_screenwidth()
        
        hs = self.root.winfo_screenheight()

        x = (ws/2) - (w/2)
        
        y = (hs/2) - (h/2)
        
        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
        frame = LabelFrame(self.root, height = 400, width = 600, text="Mouse")

        frame.pack(fill = "both", expand=True, padx=5, pady=5)

        Label(frame, text="Position：").grid(row = 0, column = 0)

        Label(frame, text="Target：").grid(row = 1, column = 0)

        Label(frame, text="Interval(s)：").grid(row = 2, column = 0)

        Entry(frame, textvariable = self.mouse_position).grid(row = 0, column = 1)

        self.target = Entry(frame, textvariable = self.mouse_target_position)

        self.target.grid(row = 1, column = 1)

        self.interval = Entry(frame, width = 6)

        self.interval.grid(row = 2, column = 1, sticky=W)

        Button(frame, text = "Start", fg = "black", command = self.Start).grid(row = 2, column = 1, padx=5, pady=5)
        
        Button(frame, text = "Stop", fg = "black", command = self.Stop).grid(row = 2, column = 1, padx=5, pady=5, sticky = E)

        self.menubar.add_command(label='about', command=self.about)

        self.root.config(menu = self.menubar)
        
    def about(self):
        
        messagebox.showinfo('About','瞅啥瞅\n') 

    def get_mouse_position(self):
        
        try:
            while True:       
                x,y = pag.position()
                
                self.mouse_position.set(str(x)+','+str(y))
            
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            
            print('end...')
            
    def click_button(self):

        global position_target_list

        global interval

        global is_start
        
        while True:

            print('is_start：%d' % is_start)
        
            if is_start:
                
                if(position_target_list == []):
                
                    pag.click()
                
                    print('click here...')
                
                else:
                
                    pag.click(position_target_list[0], position_target_list[1])

                    print('click:%d, %d' % (position_target_list[0], position_target_list[1]))

            time.sleep(interval)

        
    def get_param(self):

        global interval

        global position_target_list

        if(self.target.get() == ''):
                
            print('self.target.get() == ''')
            
        else:

            target_str = self.target.get().split(',')

            position_target_list = list(map(int, target_str))

            print(position_target_list)
        
        if(self.interval.get() == ''):
                
            print('self.interval.get() == ''')
                
        else:
            
            interval = int(self.interval.get())
                
            print(self.interval.get())

        
    def Start(self):        

        global is_start

        is_start = 1

        try:
            self.get_param()
        
            self.get_position_thread.start()
        
            self.click_button_thread.start()

        except RuntimeError:
            
            print('Thread has already started...')


    def Stop(self):

        global interval

        global position_target_list
    
        global is_start
    
        position_target_list == []

        interval = 10

        is_start= 0

       

root = Tk()
    
window = MainWindow(root)
    
window.show()

root.mainloop()
        
