'''
【实例】画图软件项目
'''
from tkinter import *
from tkinter.colorchooser import *      #选择背景色
from tkinter.filedialog import *        #文件对话框


# 画布大小
canvas_width=600
canvas_height=400


class Application(Frame):
    '''Application类文档说明：'''
    def __init__(self,master=None,bgcolor="#000000"):
        super().__init__(master)
        self.master=master
        self.bgcolor=bgcolor
        self.fgcolor="blue"
        self.x=0
        self.y=0
        self.lastDraw=0     #表示最后绘制的图形
        self.startDrawFlag=False
        self.pack()
        self.creatWigidget()
        
    
    #----------------------------<creatWigidget> start----------------------------#
    def creatWigidget(self):
        #创建绘图区域
        self.drawPad=Canvas(root,width=canvas_width,height=canvas_height*0.9,bg=self.bgcolor)
        self.drawPad.pack()
        
        #创建按钮
        btn_start=Button(root,text="开始",name="start")
        btn_start.pack(side="left",padx="10")
        btn_pen=Button(root,text="画笔",name="pen")
        btn_pen.pack(side="left",padx="10")
        btn_rect=Button(root,text="矩形",name="rect")
        btn_rect.pack(side="left",padx="10")
        btn_clear=Button(root,text="清屏",name="clear")
        btn_clear.pack(side="left",padx="10")
        btn_eraser=Button(root,text="橡皮擦",name="eraser")
        btn_eraser.pack(side="left",padx="10")
        btn_line=Button(root,text="直线",name="line")
        btn_line.pack(side="left",padx="10")
        btn_lineArrow=Button(root,text="箭头直线",name="lineArrow")
        btn_lineArrow.pack(side="left",padx="10")
        btn_color=Button(root,text="颜色",name="color")
        btn_color.pack(side="left",padx="10")
        
        #事件处理
        btn_pen.bind_class("Button","<1>",self.eventManager)
        self.drawPad.bind("<ButtonRelease-1>",self.stopDraw)
        
        #增加颜色切换快捷键处理
        root.bind("<KeyPress-r>",self.hotkey)
        root.bind("<KeyPress-g>",self.hotkey)
        root.bind("<KeyPress-y>",self.hotkey)
    
    def eventManager(self,event):
        name=event.widget.winfo_name()
        print(name)
        if name=="line":
            self.drawPad.bind("<B1-Motion>",self.myline)
        elif name=="lineArrow":
            self.drawPad.bind("<B1-Motion>",self.mylineArrow)
        elif name=="rect":
            self.drawPad.bind("<B1-Motion>",self.myRect)    
        elif name=="pen":
            self.drawPad.bind("<B1-Motion>",self.myPen)    
        elif name=="eraser":
            self.drawPad.bind("<B1-Motion>",self.myEraser) 
        elif name=="clear":
            self.drawPad.delete("all")   #清屏
        elif name=="color":
            #颜色
            c=askcolor(color=self.fgcolor,title="选择画笔颜色")
            self.fgcolor=c[1]
      
    def stopDraw(self,event):
        # print("stopDraw")
        self.startDrawFlag=False
        self.lastDraw=0
        
    def myline(self,event): 
        '''
        仅参考
        '''
        self.drawPad.delete(self.lastDraw)      #只保留最近绘制的一条线段
        if not self.startDrawFlag:
            self.startDrawFlag=True
            self.x=event.x
            self.y=event.y
        else:
            self.lastDraw=self.drawPad.create_line(self.x,self.y,event.x,event.y,fill=self.fgcolor)
    
    def startDraw(self,event):
        self.drawPad.delete(self.lastDraw)      #只保留最近绘制的一条线段
        if not self.startDrawFlag:
            self.startDrawFlag=True
            self.x=event.x
            self.y=event.y    
    def myline(self,event): 
        self.startDraw(event)
        self.lastDraw=self.drawPad.create_line(self.x,self.y,event.x,event.y,fill=self.fgcolor)
    
    def mylineArrow(self,event): 
        self.startDraw(event)
        self.lastDraw=self.drawPad.create_line(self.x,self.y,event.x,event.y,
            arrow=LAST,
            fill=self.fgcolor,
        )
        
    def myRect(self,event): 
        self.startDraw(event)
        self.lastDraw=self.drawPad.create_rectangle(self.x,self.y,event.x,event.y,
            fill=self.fgcolor,
        )
        
    def myPen(self,event): 
        # print("#----------myPen----------------#")
        # print("self.fgcolor",self.fgcolor)
        self.startDraw(event)
        self.drawPad.create_line(self.x,self.y,event.x,event.y,
            fill=self.fgcolor,
        )
        self.x=event.x
        self.y=event.y
    
    def myEraser(self,event): 
        self.startDraw(event)
        self.drawPad.create_rectangle(event.x-4,event.y-4,event.x+4,event.y+4,
            fill=self.bgcolor,
        )
        
    def myColor(self,event): 
        self.startDraw(event)
        self.drawPad.create_rectangle(event.x-4,event.y-4,event.x+4,event.y+4,
            fill=self.bgcolor,
        )
     
    #快捷键
    def hotkey(self,event): 
        # print("#----------hotkey----------------#")
        # print(event.char=="g")      #True
        # print(event.char=='g')      #True
        if event.char=='r':
            self.fgcolor="#ff0000"
        elif event.char=='g':
            self.fgcolor="green"
        elif event.char=='y':
            self.fgcolor="#ffff00"
        # print("self.fgcolor",self.fgcolor)

    #----------------------------<creatWigidget> end----------------------------#
    

    




if __name__=="__main__":
    root=Tk()
    root.geometry("{0}x{1}+{2}+{3}".format(canvas_width,canvas_height,400,100))        #窗口大小、左上角位置
    root.title("绘图项目")     #窗口标题
    root["bg"]="white"        #背景色
    
    app=Application(master=root)
    
    



    root.mainloop()


