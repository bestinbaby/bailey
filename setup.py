from setuptools import setup, find_packages

setup(
    name="bailey",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bailey = bailey.bailey:main',
        ]},
    install_requires=['parsimonious>=0.8.1'],
    package_data={
        '': ['*.txt', '*.md'],
    },
    author="Baiju Muthukadan",
    author_email="baiju.m.mail@gmail.com",
    description="Bailey's dictionary parser",
)
