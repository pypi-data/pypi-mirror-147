from setuptools import setup, find_packages


setup(
    name='futuretone',
    version='0.0.7',
    author='Jay',
    author_email='0jaybae0@gmail.com',
    description='Integrates into Future Tone on the PS4',
    url='https://github.com/Jay184/FT-Unofficial/tree/dev/api',
    project_urls={
        'Bug Tracker': 'https://github.com/Jay184/FT-Unofficial/labels/api',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['futuretone'],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        futuretone=futuretone:app
    ''',
    install_requires=[
        'click<8.1.0',
        'pydantic==1.9.0',
        'twitchio==2.2.0',
        'typer==0.4.0',
        'construct==2.10.68',
        'ps4debug>=0.1.3',  # Hey, I made this one! Check it out at "https://pypi.org/project/ps4debug/"
    ],
    extras_require={
        'dev': [
            'pyinstaller',
            'pyinstaller-versionfile',
            'build',
            'twine',
            'pytest',
        ]
    },
    python_requires='>=3.10'
)
