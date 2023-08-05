from setuptools import setup, find_packages

setup(
    name='ml-dev-tools',
    version='0.0.2',
    description='Useful functions for Machine Learning',
    author='Yousef Nami',
    author_email='namiyousef@hotmail.com',
    url='https://github.com/namiyousef/ml-utils',
    install_requires=['torch', 'sklearn'],
    #package_data={}
    packages=find_packages(exclude=('tests*', 'experiments*')),
    license='MIT',
    #entry_points=(),
)