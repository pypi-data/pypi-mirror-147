''' setup py'''

from setuptools import find_packages, setup

setup(
    name='sagala_framework',
    packages=find_packages(),
    version='0.1.0',
    description='Test buat library python',
    author='riskaamalia',
    license='MIT',
    install_requires=[],    
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='test',
)
