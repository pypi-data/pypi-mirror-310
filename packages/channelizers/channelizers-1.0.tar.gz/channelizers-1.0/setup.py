import codecs
import os
from setuptools import setup, find_packages

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


VERSION = '1.0'
DESCRIPTION = ('A python package for ultra bandwidth signal process, can divide signal into several narrow bandwidth '
               'signal')
LONG_DESCRIPTION = ('A python package for ultra bandwidth signal process, can divide signal into several narrow '
                    'bandwidth signal. The method use polyphase filter bank, including Critical polyphase filter '
                    'bank(CSPFB)/Integer-oversample filter bank(IOSPFB)/Rationally-oversampled filter bank(ROSPFB)')
# Setting up
setup(
    name="channelizers",
    version=VERSION,
    author="duxu",
    author_email="duxu@xao.ac.cn",
    license='MIT',
    description=DESCRIPTION,
    url='https://github.com/WhataDavid/Channelizer',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(where="PFB"),
    package_dir={"": "PFB"},  # PFB 是根目录
    install_requires=['numpy','matplotlib','scipy'],
    zip_safe=False,
    keywords=['python','channelizer','PFB','ultra bandwidth signal','astronomy'],
    include_package_data=True,
    package_data={
        # 只包括必要的文件
        "pfb": ["__init__.py","channelizer.py", "cspfb.py","fft_all.py","mini_data.txt","opfb.py","plot_block_dtw.ipynb","plot_profile.ipynb","plot_pulse_dtw.ipynb","plot_sub.ipynb","psr.py,exec_text.py"],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X"
    ]
)