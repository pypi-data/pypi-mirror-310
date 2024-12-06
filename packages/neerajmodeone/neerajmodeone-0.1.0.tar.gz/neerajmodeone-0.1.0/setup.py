from setuptools import setup,find_packages

setup(
    name = 'neerajmodeone',     # package
    version= '0.1.0',           # version
    description= 'A sample Python module',
    author= 'Neeraj V N',
    author_email= 'weldernaru@gmail.com',
    package = find_packages(),         # Automathically find modules
    install_requires = [],             # Dependencies (if any)
    python_requires = '>=3.6',          # Supported Python versions
)
