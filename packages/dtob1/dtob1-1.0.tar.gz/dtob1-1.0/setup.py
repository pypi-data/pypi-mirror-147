from distutils.core import setup

setup(
    name='dtob1',                #发布的模块名
    version='1.0',              #版本号
    description='这是一个十进制数转换成二进制数的模块',#描述
    author='王老师',            #作者
    author_email='wang@sju.edu.cn',
    py_modules=[ 'dtob1.file_tobin','dtob1.file_tohex']    #要发布的模块
)
