# -*- coding:utf-8 -*-
from setuptools import setup, find_packages  # 这个包没有的可以pip一下

setup(
    name="PdfTextFile",  # 这里是pip项目发布的名称
    version="0.0.1",  # 版本号，数值大的会优先被pip
    keywords=("pip", "PdfTextFile", "featureextraction"),
    description="pdf parsing text",
    long_description="PdfTextFile",
    license="MIT Licence",
    author="xxx",
    author_email="ddpptbx@163.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["pdfminer.six", "pdfminer", "regex", "pytz", "certifi", "setuptools",
                      "cryptography", "pip", "packaging", "Pillow", "click", "traits", "rdflib",
                      "configparser", "configobj", "tqdm", "lxml", "chardet", "simplejson",
                      "pycryptodome", "filelock", "idna", "nibabel", "pyparsing", "requests", "pycparser",
                      "python-dateutil", "networkx", "charset-normalizer", "prov", "urllib3", "numpy",
                      "six", "cffi", "scipy", "nipype", "pandas", "pydot", "pyxnat", "PyPDF3", "pathlib",
                      "wheel", "httplib2", "future", "Wand", "isodate", "pdfplumber", "colorama", "etelemetry",
                      "ci-info", "fitz"]  # 这个项目需要的第三方库
)
