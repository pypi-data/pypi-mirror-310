import setuptools

version = {
    "year" :2024,
    "minor" :0,
    "patch" :1 ,
}

setuptools.setup(
    name='cbuild',
    version=f"{version["year"]}.{version["minor"]}.{version["patch"]}",
    description='An Easy To Use CLI Build Tool For C',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Izaiyah Stokes',
    author_email='zeroth.bat@gmail.com',
    url='https://github.com/d34d0s/cbuild',
    packages=setuptools.find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)