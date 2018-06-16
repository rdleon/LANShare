from setuptools import setup

setup(name='lanshare',
      version='0.1',
      description='Sharing programs on the LAN',
      url='https://github.com/hsmty/LANShare',
      author='Rafael Díaz de León Plata',
      author_email='leon@elinter.net',
      license='MIT',
      packages=['lanshare'],
      install_requires=[
          'zeroconf',
      ],
      entry_points = {
          'console_scripts': [
              'lanshare = lanshare.__main__:main'
          ]
      })
