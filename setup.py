from setuptools import setup

setup(
    name='kr-cli',
    version='0.1',
    py_modules=['kr'],
    install_requires=[
        'Click',
        'beautifulsoup4',
        'requests',
        'tabulate',
    ],
    entry_points='''
        [console_scripts]
        kr=kr:cli
    ''',
)

