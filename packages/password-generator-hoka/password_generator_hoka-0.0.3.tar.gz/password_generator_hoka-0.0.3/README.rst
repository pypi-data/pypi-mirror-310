Password Generator

A simple Python package for generating secure passwords.

Installation
------------

To install the package, you can use pip:

.. code:: bash

    pip install password-generator

Usage
-----

Here is an example of how to use the `password-generator` package:

.. code:: python

    from password_generator import generate_password

    # Create a password generator instance
    pg = generate_password()

    # Generate a secure password
    password = pg.generate()
    print(password)

Features
--------

- Generates random, secure passwords.
- Customizable length and character set.
- Simple and easy to use.

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.

