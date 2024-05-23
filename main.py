#%%
import cv2
import numpy as np
import pandas as pd
from PIL import Image, ImageTk


import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class app(ttk.Frame):
    def __init__(self, master =None): # master : tk.TK class
        super().__init__(master) # tk.TK classでinitialize

        self.master.title('Grid2Spec')
        self.master.geometry("1440x720+50+50")
        self.mainframe = ttk.Frame(self.master)

        pad_x = 10
        pad_y = 10
        self.crrX = tk.DoubleVar()
        self.crrY = tk.DoubleVar()

        self.waveBtn = ttk.Button(self.master, text="Load mtr [.csv]", command=self.loadMtr)
        self.waveBtn.grid(column=0, row = 0,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)
        self.rsBtn = ttk.Button(self.master, text="Load rs [.csv]", command = self.loadRs)
        self.rsBtn.grid(column=0, row = 1,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)

        self.valX = tk.IntVar()
        self.valX.set(15)
        self.valY = tk.IntVar(value=15)
        self.valY.set(15)

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
        self.saveBtn = ttk.Button(self.master, text="Save Current Spectrum")
        self.saveBtn.grid(column=0, row = 6,columnspan=2, sticky=tk.EW ,padx=pad_x, pady = pad_y)

        self.buffCanvas = tk.Canvas(self.master, width =100, height=100)
        self.buffCanvas.grid(column=0, row = 7, columnspan=2,sticky=tk.EW ,padx=pad_x, pady = pad_y, ipady=60)

        self.canvasSize = 540
        self.imgCanvas = tk.Canvas(self.master, width=self.canvasSize,height=self.canvasSize )
        self.imgCanvas.create_rectangle(0, 0, self.canvasSize,self.canvasSize, fill = 'green')
        self.imgCanvas.grid(column=2, row = 1,rowspan=10,columnspan=2, sticky=tk.W+tk.E+tk.N+tk.S ,padx=pad_x*2, pady = pad_y*2, ipady=50)
        self.imgCanvas.bind('<B1-Motion>', self.pickPos)

        self.crrXlabel = ttk.Label(self.master, text = "current X posision")
        self.crrXlabel.grid(column =2, row =7, sticky=tk.SW ,padx=pad_x+2, pady = pad_y/4)
        self.crrYlabel = ttk.Label(self.master, text = "current Y position")
        self.crrYlabel.grid(column =2, row =8, sticky=tk.NW ,padx=pad_x+2, pady = pad_y/4)

        self.valCrrX = tk.IntVar()
        self.valCrrY = tk.IntVar()
        self.crrXValue = ttk.Label(self.master,textvariable=self.valCrrX)
        self.crrXValue.grid(column =3, row =7, sticky=tk.SW ,padx=1, pady = pad_y/4)
        self.crrYValue = ttk.Label(self.master,textvariable=self.valCrrY)
        self.crrYValue.grid(column =3, row =8, sticky=tk.NW ,padx=1, pady = pad_y/4)


        # functions
    def loadImg(self):
        self.imgPath = filedialog.askopenfilename(filetypes=[('','*.png;*.jpg;*.jpeg;*.emf;*.tiff')],title = "Choose Image file")
        if(self.imgPath ==''):
            return 0
        
        print(self.imgPath)
        self.img_array = np.fromfile(self.imgPath, dtype=np.uint8)
        self.img_ = cv2.imdecode(self.img_array, cv2.IMREAD_COLOR)
        print(self.img_)
        print(self.img_.shape)

        return 0
    
    def loadMtr(self):
        self.mtrPath = filedialog.askopenfilename(filetypes=[('','*.csv')],title = "Choose matrix data file (.csv)")
        if(self.mtrPath ==''):
            return 0
        self.Mtr = pd.read_csv(self.mtrPath)
    def loadRs(self):
        self.rsPath = filedialog.askopenfilename(filetypes=[('','*.csv')],title = "Choose raman shift data file (.csv)")
        if(self.rsPath ==''):
            return 0
        self.rs = pd.read_csv(self.rsPath)
    
    def getXYGrid(self):
        self.xGrid = int(self.Xspnbox.get())
        self.yGrid = int(self.Yspnbox.get())

        print(self.xGrid)  
        print(self.yGrid)   
    

    def checkValid_onInit(self): # confirm data validity
        # data load
        # if(self.Mtr ==None or self.rs==None):
        #     print("Spectral data is insufficient ...")
        #     return -1

        if(self.img_ ==None):
            print("Image data is not loaded ...")
            return -1
        
        else:
            return 0
        # grid size
        if(self.xGrid ==0 and self.yGrid==0):
            print("0x0 Grid is not permitted ...")
            return -1
        # size consistency


    def imgResize(self): # img :image attribute
        self.imgResize = self.img_.copy()
        self.crrImgX = self.img_.shape[0]
        self.crrImgY = self.img_.shape[1]
        print(self.imgResize.shape)

        if(self.crrImgX <= self.crrImgY):
            self.imgResize=cv2.resize(self.imgResize, dsize=None, fx = self.canvasSize/self.crrImgY, fy =self.canvasSize/self.crrImgY )
        else:
            self.imgResize=cv2.resize(self.imgResize, dsize=None, fx = self.canvasSize/self.crrImgX, fy =self.canvasSize/self.crrImgX )
        
        print(self.imgResize.shape)
        self.ResImgSizeX, self.ResImgSizeY, = self.imgResize.shape[:2]
        self.img = cv2.cvtColor(self.imgResize, cv2.COLOR_BGR2RGB)
        self.img_pil = Image.fromarray(self.img) # RGBからPILフォーマットへ変換
        self.img_tk  = ImageTk.PhotoImage(self.img_pil) # ImageTkフォーマットへ変換

        return 0
    
    def addGrid2Img(self):
        self.xStp = self.ResImgSizeX /int(self.xGrid)
        self.yStp = self.ResImgSizeY /int(self.yGrid)
        print(self.xStp)


        for x in range(self.xGrid+1):
            self.imgCanvas.create_line( x * self.xStp, 0,x * self.xStp ,self.ResImgSizeY, width=0.01)
        for y in range(self.yGrid+1):
            self.imgCanvas.create_line( 0, y * self.yStp, self.ResImgSizeX,y * self.yStp, width=0.1)
    
    def imgSet(self):
        self.getXYGrid()
        self.imgResize()
        self.imgCanvas.create_image(0, 0, image=self.img_tk, anchor='nw') # ImageTk 画像配置
        self.addGrid2Img()

    

    def init(self):
        self.checkValid_onInit()
        self.imgSet()

    
    def pickPos(self,event):
        self.crrX = event.x
        self.crrY = event.y
        if(self.crrX >=self.ResImgSizeX):
            self.crrX = self.ResImgSizeX-0.01
        if(self.crrY >=self.ResImgSizeY):
            self.crrY = self.ResImgSizeY-0.01
        if(self.crrX <0):
            self.crrX = 0
        if(self.crrY <0):
            self.crrY = 0
        self.calcGridPos()
    
    def calcGridPos(self):
        self.crrGridX = int(self.crrX // self.xStp)
        self.crrGridY = int(self.crrY // self.yStp)     
        self.valCrrX.set(self.crrGridX)
        self.valCrrY.set(self.crrGridY)
        print(self.crrGridX)
        print(self.crrGridY)





if __name__ == "__main__":
    main_wn = tk.Tk()
    Application = app(master = main_wn)
    Application.mainloop()
    
#%%