from setuptools import setup, find_packages

setup(
    name='gramload',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'instaloader',
    ],
    entry_points={
        'console_scripts': [
            'gramload=gramload.gramload:main',
        ],
    },
)