from setuptools import setup, find_packages
import codecs
import os

# Setting up
setup(
    name="myhellopkg",
    version='0.0.5',
    author="Muthukumar",
    author_email="<gkmuthu@gmail.com>",
    description='Say Hello',
    long_description_content_type="text/markdown",
    install_requires=['pysmb'],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    py_modules=["helloworld"],
    package_dir={'':'src'},
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
