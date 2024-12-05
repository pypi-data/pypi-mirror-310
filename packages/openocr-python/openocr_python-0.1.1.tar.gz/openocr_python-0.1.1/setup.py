from setuptools import setup

VERSION = '0.1.1'
DESCRIPTION = 'a python package for openocr, which is used to help developers quickly deploy OCR algorithms implemented in the openocr framework.'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Setting up
setup(
    author="OpenOCR",
    author_email="18300180089@fudan.edu.cn",
    name="openocr-python",
    url='https://github.com/Topdu/OpenOCR',
    version=VERSION,
    packages=['openocr', 'tools'],
    package_dir={'': '.'},
    include_package_data=True,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    project_urls={"Source Code": "https://github.com/Topdu/OpenOCR",},
    install_requires=['opencv-python<=4.6.0.66','tqdm','rapidfuzz','lmdb','imgaug','pyyaml'],
    keywords=['python','OCR','STR','OpenOCR','openocr'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)

