from setuptools import setup, find_packages

setup(
    name='flight_mapper',
    packages=find_packages(include=('flight_mapper', 'flight_mapper.*')),
    include_package_data=True,
    install_requires=[
        'matplotlib>=3.2',
        'numpy>=1.17',
        'scipy>=1.3',
        'pandas',
        'yattag'
    ]
)
