from setuptools import setup, find_packages
import codecs
import os
import PyScriptTools

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '4.2.7'
DESCRIPTION = 'Simple Python Package to Gather and Show Your System Info.'
LONG_DESCRIPTION = 'A package that allows you to Gather and Collect all of Your System Information by Calling Only methods.'


setup(
    name="PyScriptTools",
    version=VERSION,
    author="Shervin Badanara (shervinbdndev)",
    author_email="shervin2234@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages() ,
    project_urls={
        'Source':'https://www.github.com/shervinbdndev/PyScriptTools/'
    },
    install_requires=['GPUtil' , 'requests' , 'sockets' , 'colorama' , 'python-cfonts' , 'setuptools' , 'wheel' , 'getmac' , 'psutil'] ,
    keywords=['python', 'system', 'systeminfo', 'local ip', 'public ip', 'sockets' , 'cpu info' , 'gpu info' , 'ram info' , 'disk info'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ] ,
    extras_require={
        'dev':['check-manifest'] ,
        'test' : ['coverage'] ,
    },
    package_data={
        'PyScriptTools':['package_data.dat'] ,
    }
)