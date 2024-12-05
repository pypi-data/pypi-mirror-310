from setuptools import setup, find_packages

version = {
    "major" :0,
    "minor" :0,
    "patch" :1 ,
    "year" :2024,
}

setup(
    name='cbuild',
    version=f"{version["major"]}.{version["minor"]}.{version["patch"]}.{version["year"]}",
    description='An Easy To Use CLI Build Tool For C',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='zeroth.bat@gmail.com',
    url='https://github.com/d34d0s/cbuild',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)