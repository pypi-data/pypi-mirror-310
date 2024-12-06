import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyspiget',
    author='Mark7888',
    author_email='l.mark7888@gmail.com',
    description='Simple Python wrapper for the Spiget API',
    keywords='spiget, spigot, minecraft, api, wrapper, plugins, resources',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Mark7888/pyspiget',
    project_urls={
        'Documentation': 'https://github.com/Mark7888/pyspiget/blob/master/README.md',
        'Bug Reports': 'https://github.com/Mark7888/pyspiget/issues',
        'Source Code': 'https://github.com/Mark7888/pyspiget',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        'requests >= 2.31.0',
    ],
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Games/Entertainment',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',

        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3',
)
