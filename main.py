from tkinter import *
from threading import Thread
from time import sleep
from decimal import Decimal

class Window:
    def __init__(self):
        self.started = False
        self.timer = 0
        self.run = False
        self.stopped = False
        self.running = False
        self.isFull = False
        self.win = Tk()
        self.win.configure(bg="black")
        self.win.geometry("650x300")
        self.win.minsize(650, 300)
        self.win.title("Cube Timer")
        Grid.columnconfigure(self.win, index=0, weight=1)
        Grid.rowconfigure(self.win, 0, weight=1)
        self.win.bind('<KeyPress>', self.pressEvent)
        self.win.bind('<KeyRelease>', self.releaseEvent)
        self.win.bind('<Configure>', self.resize)
        self.win.protocol('WM_DELETE_WINDOW', self.close)
        self.draw()
        self.win.mainloop()

    def draw(self):
        # draw the main timer

        self.timerText = Label(self.win, text="00.00", font=("DS-DIGITAL",200,"bold"), bg="black", fg="white")
        self.timerText.grid(row=0, column=0,  stick='news')
    
    def resize(self, e):
        size = e.width / 5
        self.timerText.configure(font=("DS-DIGITAL",int(size),"bold"))
    
    def display(self):
        if self.timer > 60:
            minutes = self.timer // 60
            seconds = self.timer % 60
            if len(str(minutes)) == 1:
                minutes = '0' + str(minutes)
            if len(str(seconds)[:-1]) == 2:
                seconds = '0' + str(seconds)
            self.timerText.configure(text=f'{minutes}:{str(seconds)[:-1]}')
        else:
            if len(str(self.timer)[:-1]) == 3: 
                self.timerText.configure(text=f'0{str(self.timer)[:-1]}')
            else:
                self.timerText.configure(text=f'{str(self.timer)[:-1]}')
    
    def updateTimer(self):
        i = 0
        while self.running:
            self.timer += Decimal('0.01')
            sleep(0.01)
            if i % 2:
                self.display()
            i += 1

    def startTimer(self):
        if not self.running:
            self.running = True
            self.timerThread = Thread(target=self.updateTimer, args=())
            self.timerThread.setDaemon(True)
            self.timerThread.start()
    
    def pressEvent(self, e):
        if e.keycode == 32:
            if not self.running:
                self.reset()
                self.timerText.configure(fg='red')
            else:
                self.display()
                self.timerText.configure(fg='light green')
                self.running = False
                self.stopped = True
        elif e.keycode == 122:
            if not self.isFull:
                self.win.attributes('-fullscreen', True)
                self.isFull = True
            else:
                self.win.attributes('-fullscreen', False)
                self.isFull = False
                
    def releaseEvent(self, e):
        if self.stopped: return
        self.timerText.configure(fg='white')
        if e.keycode == 32:
            self.startTimer()
    
    def reset(self):
        self.timerText.configure(text='00.00')
        self.timer = 0
        self.stopped = False
        self.running = False
        self.run = False
        self.started = False
    
    def close(self):
        self.running = False
        self.win.destroy()

    

Window()