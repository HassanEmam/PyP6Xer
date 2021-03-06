from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='PyP6Xer',
    version='1.011.04',
    long_description=readme(),
    long_description_content_type='text/markdown',
    packages=['xerparser', 'xerparser.model', 'xerparser.model.classes'],
    url='',
    license='GNU GENERAL PUBLIC LICENSE',
    author='Hassan',
    author_email='hassan.emam@hotmail.com',
    install_requires=[
        'tqdm==4.50.0'
      ],
    description='Parser for XER written in Python'
)
