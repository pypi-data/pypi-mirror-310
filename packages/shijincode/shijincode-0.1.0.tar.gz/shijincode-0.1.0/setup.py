from setuptools import setup,find_packages

setup(
    name = 'shijincode',     # package
    version= '0.1.0',           # version
    description= 'A sample Python module',
    author= 'shijin',
    author_email= 'shijinkc0@gmail.com',
    package = find_packages(),         # Automathically find modules
    install_requires = [],             # Dependencies (if any)
    python_requires = '>=3.6',          # Supported Python versions
)