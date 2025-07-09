from setuptools import setup, find_packages

def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

# Read version from xerparser/__init__.py
def get_version():
    with open('xerparser/__init__.py', 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"\'')
    raise RuntimeError('Unable to find version string.')

setup(
    name='PyP6XER',
    version=get_version(),
    description='Python library for parsing and manipulating Primavera P6 XER files',
    long_description=readme(),
    long_description_content_type='text/markdown',
    
    # Author information
    author='Hassan Emam',
    author_email='hassan.emam@hotmail.com',
    
    # URLs
    url='https://github.com/HassanEmam/PyP6Xer',
    project_urls={
        'Documentation': 'https://hassanemam.github.io/PyP6Xer/',
        'Source': 'https://github.com/HassanEmam/PyP6Xer',
        'Tracker': 'https://github.com/HassanEmam/PyP6Xer/issues',
    },
    
    # Package discovery
    packages=find_packages(exclude=['tests*', 'docs*']),
    include_package_data=True,
    
    # License
    license='LGPL-2.1',
    
    # Python requirements
    python_requires='>=3.8',
    
    # Dependencies
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    
    # Optional dependencies
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'black>=21.0',
            'flake8>=3.8',
            'mypy>=0.900',
        ],
        'docs': [
            'sphinx>=5.0.0',
            'sphinx-rtd-theme>=1.0.0',
            'sphinx-autoapi>=2.0.0',
            'myst-parser>=0.18.0',
            'sphinx-copybutton>=0.5.0',
        ],
    },
    
    # Classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business :: Scheduling',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    
    # Keywords
    keywords='primavera p6 xer project management scheduling construction engineering parser dcma',
    
    # Entry points (if needed in the future)
    # entry_points={
    #     'console_scripts': [
    #         'pyp6xer=xerparser.cli:main',
    #     ],
    # },
)
