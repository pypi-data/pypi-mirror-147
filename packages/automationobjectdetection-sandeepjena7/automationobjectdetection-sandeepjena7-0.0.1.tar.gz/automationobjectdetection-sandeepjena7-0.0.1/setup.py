from setuptools import setup
import os

PROJECT_NAME = "automationobjectdetection"
USER_NAME = "sandeepjena7"

setup(
    name=f"{PROJECT_NAME}-{USER_NAME}",
    version="0.0.1",
    url="https://github.com/sandeepjena7/automateobjectdetctiontf1dectron2yolov5",
    author="sandeepjean777",
    author_email="sandeepjean777@gmail.com",
    packages=["src"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "protobuf"
        ,"six"
        ,"tensorboard==1.14.0"
        ,"tensorflow==1.14.0"
        ,"opencv-python"
        ,"matplotlib"
        ,"Cython"
        ,"torch==1.8.1 "
        ,"torchvision==0.9.1"
        ,"fvcore"
        ,"cloudpickle"
        ,"omegaconf"
        ,"pandas"
        ,"seaborn"
        ,"requests"
        ,"pycocotools" #ihave not install pycocotools-windows through setup.py we can install mannualy
        # pip install  pycocotools-windows
    ]
    )