from setuptools import setup, find_packages

setup(name='zhongtukexin_test',
      version='0.0.1',
      description='zhongtukexin_test atttributes and functions',
      author='ln',
      author_email='1203988597@qq.com',
      requires=['json'],  # 定义依赖哪些模块
      packages=find_packages(),  # 系统自动从当前目录开始找包
      # 如果有的文件不用打包，则只能指定需要打包的文件
      # packages=['代码1','代码2','__init__']  #指定目录中需要打包的py文件，注意不要.py后缀
      )
