from setuptools import setup, find_packages

'''classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]'''

setup(
    name='swapnilcalculator',
    version='0.0.1',
    description='Very very basic calculator for trial',
    Long_description=open('README.txt').read()+'\n'+open('CHANGELOG.txt').read(),
    url='',
    author='swapnil',
    author_email='swapniljt85@gmail.com',
    license='MIT',
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    #classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['']
)