from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.rst").read_text()

setup(
    name="addresshunt",
    version='1.1',
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
    ],
    long_description=long_description,
    long_description_content_type='text/x-rst'
)