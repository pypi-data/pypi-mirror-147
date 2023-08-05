from setuptools import setup, find_packages


setup(
    name='wot-ap-tms',
    version='1.0',
    license='MIT',
    author="Andrei Petukhou",
    author_email='andrey_petuhov@tut.by',
    packages=find_packages('src'),
    package_dir={'': 'src'},

)
