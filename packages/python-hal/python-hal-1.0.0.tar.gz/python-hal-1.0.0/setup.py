from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'H.A.L Is a voice activated virtual assistant'
LONG_DESCRIPTION = 'H.A.L (Helpful Artificial Listener) Is a voice activated virtual assistant meant to help do simple tasks on your computer'

# Setting up
setup(
    name="python-hal",
    version=VERSION,
    author="Cyber Coding",
    author_email="<kinectcode@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['SpeechRecognition', 'datetime', 'wikipedia', 'gtts', 'pygame', 'mutagen', 'art', 'requests', 'python-dotenv', 'bs4', 'datetime', 'argparse', 'requests'],
    keywords=['python', 'hal', 'assistant', 'voice controlled', 'voice', 'text to speech'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)