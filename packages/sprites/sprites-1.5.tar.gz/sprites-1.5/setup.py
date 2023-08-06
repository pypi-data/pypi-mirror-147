﻿from setuptools import setup,find_packages

with open("README.md", encoding='utf-8') as fh:
    long_d = fh.read()


setup(name='sprites',
      long_description_content_type="text/markdown",
      version = '1.5',
      description = 'Python Sprites Module for make introductory animations and games and educational purpose。It mainly provides Sprite class inherited from Turtle class。Pyhton的精灵模块，为教育目的而制作启蒙动画与游戏。主要提供继承自Turtle类的Sprite类,Key类,Mouse类。支持像素级碰撞检测命令及增强的图章命令等等。作者：李兴球。网址： www.lixingqiu.com',
      long_description = long_d,      
      keywords = 'creative game pygame turtle animation sprite',
      url = 'http://www.lixingqiu.com',
      author ='lixingqiu',
      author_email = '406273900@qq.com',
      license = 'MIT',
      packages = ['sprites'],
      zip_safe = False,
      install_requires = [ 'pillow>=2.7.0','numpy']
     )

