sornobase
================

My base libraries. `sorno` is just a brand name that I use for my stuff.
It's convenient to use that as a package name instead of the usual "org.xxx".

The source code of the whole project is in github:
https://github.com/hermantai/sornobase

PyPI page: https://pypi.python.org/pypi/sornobase

Installation
--------------------
If you don't have Python installed, you first need to install it from
https://www.python.org/downloads/. You need a version at least 3.

For the following commands, add **sudo** in front of the commands if you are
getting permission error.

A Python package management system will make your life easier, so install pip:
https://pip.pypa.io/en/stable/installation/

Install libmagic
~~~~~~~~~~~~~~~~
The library depends on python-magic: https://pypi.org/project/python-magic/

That requires the installation of libmagic::

    $ brew install libmagic

Install with pip
~~~~~~~~~~~~~~~~
::

    $ pip install sornobase

Install from source
~~~~~~~~~~~~~~~~~~~
You can install sornobase from the source code by cloning the git repo::

    $ git clone https://github.com/hermantai/sornobase

Then cd to the sornobase directory::

    $ cd sornobase

Install it::

    $ python setup.py install


Running the tests
-----------------
In the directory containing the ./test.sh file, then run it::

    $ ./test.sh

You can run tests only for the sorno library::

    $ ./test_sornobase.sh

Or tests only for the scripts::

    $ ./test_scripts.sh

Unit testing
~~~~~~~~~~~~
You can run the unit tests in the *sornobase/tests* directory. First, set up the
testing environment by running::

    $ source setup_test_env.sh

If you have installed sornobase in your machine, the *sornobase* library
from the installation is used instead of your local changes because of
easy-install messing with the search path. In that case you need to either
remove the egg manually or bump up the version and install it with your local
changes to override the existing version.

Then you can run individual unit tests with::

    $ python sornobase/tests/test_xxx.py

Deployment
~~~~~~~~~~
The only deployment destinations for now is github and PyPI. In github, this
project resides in the sornobase project:
https://github.com/hermantai/sornobase

To deploy to PyPI, first install twine::

    $ pip install twine

Then you can use the script to deploy to PyPI::

    $ ./pypi_deploy_with_twine.sh

Use **sudo** if you encounter permission issues when running the commands.

Use the following if you get an error saying "twine cannot be found" even
twine is on your PATH::

    sudo env "PATH=$PATH" ./pypi_deploy_with_twine.sh

If twine does not work, use the old school::

    $ ./pypi_deploy.sh
