from setuptools import setup

setup(
    name='cameo_threshold',
    version='0.1.0',
    description='the first version of cameo_threshold',
    release_notes='',
    url='https://github.com/bohachu/cameo_threshold',
    author='JC Wang',
    author_email='jcxgtcw@gmail.com',
    license='BSD 2-clause',
    packages=['cameo_threshold'],
    install_requires=[
        'pandas'
        #'polars'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)