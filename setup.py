from setuptools import setup

setup(
   name='eda',
   version='1.0',
   description='Visualization and EDA',
   author='Jinho Park',
   author_email='jinhoparkseoul@gmail.com',
   packages=['eda'],  #same as name
   install_requires=['wheel', 'bar'], #external packages as dependencies
)
