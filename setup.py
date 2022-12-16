from setuptools import setup

setup(name='qnapdisplay_truenas',
      version='0.1',
      description='Library for interacting with front-panel displays on Qnap products within TrueNAS Scale',
      url='https://github.com/ITninja04/QNAP_Scale_LCD_Script',
      author='ITninja04',
      license='MIT',
      packages=['qnapdisplay_truenas'],
      install_requires=['pyserial', 'serial', 'netaddr', 'psutil', 'netaddr'])
