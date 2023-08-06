from setuptools import find_packages, setup

setup(
    name='dsframeworklib',
    packages=find_packages(include=['dsframeworklib', 'dsframeworklib.utils']),
    version='0.0.14',
    description='Basic distributed system framework, to simulate working of distributed systems',
    author='appmonster007',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
