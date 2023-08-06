'''
本地发布：
python setup.py sdist
本地安装：
python setup.py install
安装到 python主目录\Lib\site-packages
使用：
import haohaoxuexi.demo1
haohaoxuexi.demo1.get_cwd()


发布到官网
1.构建源码包，前提：pip install build
python -m build
2.上传项目，前提：pip install twine
twine upload dist/*
3.下载使用
pip install package-name
4.更新包
pip install package-name update


使用：
from haohaoxuexi.tk.tk import *
app=Application(master=root)
app.testMessagebox()
root.mainloop()


'''

'''
v1.0.1	加入tk模块 tkinter组件编写实例


'''

from tk import *
if __name__=="__main__":


    # root=Tk()
    # root.geometry("600x600+200+200")        #窗口大小、左上角位置
    # root.title("GUI测试")     #窗口标题
    # root["bg"]="white"        #背景色
    
    
    app=Application(master=root)
    
    
    # app.creatWigidget()
    # app.creatLabel()
    # app.creatButton_login()
    # app.createEntry_login()
    
    #----Text多行文本框_复杂tag标记
    # app.createText()
    
    #----单选按钮：RadioButton
    # app.createRadioButton()
    #----多按钮：CheckButton
    # app.createCheckButton()
    
    
    #----Canvas画布组件
    # app.createCanvas()
    
    #----通过Grid布局实现登录界面
    # app.createGrid()
    #----通过Grid实现计算器软件界面
    # app.createCalculator()
    #----通过pack实现钢琴按键布局
    # app.createPiano()
    #----测试Place布局
    # app.testPlace()
    #----通过place布局管理器实现扑克牌位置控制
    # app.testPokerGame()
    #----鼠标和键盘事件
    # app.testEvent()
    #----Lambda表达式
    # app.testLambda()
    #----三种事件绑定
    # app.testEventBind()
    #----测试OptionMenu
    # app.testOptionMenu()
    #----测试Scale 滚动条
    # app.testScale()
    #----选择背景色
    # app.testBgColor()
    #----文件对话框获取文件
    # app.testFileDialog()
    #----简单对话框
    # app.testSimpleDialog()
    #----通用消息框
    app.testMessagebox()
    
    








 
    root.mainloop()









