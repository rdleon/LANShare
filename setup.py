from setuptools import setup
from lanshare.conf import __version__

setup(name='lanshare',
      version=__version__,
      description='Share files on a local network',
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
