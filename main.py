#-*- coding:utf-8 -*-

import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import seaborn as sns

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class app(ttk.Frame):
    def __init__(self, master =None): # master : tk.TK classs
        super().__init__(master) # tk.TK class :initialize

        self.MtrLoad = False
        self.rsLoad = False
        self.imgLoad =False

        # window
        self.master.title('Grid2Spec')
        self.master.geometry("1440x720+50+50")
        self.mainframe = ttk.Frame(self.master)

        # widget setting
        pad_x = 10
        pad_y = 10
        self.crrX = tk.DoubleVar()
        self.crrY = tk.DoubleVar()

        self.waveBtn = ttk.Button(self.master, text="Load mtr [.txt]", command=self.loadMtr)
        self.waveBtn.grid(column=0, row = 0,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)
        self.rsBtn = ttk.Button(self.master, text="Load rs [.txt]", command = self.loadRs)
        self.rsBtn.grid(column=0, row = 1,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)

        self.valX = tk.IntVar(value=20)
        self.valY = tk.IntVar(value=20)


        self.Xlabel = ttk.Label(self.master, text = "num X step")
        self.Xlabel.grid(column =0, row =2, sticky=tk.EW ,padx=pad_x, pady = pad_y)
        self.Ylabel = ttk.Label(self.master, text = "num Y step")
        self.Ylabel.grid(column =0, row =3, sticky=tk.EW ,padx=pad_x, pady = pad_y)

        self.Xspnbox = ttk.Spinbox(self.master,textvariable=self.valX, from_=0, to=100, increment=1)
        self.Xspnbox.grid(column =1, row =2, sticky=tk.EW ,padx=pad_x, pady = pad_y)
        self.Yspnbox = ttk.Spinbox(self.master,textvariable=self.valY, from_=0, to=100, increment=1)
        self.Yspnbox.grid(column =1, row =3, sticky=tk.EW ,padx=pad_x, pady = pad_y)

        self.imgBtn = ttk.Button(self.master, text="Load img", command=self.loadImg)
        self.imgBtn.grid(column=0, row = 4,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)
   
        self.setBtn = ttk.Button(self.master, text="Initialize", command=self.init)
        self.setBtn.grid(column=0, row = 5,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)
        self.saveBtn = ttk.Button(self.master, text="Save Current Spectrum",command=self.saveCrrSpec)
        self.saveBtn.grid(column=0, row = 6,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)

        self.buffCanvas = tk.Canvas(self.master, width =100, height=100)
        self.buffCanvas.grid(column=0, row = 7, columnspan=2,sticky=tk.EW ,padx=pad_x, pady = pad_y, ipady=60)

        # Image related
        self.canvasSize = 500
        self.imgCanvas = tk.Canvas(self.master, width=self.canvasSize,height=self.canvasSize,highlightthickness=0)
        self.imgCanvas.create_rectangle(0, 0, self.canvasSize,self.canvasSize, fill = '#DDDDDD')
        self.imgCanvas.grid(column=2, row = 1,rowspan=10,columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S ,padx=pad_x*2, pady = pad_y*2, ipady=30)
        self.imgCanvas.bind('<B1-Motion>', self.pickPos)

        self.crrXlabel = ttk.Label(self.master, text = "current X posision")
        self.crrXlabel.grid(column =2, row =7, sticky=tk.SW ,padx=pad_x*2, pady = pad_y/4)
        self.crrYlabel = ttk.Label(self.master, text = "current Y position")
        self.crrYlabel.grid(column =2, row =8, sticky=tk.NW ,padx=pad_x*2, pady = pad_y/4)

        self.valCrrX = tk.IntVar()
        self.valCrrY = tk.IntVar()
        self.crrXValue = ttk.Label(self.master,textvariable=self.valCrrX)
        self.crrXValue.grid(column =3, row =7, sticky=tk.SW ,padx=1, pady = pad_y/4)
        self.crrYValue = ttk.Label(self.master,textvariable=self.valCrrY)
        self.crrYValue.grid(column =3, row =8, sticky=tk.NW ,padx=1, pady = pad_y/4)


        # Graph related
        sns.set_style(style="darkgrid")
        self.fig = Figure()
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.figCanvas = FigureCanvasTkAgg(self.fig, self.master)
        self.figCanvas.get_tk_widget().grid(column =4, row =1, sticky=tk.NW ,rowspan=7,padx=1, pady = pad_y/4,ipady=30)
        
        #self.naviFrame = ttk.Frame(master = self.mainframe)
        self.figWiToolbar = NavigationToolbar2Tk(self.figCanvas, self.master,pack_toolbar=False)
        self.figWiToolbar.grid(column =4, row =8, sticky=tk.NW ,rowspan=10,padx=1, pady = pad_y/4)
 
    # functions
    def loadImg(self):
        self.imgPath = filedialog.askopenfilename(filetypes=[('','*.png;*.jpg;*.jpeg;*.emf;*.tiff;*.tif')],title = "Choose Image file")
        if(self.imgPath ==''):
            return 0
        #print(self.imgPath)
        self.img_array = np.fromfile(self.imgPath, dtype=np.uint8)
        self.img_ = cv2.imdecode(self.img_array, cv2.IMREAD_COLOR)

        self.imgLoad =True
    
    def loadMtr(self):
        self.mtrPath = filedialog.askopenfilename(filetypes=[('','*.txt')],title = "Choose matrix data file (.txt)")
        if(self.mtrPath ==''):
            return 0
        
        self.Mtr_ = pd.read_table(self.mtrPath, sep="\t", header=None)
        self.Mtr = np.array(self.Mtr_)
        self.Mtr_row, self.Mtr_col  = self.Mtr.shape

        self.MtrLoad=True

    def loadRs(self):
        self.rsPath = filedialog.askopenfilename(filetypes=[('','*.txt')],title = "Choose raman shift data file (.txt)")
        if(self.rsPath ==''):
            return 0
        
        self.rs_ = pd.read_table(self.rsPath, sep="\t", header=None)
        self.rs = np.array(self.rs_)
        self.rs_row, self.rs_col  = self.rs.shape
        if(self.rs_col >1):
            print("Bad data format for raman shift: > 1 size of column ... ")
            return -1
        
        self.rs = np.ravel(self.rs)
        self.rsLoad=True

    # initialize 
    def init(self):
        self.getXYGrid()
        if (self.checkValid_onInit()==-1):
            return -1
        
        self.imgSet()
        self.ax.plot(self.rs, self.Mtr[:,0],linewidth=0.5)
        self.ax.set_xlabel("Raman shift [cm-1]")
        self.ax.set_ylabel(" a. u.")
        self.figCanvas.draw()
    
    def getXYGrid(self):
        self.xGrid = int(self.Xspnbox.get())
        self.yGrid = int(self.Yspnbox.get())

    def checkValid_onInit(self): # confirm data validity
        #data load
        if((self.MtrLoad is False) or (self.rsLoad is False)):
            print("Spectral data is insufficient ...")
            return -1

        if(self.imgLoad is False):
            print("Image data is not loaded ...")
            return -1
        #size consistency
        if(self.xGrid * self.yGrid != self.Mtr.shape[1]):
            print("Set grid does not match the data size ...")
            return -1
        

    def imgResize(self): # img :image attribute
        self.imgResize = self.img_.copy()
        self.crrImgX = self.img_.shape[0]
        self.crrImgY = self.img_.shape[1]
        #print(self.imgResize.shape)

        if(self.crrImgX <= self.crrImgY):
            self.imgResize=cv2.resize(self.imgResize, dsize=None, fx = self.canvasSize/self.crrImgY, fy =self.canvasSize/self.crrImgY )
        else:
            self.imgResize=cv2.resize(self.imgResize, dsize=None, fx = self.canvasSize/self.crrImgX, fy =self.canvasSize/self.crrImgX )
        
        self.ResImgSizeY, self.ResImgSizeX, = self.imgResize.shape[:2]

        self.img = cv2.cvtColor(self.imgResize, cv2.COLOR_BGR2RGB)
        self.img_pil = Image.fromarray(self.img) 
        self.img_tk  = ImageTk.PhotoImage(self.img_pil) 

        return 0
    
    def addGrid2Img(self):
        self.xStp = self.ResImgSizeX /int(self.xGrid)
        self.yStp = self.ResImgSizeY /int(self.yGrid)
        #print(self.xStp)
        for x in range(self.xGrid+1):
            self.imgCanvas.create_line( x * self.xStp, 0,x * self.xStp ,self.ResImgSizeY)
        for y in range(self.yGrid+1):
            self.imgCanvas.create_line( 0, y * self.yStp, self.ResImgSizeX,y * self.yStp)
    
    def imgSet(self):
        self.imgResize()
        self.imgCanvas.create_image(0, 0, image=self.img_tk, anchor='nw') # ImageTk
        self.addGrid2Img()
   
    def pickPos(self,event):
        self.prevX = self.crrX ## for line move
        self.prevY = self.crrY

        self.crrX = event.x
        self.crrY = event.y
        # fix position if exceed the boundary

        if(self.crrX >=self.ResImgSizeX):
            self.crrX = self.ResImgSizeX-0.01
        if(self.crrY >=self.ResImgSizeY):
            self.crrY = self.ResImgSizeY-0.01
        if(self.crrX <0):
            self.crrX = 0
        if(self.crrY <0):
            self.crrY = 0

        self.calcGridPos()
        self.updateGraph()
        self.moveCursor()

    def moveCursor(self):

        if((hasattr(self,"lineX")==False) and (hasattr(self,"lineX")==False)):
            self.lineX = self.imgCanvas.create_line( 0, self.crrY,      self.ResImgSizeX, self.crrY, tag = "lineX", fill="#3BAF75") # hirizontal
            self.lineY = self.imgCanvas.create_line( self.crrX,0,       self.crrX ,self.ResImgSizeX, tag = "lineY", fill="#3BAF75") # vertical
        else:
            self.imgCanvas.move(self.lineX, 0, self.crrY- self.prevY)
            self.imgCanvas.move(self.lineY, self.crrX- self.prevX, 0)
   
    def calcGridPos(self):
        self.crrGridX = int(self.crrX // self.xStp)
        self.crrGridY = int(self.crrY // self.yStp)     
        self.valCrrX.set(self.crrGridX)
        self.valCrrY.set(self.crrGridY)
    
    def updateGraph(self):
        self.wvIdx = self.crrGridY*int(self.xGrid) + self.crrGridX

        self.crrSpec = self.Mtr[:,self.wvIdx].copy()
        self.ax.cla()
        self.ax.plot(self.rs, self.crrSpec, linewidth=0.5)
        self.ax.set_xlabel("Raman shift [cm-1]")
        self.ax.set_ylabel(" a. u.")
        self.figCanvas.draw()
    
    def saveCrrSpec(self):
        self.MtrFileName = self.mtrPath[self.mtrPath.rfind('/')+1:]
        self.svFileName = self.MtrFileName[:-4]+"_X"+str(self.crrGridX)+"Y"+str(self.crrGridY)+".txt"

        to_save = pd.DataFrame(self.crrSpec)
        to_save = to_save.rename(columns={to_save.columns[0] :self.svFileName[:-4] })
        to_save.to_csv(self.svFileName,index=False, header=self.svFileName[:-4], sep='\t')
        
        print(f"Spectrum {self.svFileName} is saved.")


if __name__ == "__main__":
    main_wn = tk.Tk()
    Application = app(master = main_wn)
    Application.mainloop()
    