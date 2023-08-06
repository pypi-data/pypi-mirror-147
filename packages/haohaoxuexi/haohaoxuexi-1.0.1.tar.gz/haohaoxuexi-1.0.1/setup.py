from distutils.core import setup
setup(
    name='haohaoxuexi',    #模块名称
    version='1.0.1',    #版本号
    #描述
    # description='这是第一个版本，仅用于测试',
    description="v1.0.1 加入tk模块(tkinter组件编写实例)",
    author='zqd',
    author_email='',
    #要发布的模块
    py_modules=['haohaoxuexi.demo1','haohaoxuexi.demo2',
        'haohaoxuexi.tk.tk','haohaoxuexi.tk.test'
    ]
    
)