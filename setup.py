from setuptools import setup, find_packages

setup(
    name='MillyMover',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.14'
    ],
    entry_points={'console_scripts':'mover=mover.__main__:main'}
)