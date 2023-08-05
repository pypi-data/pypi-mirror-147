from setuptools import setup, find_packages

setup(
    name='sun-py-package-test',
    version="v1.0.1",
    description='test',
    long_description="test long",
    author='aa',
    maintainer_email="aa@aa.com",
    scripts=[],
    packages=find_packages(exclude=["tests*"]),
    license="Apache License 2.0",
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable'
    ],
)