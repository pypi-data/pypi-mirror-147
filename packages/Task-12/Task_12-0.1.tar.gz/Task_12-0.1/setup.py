from setuptools import setup, find_packages


setup(
    name='Task_12',
    version='0.1',
    author="Eryuzheva Alesya",
    license='MIT',
    description='this project is for testing',
    packages=find_packages(),
    url='https://github.com/LesyaEryuzheva/My_hometasks',
    install_requires=[
          'Django==4.0.4',
          'Fastapi==0.75.2'
      ],

)