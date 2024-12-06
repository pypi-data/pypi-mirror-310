from setuptools import setup,find_packages

setup(
    name = 'parvathimodule',  # Package name
    version = '0.2.0'      ,  # Version
    description = 'A sample Python module',
    author = 'Parvathi Vishnu',
    author_email= 'parvathi.r.vishnu@gmail.com',
    packages=find_packages(), #Automatically find modules
    install_requires=[] , # Dependencies (if any)
    python_requires = '>=3.6' #Supported python versions

)

# pip install setuptools wheel -- for creating a package
# We need to change to the location where setup.py is located ie; cd parvathimodule
# python setup.py sdist bdist_wheel --- for creating supporting files of python to locally install our module
# pip install dist/parvathimodule-0.1.0-py3-none-any.whl -- for installing our created modulepython setup.py sdist bdist_wheel 