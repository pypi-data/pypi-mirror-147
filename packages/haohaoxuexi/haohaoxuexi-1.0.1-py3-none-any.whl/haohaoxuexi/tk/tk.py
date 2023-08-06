'''
使用面向对象方式，测试GUI程序写法
'''

from tkinter import *
from tkinter import messagebox
import webbrowser
import random
from tkinter.colorchooser import *      #选择背景色
from tkinter.filedialog import *        #文件对话框
from tkinter.simpledialog import *      #简单对话框

#通用消息框
# from tkinter import__*
from tkinter.messagebox import *        #通用消息框

root=Tk()
root.geometry("600x600+200+200")        #窗口大小、左上角位置
root.title("GUI测试")     #窗口标题
# root["bg"]="white"        #背景色

class Application(Frame):
    '''Application类文档说明：'''
    def __init__(self,master=None):
        pass
        super().__init__(master)
        # self.master=master
        self.pack()
        
    
    #----------------------------<creatWigidget> start----------------------------#
    def creatWigidget(self):
        '''创建组件'''
        self.btn01=Button(self)
        self.btn01["text"]="抢白菜啦！"
        self.btn01.pack()
        self.btn01["command"]=self.fun_btn01
        
        #创建一个退出程序的按钮
        self.btnQuit=Button(self,text="退出",command=root.destroy)
        self.btnQuit.pack()
    def fun_btn01(e):   #e是事件的对象
        messagebox.showinfo("通知","好白菜被猪拱完了！")
        print("好白菜被猪拱完了！")    
    #----------------------------<creatWigidget> end----------------------------#
    
    
    #----------------------------<creatLabel> start----------------------------#
    def creatLabel(self):
        '''创建Label组件'''
        self.label01=Label(self,
            text="20220414abcdefgggggg",
            font=("黑体",14),   #字体
            # justify="right",    #右对齐(参数无效)
            width=10,
            height=3,
            bg="black",     #背景色
            fg="white"      #前景色
            )
        self.label01.pack()
        
        #显示图像
        global photo    #全局变量，局部变量无法显示图片(方法执行完后，对象被销毁，图片无法显示)
        photo=PhotoImage(file="./logo.gif")
        self.label02=Label(self,
            image=photo,
            width=100,
            height=100
        )
        self.label02.pack()
        
        #多行文本
        str='''我的日记本\n今天天气不错\n昨天阴天\n前天下大雨\n--20220415'''
        self.label03=Label(self,
            text=str,
            font=("黑体",14),   #字体
            borderwidth=1,
            relief="solid",     #边框3D效果
            justify="right",    #多行文字：右对齐
            width=15,
            height=6,
            bg="gray",     #背景色
            fg="blue"      #前景色
            )
        self.label03.pack()
    #----------------------------<creatLabel> end----------------------------#
        
    
    #----------------------------<creatButton_login> start----------------------------#
    def creatButton_login(self):
        #文字按钮
        self.btn01=Button(root,
            text="登录",
            width=6,
            height=3,
            anchor="e",
            command=self.login
        )
        self.btn01.pack()
        # self.btn01.config(state="disabled")    #设置按钮为禁用
        
        #图像按钮
        global photo    #全局变量，局部变量无法显示图片(方法执行完后，对象被销毁，图片无法显示)
        photo=PhotoImage(file="./logo.gif")
        self.btn02=Button(root,
            image=photo,
            width=40,
            height=20,
            command=self.login
        )
        self.btn02.pack()
    def login(self):
        messagebox.showinfo("info","登录成功")
    #----------------------------<creatButton_login> end----------------------------#
    
    #----------------------------<createEntry_login> start----------------------------#    
    def createEntry_login(self):
        """创建用户名、密码登录界面，测试单行文本框(Entry)使用"""
        self.label01=Label(self,text="用户名")
        self.label01.pack()
        
        #----用户名
        #StringVar变量绑定到指定的组件；StringVar变量发生变化，组件内容也变化；组件内容变化，StringVar变量也发生变化。
        str1=StringVar()
        self.entry01=Entry(self,
            textvariable=str1
        )
        self.entry01.pack()
        
        #设置输入框默认值，即StringVar值
        str1.set("admin")   
        #获取输入框内容
        print(str1.get())
        print(self.entry01.get())
        
        #----密码
        self.label02=Label(self,text="密码")
        self.label02.pack()
        
        str2=StringVar()
        self.entry02=Entry(self,
            textvariable=str2,
            show="*"        #加密显示
        )
        self.entry02.pack()
        #设置输入框默认值，即StringVar值
        str2.set("123456")  
        
        
        #----登录
        Button(self,text="登录",command=self.login2).pack()
    def login2(self):
        username=self.entry01.get()
        passwd=self.entry02.get()
        s="输入的用户名：{}，密码：{}".format(username,passwd)
        print(s)
        if username=="admin" and passwd=="123456":
            messagebox.showinfo("info","登录成功！")
        else:
            messagebox.showinfo("info","登录失败，用户名或密码输入错误！")
    #----------------------------<createEntry_login> end----------------------------#
    
    #----------------------------<createText> start----------------------------#
    def createText(self):
        """Text多行文本框_复杂tag标记"""
        self.t1=Text(root,width=40,height=12,bg="gray")
        self.t1.pack()
    
        self.t1.insert(1.0,"0123456789\nabcdefg")       #第一行第0列（行从1开始计数，列从0开始计数）
        self.t1.insert(2.3,"锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦\n")
        
        Button(self,text="重复插入文本",command=self.insertText).pack(side="left")  #side="left" 按钮左对齐，不写就垂直排列
        Button(self,text="返回文本",command=self.returnText).pack(side="left")
        Button(self,text="添加图片",command=self.addImage).pack(side="left")
        Button(self,text="添加组件",command=self.addWidget).pack(side="left")
        Button(self,text="通过tag精确控制文本",command=self.testTag).pack(side="left")
    #----------------------------<createText> end----------------------------#
    
    #----------------------------<createRadioButton> start----------------------------#
    def createRadioButton(self):
        """单选按钮：RadioButton"""
        self.var=StringVar();
        self.var.set("F")   #设置变量值
        
        self.r1=Radiobutton(self,text="男性",value="M",variable=self.var)
        self.r2=Radiobutton(self,text="女性",value="F",variable=self.var)
        self.r1.pack(side="left")   #左右放置
        self.r2.pack(side="left")
        
        Button(self,text="确定",command=self.confirm).pack(side="left")
    
    
    def insertText(self):
        #INSERT索引表示在光标处插入
        self.t1.insert(INSERT,"AAAA")
        #END索引表示在最后插入
        self.t1.insert(END,"【ZZZ】")
    
    
    def returnText(self):
        print(self.t1.get(1.0,1.5))   #获取区域内的文本
        # print(self.t1.get(1.0,END))   #获取区域内的文本
    
    
    def addImage(self):
        self.photo=PhotoImage(file="./logo.gif",
            width=60,
            height=60
        )
        self.t1.image_create(END,image=self.photo)
    
    
    def addWidget(self):
        b1=Button(self.t1,text="点击")
        self.t1.window_create(INSERT,window=b1)
    
    
    def testTag(self):
        self.t1.delete(1.0,END)     #删除所有内容
        str1='''good good study,day day up!\n好好学习\n天天向上\n百度一下，你就知道!'''
        self.t1.insert(INSERT,str1)     #从光标处插入文本
        
        self.t1.tag_add("good",1.0,1.9)                         #指定tag名称，和起始位置
        self.t1.tag_config("good",background="yellow",foreground="red")     #对tag做处理
        
        self.t1.tag_add("baidu",4.0,4.2)                        #指定tag名称，和起始位置
        self.t1.tag_config("baidu",underline=True)              #对tag做处理：加下划线
        self.t1.tag_bind("baidu","<Button-1>",self.webshow)     #对tag做处理：加网络链接
    
    
    def webshow(self,event):
        webbrowser.open("http://www.baidu.com")
        
        
    def confirm(self):
        messagebox.showinfo("info","选择的性别："+self.var.get()) #get获取变量值
    #----------------------------<createRadioButton> end----------------------------#
    
    #----------------------------<createCheckButton> start----------------------------#
    def createCheckButton(self):
        self.var1=IntVar()
        self.var2=IntVar()
        print(self.var1.get())  #默认值是0
        
        self.c1=Checkbutton(self,text="打球",variable=self.var1,onvalue=1,offvalue=0)
        self.c2=Checkbutton(self,text="写作业",variable=self.var2,onvalue=1,offvalue=0)
        self.c1.pack(side="left")
        self.c2.pack(side="left")
        
        Button(self,text="确定",command=self.confirm).pack(side="left")
    def confirm(self):
        if self.var1.get()==1:
            messagebox.showinfo("info","想去打球了") 
        if self.var2.get()==1:
            messagebox.showinfo("info","该去写作业了") 
   
    #----------------------------<createCheckButton> end----------------------------#
    
    #----------------------------<createCanvas> start----------------------------#
    def createCanvas(self):
        '''Canvas画布组件'''
        self.canvas=Canvas(self,width=300,height=200,bg="green")
        self.canvas.pack()
        
        line=self.canvas.create_line(10,10,30,20,40,50) #画直线(10,10),(30,20),(40,50)
        rect=self.canvas.create_rectangle(50,50,150,150) #画矩形(50,50),(100,100)
        oval=self.canvas.create_oval(50,50,150,150) #画椭圆(50,50),(100,100)
        
        global photo
        photo=PhotoImage(file="./logo.gif",
            width=60,
            height=60
        )
        self.canvas.create_image(150,170,image=photo)
        
        Button(self,text="画10个矩形",command=self.draw10Rect).pack(side="left")
    def draw10Rect(self):
        for i in range(0,10):
            x1=random.randrange(int(self.canvas["width"])/2)
            y1=random.randrange(int(self.canvas["height"])/2)
            x2=x1+random.randrange(int(self.canvas["width"])/2)
            y2=y1+random.randrange(int(self.canvas["height"])/2)
            self.canvas.create_rectangle(x1,y1,x2,y2)
        
    #----------------------------<createCanvas> end----------------------------#
    
    #----------------------------<createGrid> start----------------------------#
    def createGrid(self):
        '''通过Grid布局实现登录界面'''  
        self.label01=Label(self,text="用户名")
        self.label01.grid(row=0,column=0)
        self.entry01=Entry(self)
        self.entry01.grid(row=0,column=1)
        Label(self,text="用户名为手机号码").grid(row=0,column=2)
        
        Label(self,text="密码").grid(row=1,column=0)
        Entry(self,show="*").grid(row=1,column=1)
        
        Button(self,text="登录").grid(row=2,column=1,sticky=EW)
        Button(self,text="取消").grid(row=2,column=2,sticky=E)
        
    #----------------------------<createGrid> end----------------------------#
    
    #----------------------------<createCalculator> start----------------------------#
    def createCalculator(self):
        '''通过Grid实现计算器软件界面'''  
        btnText=(("MC","M+","M-","MR"),
            ("C","±","/","×"),
            (7,8,9,"-"),
            (4,5,6,"+"),
            (1,2,3,"="),
            (0,"."),
        )
        
        Entry(self).grid(row=0,column=0,columnspan=4,pady=10)
        
        for rindex,r in enumerate(btnText):
            for cindex,c in enumerate(r):
                if c=="=":
                    Button(self,text=c,width=2).grid(row=rindex+1,column=cindex,rowspan=2,sticky=NSEW)
                elif c==0:
                    Button(self,text=c,width=2).grid(row=rindex+1,column=cindex,columnspan=2,sticky=NSEW)
                elif c==".":
                    Button(self,text=c,width=2).grid(row=rindex+1,column=cindex+1,sticky=NSEW)
                else:
                    Button(self,text=c,width=2).grid(row=rindex+1,column=cindex,sticky=NSEW)
        
        
    
    #----------------------------<createCalculator> end----------------------------#
    
    #----------------------------<createPiano> start----------------------------#
    def createPiano(self):
        '''通过pack实现钢琴按键布局'''
        # Frame是一个矩形区域，用来放置其他子组件
        self.f1=Frame(root)
        self.f1.pack()
        self.f2=Frame(root)
        self.f2.pack()
        
        btnText=("流行风","中国凤","日本风","重金属","轻音乐")
        for txt in btnText:
            Button(self.f1,text=txt).pack(side="left",padx="10")
        for i in range(1,20):
            Label(self.f2,
                width=5,
                height=10,
                borderwidth=1,
                relief="solid",
                bg="black" if i %2==0 else "white"       #颜色更迭
            ).pack(
                side="left",
                padx=2      #间距
            )
        
    #----------------------------<createPiano> end----------------------------#
    
    #----------------------------<testPlace> start----------------------------#
    def testPlace(self):
        '''测试Place布局'''

        root["bg"]="white"        #背景色
        
        # Frame是一个矩形区域，用来放置其他子组件
        self.f1=Frame(root,width=200,height=200,bg="green")
        self.f1.place(x=30,y=30)
        
        Button(root,text="按钮1").place(relx=0.2,x=100,y=20,relwidth=0.2,relheight=0.5)
        Button(self.f1,text="按钮2").place(relx=0.6,rely=0.7)
        Button(self.f1,text="按钮3").place(relx=0.5,rely=0.2)

    #----------------------------<testPlace> end----------------------------#
    
    #----------------------------<testPokerGame> start----------------------------#
    def testPokerGame(self):
        '''通过place布局管理器实现扑克牌位置控制'''

        # self.photo=PhotoImage(file="./image/puke_gif/3.gif")
        # self.puke1=Label(root,image=self.photo)
        # self.puke1.place(x=10,y=50)
        
        self.photos=[PhotoImage(file="./image/puke_gif/"+str(i+1)+".gif") for i in range(13)]
        self.pukes=[Label(root,image=self.photos[i]) for i in range(13)]
        for i in range(13):
            self.pukes[i].place(x=10+i*40,y=50)
        
        #为所有的Label增加事件处理
        self.pukes[0].bind_class("Label","<Button-1>",self.pukeOut)     #左键单击事件
    def pukeOut(self,event):
        '''出牌'''
        print(event.widget.winfo_geometry())    #窗口信息
        print(event.widget.winfo_y())       #y坐标
        
        if event.widget.winfo_y()==50:
            event.widget.place(y=30)
        else:
            event.widget.place(y=50)
        
    #----------------------------<testPokerGame> end----------------------------#
    
    #----------------------------<testEvent> start----------------------------#
    def testEvent(self):
        '''鼠标和键盘事件'''

        self.c1=Canvas(root,width=200,height=200,bg="green")
        self.c1.pack()
    
        self.c1.bind("<Button-1>",self.mouseTest)       #左键单击
        self.c1.bind("<B1-Motion>",self.testDrag)       #左键拖动
        root.bind("<KeyPress>",self.testKeyBoard)
        root.bind("<KeyPress-a>",self.press_a_test)
        root.bind("<KeyRelease-a>",self.release_a_test)
    
    
    def mouseTest(self,event):
        print("鼠标左键点击位置(相对父容器)：{0}，{1}".format(event.x,event.y))
        print("鼠标左键点击位置(相对屏幕)：{0}，{1}".format(event.x_root,event.y_root))
        print("事件绑定的组件：{0}".format(event.widget))
    def testDrag(self,event):
        self.c1.create_oval(event.x,event.y,event.x+1,event.y+1)
    def testKeyBoard(self,event):
        print("键的keycode:{0},键的char:{1},键的keysym:{2}".
            format(event.keycode,event.char,event.keysym))
    def press_a_test(self,event): 
        print("press a")
    def release_a_test(self,event): 
        print("release a")
    #----------------------------<testEvent> end----------------------------#
    
    #----------------------------<testLambda> start----------------------------#
    def testLambda(self):
        '''Lambda表达式'''

        Button(root,text="测试1",command=self.mouseTest1).pack(side="left")
        Button(root,text="测试2",
            command=lambda:self.mouseTest2("aaa","bbb")).pack(side="left")
    
    
    def mouseTest1(self):
        print("command方式，简单情况：不涉及event对象，可以使用")
    def mouseTest2(self,a,b):
        print("a={0},b={1}".format(a,b))

    #----------------------------<testLambda> end----------------------------#
    
    #----------------------------<testEventBind> start----------------------------#
    def testEventBind(self):
        '''三种事件绑定'''

        self.b1=Button(root,text="bind()绑定")
        self.b1.pack(side="left")
        #bind方式绑定
        self.b1.bind("<Button-1>",self.event_bind_test1)
        
        #command属性直接绑定事件
        self.b2=Button(root,text="command属性绑定",
                command=lambda:self.event_bind_test2("aaa","bbb")
            )
        self.b2.pack(side="left")
        
        self.b3=Button(root,text="按钮3")
        self.b3.pack(side="left")
        
        #给所有Button按钮都绑定右键单击事件
        self.b3.bind_class("Button","<Button-3>",self.event_bind_test3)
    
    
    def event_bind_test1(self,event):
        print("bind()方式绑定，可以获取event对象")
        print(event.widget)
    def event_bind_test2(self,a,b):
        print("command方式绑定，不能直接获取event对象")
        print("a={0},b={1}".format(a,b))
    def event_bind_test3(self,event):
        print("右键单击事件，绑定给所有按钮")
        print(event.widget)

    #----------------------------<testEventBind> end------------------------------#
    
    #----------------------------<testOptionMenu> start----------------------------#
    def testOptionMenu(self):
        '''测试OptionMenu'''

        self.v=StringVar(root)
        self.v.set("语文")
        option=OptionMenu(root,self.v,"数学","英语","地理","化学【人造酱油】")
        
        option["width"]=10
        option.pack()
        
        Button(root,text="按钮",command=self.testOptionMenu_1).pack(side="left")
        
    def testOptionMenu_1(self):
        print(self.v.get())
        # v.set()       #直接修改optionMenu中选中的值
        

    #----------------------------<testOptionMenu> end------------------------------#
    
    #----------------------------<testScale> start----------------------------#
    def testScale(self):
        '''测试Scale 滚动条'''

        self.s1=Scale(root,
            from_=10,                #起始值
            to=50,                  #终点值
            length=200,             #滚动条宽度
            tickinterval=5,         #标记间隔
            orient=HORIZONTAL,      #水平滚动条，默认垂直滚动条
            command=self.testScale_1     #事件
        )
        self.s1.pack()
        
        self.a=Label(root,
            text="好好学习",
            width=10,
            height=1,
            bg="black",
            fg="white"
        )
        self.a.pack()
        
        
    def testScale_1(self,value):
        print("滑块的值：",value)
        newFont=("宋体",value)
        self.a.config(font=newFont)
        

    #----------------------------<testScale> end------------------------------#
    
    #----------------------------<testBgColor> start----------------------------#
    def testBgColor(self):
        '''选择背景色
           先导入：tkinter.colorchooser
        '''

        Button(root,text="选择背景色",command=self.testBgColor_1).pack()

    def testBgColor_1(self):
        s1=askcolor(color="red",title="选择背景色")
        print(s1)       #((135, 12, 120), '#870c78')
        root.config(bg=s1[1])
        
    #----------------------------<testBgColor> end------------------------------#
    
    #----------------------------<testFileDialog> start----------------------------#
    def testFileDialog(self):
        '''文件对话框获取文件
           先导入tkinter.filedialog
        '''

        Button(root,text="选择编辑的文件",command=self.testFileDialog_1).pack()
        Button(root,text="选择读取的文件",command=self.testFileDialog_2).pack()
        
        self.label=Label(root,width=40,height=3,bg="green")
        self.label.pack()

    def testFileDialog_1(self):
        '''获取文件路径'''
        f=askopenfilename(title="上传文件", #窗口标题
            initialdir="d:",        #初始化目录
            filetypes=[("图片文件",".gif")] #默认打开文件类型
            )
        print(f)        #C:/Users/pursu/Downloads/py/logo.gif
        self.label["text"]=f
        
    def testFileDialog_2(self):
        '''获取文件内容'''
        f=askopenfile(title="上传文件", #窗口标题
            initialdir="d:",        #初始化目录
            filetypes=[("文本文件",".txt")] #默认打开文件类型
            )
        self.label["text"]=f.read()

    #----------------------------<testFileDialog> end------------------------------#
    
    #----------------------------<testSimpleDialog> start----------------------------#
    def testSimpleDialog(self):
        '''简单对话框
           先导入tkinter.simpledialog
        '''

        Button(root,text="年龄多大？",command=self.testSimpleDialog_1).pack()

        self.label=Label(root,width=40,height=3,bg="green")
        self.label.pack()

    def testSimpleDialog_1(self):
        '''事件'''
        a=askinteger(title="输入年龄",
            rompt="请输入年龄",
            initialvalue=18,
            minvalue=1,
            maxvalue=150
        )
        # askstring、askfloat框使用方式一样
        self.label["text"]=a
        


    #----------------------------<testSimpleDialog> end------------------------------#
    
    #----------------------------<testMessagebox> start----------------------------#
    def testMessagebox(self):
        '''通用消息框
            from tkinter.messagebox import *
        '''
        Button(root,text="确定/取消",command=self.testMessagebox_1).pack()
        Button(root,text="Yes/No",command=self.testMessagebox_2).pack()
        Button(root,text="Retry/Cancel",command=self.testMessagebox_3).pack()
        Button(root,text="error",command=self.testMessagebox_4).pack()
        Button(root,text="info",command=self.testMessagebox_5).pack()
        Button(root,text="warning",command=self.testMessagebox_5).pack()
        
        
    def testMessagebox_1(self):
        a=askokcancel(title="窗口标题",
            message="你确定吗？"
        )
        print(a)
    def testMessagebox_2(self):
        a=askquestion(title="窗口标题",
            message="你确定吗？"
        )
        print(a)
    def testMessagebox_3(self):
        a=askretrycancel(title="窗口标题",
            message="你确定吗？"
        )
        print(a)
    def testMessagebox_4(self):
        a=showerror(title="窗口标题",
            message="你确定吗？"
        )
        print(a)
    def testMessagebox_5(self):
        a=showinfo(title="窗口标题",
            message="好好学习\n天天向上\n吃饼干喝奶茶"
            )
        print(a)
    def testMessagebox_6(self):
        a=showwarning(title="窗口标题",
            message="好好学习\n天天向上\n吃饼干喝奶茶"
            )
        print(a)

    #----------------------------<testMessagebox> end------------------------------#
    



    #----------------------------<fun> start----------------------------#
        
    
    #----------------------------<fun> end------------------------------#
'''


'''

if __name__=="__main__":
    # print(random.randrange(20))
    root=Tk()
    root.geometry("600x600+200+200")        #窗口大小、左上角位置
    root.title("GUI测试")     #窗口标题
    root["bg"]="white"        #背景色
    
    app=Application(master=root)
    app.creatWigidget()


    root.mainloop()





































'''
from tkinter import *
from tkinter import messagebox

#-----主窗口对象
root=Tk()
root.title("GUI测试")     #窗口标题
root.geometry("500x300+200+100")         #设置窗口大小:500*300，位置(200,100)



btn01=Button(root)
btn01['text']="抢白菜啦！"
btn01.pack()


def fun_btn01(e):   #e是事件的对象
    messagebox.showinfo("通知","好白菜被猪拱完了！")
    print("好白菜被猪拱完了！")

#----btn01按钮左键(1)绑定事件(fun_btn01)
btn01.bind("<Button-1>",fun_btn01)


#-----进入事件循环，保持主窗口一直显示
root.mainloop()

'''
