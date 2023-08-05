from setuptools import setup

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='scChart',
    version='1.0',
    description='Chart Feature for ScratchConnect Python Library',
    long_description=open('chartREADME.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/Sid72020123/scratchconnect/',
    author='Siddhesh Chavan',
    author_email='siddheshchavan2020@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='chart scratch data',
    packages=["scChart"],
    install_requires=['pyhtmlchart']
)
