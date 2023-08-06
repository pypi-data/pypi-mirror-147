Hello World
===========

This is an example project demonstrating how to publish a python module to PyPI.

Installation:
~~~~~~~~~~~~~

Run the following to install:

``pip install helloworld``

Usage:
~~~~~~

.. code-block:: python

    from helloworld import say_hello()

    # Generate "Hello, World!"
    say_hello()

    # Generate "Hello, Tal!"
    say_hello("Tal")


Developing Hello World:
~~~~~~~~~~~~~~~~~~~~~~~

To install helloworld, along with the tools you need to develop and run tests,
run the following in your virtualenv:

``pip install -e .[dev]``
