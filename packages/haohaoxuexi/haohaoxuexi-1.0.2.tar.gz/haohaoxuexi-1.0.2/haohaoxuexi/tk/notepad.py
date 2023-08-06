'''
【实例】记事本项目
'''
from tkinter import *
from tkinter.colorchooser import *      #选择背景色
from tkinter.filedialog import *        #文件对话框



class Application(Frame):
    '''Application类文档说明：'''
    def __init__(self,master=None):
        super().__init__(master)
        self.master=master
        self.textpad=None
        self.pack()
        self.creatWigidget()
        
    
    #----------------------------<creatWigidget> start----------------------------#
    def creatWigidget(self):
        # 创建主菜单
        menubar=Menu(root)
        
        # 创建子菜单
        menuFile=Menu(menubar)
        menuEdit=Menu(menubar)
        menuHelp=Menu(menubar)
        
        #将子菜单加入到主菜单栏
        menubar.add_cascade(label="文件(F)",menu=menuFile)
        menubar.add_cascade(label="编辑(E)",menu=menuEdit)
        menubar.add_cascade(label="帮助(H)",menu=menuHelp)
        
        # 添加菜单项
        menuFile.add_command(label="新建",accelerator="ctrl+n",command=self.newFile)
        menuFile.add_command(label="打开",accelerator="ctrl+o",command=self.openFile)
        menuFile.add_command(label="保存",accelerator="ctrl+s",command=self.saveFile)
        menuFile.add_separator()        #添加分割线
        menuFile.add_command(label="退出",accelerator="ctrl+q",command=self.exit)
        
        #将主菜单添加到根窗口
        root["menu"]=menubar
        
        # 增加快捷键
        root.bind("<Control-n>",lambda event:self.newFile())
        root.bind("<Control-o>",lambda event:self.openFile())
        root.bind("<Control-s>",lambda event:self.saveFile())
        root.bind("<Control-q>",lambda event:self.exit())
        
        #文本编辑区
        self.textpad=Text(root,width=30,height=10)
        self.textpad.pack()
        
        #创建上下菜单(即鼠标右键菜单)
        self.contextMenu=Menu(root)
        self.contextMenu.add_command(label="背景颜色",command=self.openAskColor)
        
        #右键绑定事件
        root.bind("<Button-3>",self.createContextMenu)
        
        
        
    def test(self):   #e是事件的对象
        
        print("好白菜被猪拱完了！")   
    def createContextMenu(self,event):   #e是事件的对象
        # 在鼠标位置处显示
        self.contextMenu.post(event.x_root,event.y_root)  
    #----------------------------<creatWigidget> end----------------------------#
    
    #----------------------------<事件> start----------------------------#
    def newFile(self):
        '''备注：方法调试失败'''
        self.filename=asksaveasfilename(title="另存为",
            defaultextention=".txt",
            filetypes=[("文本文件","*.txt")],
            initialdir="d:",
            initialfile="未命名.txt",
        )
        self.saveFile()
    def openFile(self):
        self.textpad.delete("1.0","end")        #清空内容
        with askopenfile(title="打开文本文件") as f:
            # print(f.read())
            self.textpad.insert(INSERT,f.read())
            self.filename=f.name
            
    
    def saveFile(self):
        with open(self.filename,"w",encoding="utf-8") as f:
           c=self.textpad.get(1.0,END)
           f.write(c)
    def exit(self):
        root.quit()
    def openAskColor(self):
        s1=askcolor(color="red",title="选择背景色")
        self.textpad.config(bg=s1[1])
    
    #----------------------------<事件> end----------------------------#
    
    




if __name__=="__main__":
    root=Tk()
    root.geometry("600x600+200+200")        #窗口大小、左上角位置
    root.title("记事本项目")     #窗口标题
    root["bg"]="white"        #背景色
    
    app=Application(master=root)
    



    root.mainloop()


