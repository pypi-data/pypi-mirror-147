from distutils.core import setup

setup(
    name='super-fast', # 对外我们模块的名字
    version='1.0.1', # 版本号
    description='test', #描述
    author='xuzhongshuai', # 作者
    author_email='2720060895@qq.com',
    py_modules=['fast.fast01','fast.fast02'] # 要发布的模块
)