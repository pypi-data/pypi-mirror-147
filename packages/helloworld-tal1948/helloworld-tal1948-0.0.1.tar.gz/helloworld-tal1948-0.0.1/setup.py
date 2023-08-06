from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

# A. name: The name of the package that will be uploaded to PyPI and will be used by pip install
#    It doesn't have to be the name of the python code that will be imported.
# B. py_modules: a list of the Python modules that will be included. In our case we have one
#    module called helloworldtal1948.py.
# C. package_dir: where our modules are located. In this case inside a sub folder called "src"
# D. Classifiers: Provides information about the package, information that will be used when
#    searching a package in PyPI.
# E. long_description: In addition to short description which is defined by description arg.
#    We can read its content from the README.rst file as we do in this example.
# F. long_description_content_type: The type of the long description. For example text/x-rst
#    for ReStructuredText or text/markdown for Markdown.
# H. install_requires: List of packages which are required for our code to run (for our module
#    to run). In other words, these are other packages which are code is using and not included
#    with the default Python distribution. In this example, we say that our code needs (although
#    it doesn't) the "blessing" package in version 1.7
# G. extras_require: packages which are needed in order to develop our package. In other words,
#    not packages which are used by our package code (packages which are needed in order for our
#    package to run), but packages that are needed if someone wants to further develop our package.
#    The most obvious example is pytest which is needed in order to run tests for our package.
#    In this case we provide a dictionary with a key in any name that we want (in this example
#    "dev". Later we can install it in a dev environment using pip install -e .["name that we
#    chose - dev]
setup(
    name='helloworld-tal1948',
    version='0.0.1',
    description="Say Hello",
    py_modules=["helloworldtal1948"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent"
                 ],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
        "blessings ~= 1.7",
    ],
    extras_require={
        "dev": [
            "pytest>=3.7",
        ],
    },
    url="https://github.com/talisel",
    author="Tal Barak",
    author_email="talisel@gmail.com",

)


# Next step is to run setup.py with bdist_wheel argument. This will create two sub folders.
# A. build with a sub folder called bdist.win32 (in this case) and a second sub folder called
#    lib with our module that were copied here.
# B. dist with the .whl file that was created.

# The "bdist_wheel" argument creates a binary distribution of our package, in wheel format.
# There are two types of distributions: binary distribution for people that simply wants to
# install the package in their environment and use it, and source distribution for people
# who wants to download the source dode of the package to their development environment,
# for example, if they want to further develop the package. The source distribution is
# created using the sdist argument after the python setup.py command.

# Now in order to test the package (that the package is installed correctly, not to test
# the actual code in the package), we have two options:
# A. we can install the whl file. However, assuming that we are still developing our package,
# everytime we make a change to the source code we will need to build the package again,
# uninstall the existing version and reinstall the new version.
# B. A second and better option, if we are still developing our package, is to use pip install
# -e . command (from the main folder, where setup.py is located). -e means that pip install
# will look for the setup.py, then using the setup.py will install our package but this time
# not by copying it to the \venv\lib folder, but just linking the package name to the source
# code inside \src. So everytime we make a change to the source code, and using the package
# name, we continue to use the most updated code.

# Now we can test that we can use the package. Instead of creating a new source code file that
# will mess our package folder, we can just run python in the terminal.

# Next step - let's assume that we want to upload our code to GitHub. We would like to have
# a .gitignore file that will assure that we don't upload unrelevant files. We can create
# a .gitignore file using the gitignore.io site. All we need is to type python in the searchbox.

# next step is to create LICENSE.txt file which can be done using the site choosealicense.com

# Then we need to create documentation. Two formats which are applicable are ReStructuredText
# and Markdown. ReStructuredText is pythonic, powerful and can be used by Sphinx. Markdown is
# more widespread, simpler and can be used by MkDocs.

# Then we need to create test file and test it using pytest.
# Finally we need to create a source ditribution, but some of the files will not be included.
# To solve this we need to create a MANIFEST.in file. This is done by:
# pip install check-manifest
# check-manifest --create
# git add MANIFEST.ini

# Commit your files first.

# Now it's time to publish it. Build sdist and bdist one more time using:
# python setup.py bdist_wheel sdist
# To upload install twine by typing pip install twine
# and then twine upload dist/*

# Everytime we make a change in setup.py
