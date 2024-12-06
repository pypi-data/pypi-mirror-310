from setuptools import setup,find_packages

setup(
    name = 'parvathimodule',  # Package name
    version = '0.1.0'      ,  # Version
    description = 'A sample Python module',
    author = 'Parvathi Vishnu',
    author_email= 'parvathi.r.vishnu@gmail.com',
    packages=find_packages(), #Automatically find modules
    install_requires=[] , # Dependencies (if any)
    python_requires = '>=3.6' #Supported python versions

)

# pip install setuptools wheel -- for creating a package