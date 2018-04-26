from os import path
from setuptools import setup


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='carbonize',
    version='0.0.1',
    author='eillarra',
    author_email='eneko@illarra.com',
    license='MIT',
    url='https://github.com/eillarra/carbonize',
    project_urls={
        'Code': 'https://github.com/eillarra/carbonize',
        'Issues': 'https://github.com/eillarra/carbonize/issues',
    },
    description='Carbon Emissions calculator.',
    long_description=long_description,
    keywords='calculator co2 carbon greenhouse emissions footprint',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=['carbonize'],
    package_dir={'carbonize': 'carbonize'},
    package_data={'carbonize': ['data/*.csv']},
    install_requires=[],
    zip_safe=False
)
