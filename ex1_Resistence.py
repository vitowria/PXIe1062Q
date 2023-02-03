import nidmm
import pandas as pd 
import numpy as np 
import pyqtgraph as pg
import time
import tkinter

from pyqtgraph.Qt import QtCore
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot

from tkinter import messagebox
from tkinter import Tk, Button, Label, Frame

###################################################################################################################


win = pg.GraphicsLayoutWidget(show=True)

liste = []
time_measurements = []

data3 = []
ptr3 = 0

#######################################################  To cvs  ##################################################

def to_cvs(liste, time_mesurements):
    dict = {'resistence (Ohms)': liste, 'time (sec)': time_measurements}  
    df = pd.DataFrame(dict) 
    df.to_csv('DataResistence.csv', index = False)

####################################################################################################################

def geometry():
    app.minsize(300,200)
    app.maxsize(640,480)
    app.geometry("500x300")

def winflag(*args):
    expression.set(expression.get())
    resolution.set(resolution.get())

    num = expression.get()
    resolut = resolution.get()

def mainp():
    with nidmm.Session("PXI1Slot2") as session:
        
        num = expression.get()
        resolut = resolution.get()
        
        
        print(num, resolut)
        app.destroy()
        array_size = 50          #definition of the increase of the vector of samples

        session.configure_measurement_digits(nidmm.Function.TWO_WIRE_RES, num, resolut) #definition of the measurements caracteristics
            
        p4 = win.addPlot()
        p4.setClipToView(True)
        curve4 = p4.plot()


        def update():
            global data3, ptr3
            start = time.time()
            liste.append(session.read())
            end = time.time()  
            if ptr3>0:
                timer = time_measurements[ptr3-1]+ end-start
                time_measurements.append(timer) 
                to_cvs(liste, time_measurements)
            else:
                time_measurements.append(end-start)
                to_cvs(liste, time_measurements)  
            
            data3.append(liste[ptr3])
            ptr3 += 1
            if ptr3 >= len(data3):
                tmp = data3
                data3.extend([]*array_size)
                data3[:len(tmp)] = tmp
            curve4.setData(data3[:ptr3])

        ##################################################  Plot  ########################################################
        timers = pg.QtCore.QTimer()
        timers.timeout.connect(update)
        timers.start(100)
        if __name__ == '__main__':
                pg.exec()

##################################################  Interface  ########################################################
app = tkinter.Tk()
app.title("Configurations (Resistence)")
geometry()

expression = tkinter.IntVar()
expression.trace("w", winflag)

resolution = tkinter.DoubleVar()
resolution.trace("w", winflag)

label_range = tkinter.Label(app,text="Range")
label_range.pack()

entry = tkinter.Entry(app, textvariable = expression, width = 30)
entry.pack()

label_resolution = tkinter.Label(app,text="Resolution")
label_resolution.pack()

entry_resolution = tkinter.Entry(app, textvariable = resolution, width = 30)
entry_resolution.pack()


btn = tkinter.Button(app, text = "ok", width = 15, height = 1, command = mainp)
btn.pack()

app.mainloop()