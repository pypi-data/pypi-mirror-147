from setuptools import setup

setup(
    name="addresshunt",
    version='1.0',
    packages=['addresshunt'],
    description='Python package for address validations',
    author='AddressHunt',
    author_email='contact@addresshunt.com.au',
    url='https://addresshunt.com.au/#home',
    entry_points='''
        [console_scripts]
    ''',
    install_requires=[
    'requests'
    ]
)