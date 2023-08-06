
import setuptools

setuptools.setup(
    name='indic-LayoutParser',  
    version='1.0.0',
    author="",
    author_email="",
    description="parsing indic text from jpg/pdf",
    long_description="parsing indic text from jpg/pdf",
    url="",
    packages=["indic-LayoutParser"],
    # entry_points = {
    #     "console_scripts": ['indic-LayoutParser = indic-LayoutParser.indic-LayoutParser:main']
    # },
    install_requires = ['layoutparser','pandas','numpy','opencv-python'
    ,'pillow','Image','pytesseract','pdf2image','pdfreader',
    'pathlib','uuid'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
