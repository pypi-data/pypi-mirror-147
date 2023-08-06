from distutils.core import setup

setup(
    name='baizhanSuperMath123', # 对外我们模块的名字
    version='1.0', # 版本号
    description='这是第一个对外发布的模块，里面只有数学方法，只用于测试哦', #描述
    author='louhergetup', # 作者
    author_email='louhergetup@163.com',
    py_modules=['baizhanSuperMath123.demo1','baizhanSuperMath123.demo2'] # 要发布的模块
)