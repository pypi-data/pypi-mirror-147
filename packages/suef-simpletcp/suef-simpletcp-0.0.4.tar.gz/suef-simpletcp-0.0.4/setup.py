from setuptools import setup
from os import path

from io import open

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='suef-simpletcp',
    version='0.0.4',
    description='Simple solution to get started with TCP Servers and Clients',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sueffuenfelf/simpletcp',
    author='sueffuenfelf',
    author_email='depsol.github@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    python_requires=">=3.6",
    keywords='tcp simple easy',

    packages=['suef_simpletcp'],

    project_urls={
        'Bug Reports': 'https://github.com/sueffuenfelf/simpletcp/issues',
        'Source': 'https://github.com/sueffuenfelf/simpletcp'
    },
)