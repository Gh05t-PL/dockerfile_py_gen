import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='dockerfile_py_gen',
    version='0.1.0',
    author='Gh05t-PL',
    author_email='',
    description='Generate dockerfiles with python',
    keywords='dockerfile, generator, python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Gh05t-PL/dockerfile_py_gen',
    project_urls={
        'Documentation': 'https://github.com/Gh05t-PL/dockerfile_py_gen',
        'Bug Reports': 'https://github.com/Gh05t-PL/dockerfile_py_gen/issues',
        'Source Code': 'https://github.com/Gh05t-PL/dockerfile_py_gen',
        # 'Funding': '',
        # 'Say Thanks!': '',
    },
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    package_data={
        'dockerfile_py_gen': ['bin/hadolint'],  # Include binary in the package data
    },
    include_package_data=True,
    classifiers=[
        # see https://pypi.org/classifiers/
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    extras_require={
        'dev': ['twine'],
        # 'test': ['coverage'],
    },
    # entry_points={
    #     'console_scripts': [  # This can provide executable scripts
    #         'run=examplepy:main',
    # You can execute `run` in bash to run `main()` in src/examplepy/__init__.py
    #     ],
    # },
)
