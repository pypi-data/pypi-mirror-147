from setuptools import setup, find_packages

setup(
    name='andrnspyke',
    version='0.0.1',
    py_modules=['pyke'],
    package_dir={"":"pykepkg"},
    packages=find_packages(where="pykepkg"),
    install_requires=[
        'Click',
        'requests',
        'pyfiglet',
        'termcolor',
        'beautifulsoup4',
    ],
    entry_points={
        'console_scripts': [
            'pyke = main:grab_word',
        ],
    },
)
