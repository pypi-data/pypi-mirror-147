
from setuptools import setup, find_packages
setup(name='test_fish',
      version='0.0.2',
      description='just test',
      author='fmc123653',
      author_email='fmc0315@126.com', #这里务必填写正确的email格式
      packages=find_packages(),  # 表示你要封装的包，find_packages用于系统自动从当前目录开始找包
      license="apache 3.0"
      )