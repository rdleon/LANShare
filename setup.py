from setuptools import setup

setup(name='lanshare',
      version='0.1',
      description='Sharing programs on the LAN',
      url='https://github.com/hsmty/LANShare',
      author='Rafael Díaz de León Plata',
      author_email='leon@elinter.net',
      license='ISC',
      packages=['lanshare'],
      install_requires=[
          'zeroconf',
      ])
