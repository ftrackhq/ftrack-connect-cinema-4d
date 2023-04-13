..
    :copyright: Copyright (c) 2015 ftrack

.. _installing:

**********
Installing
**********

.. note::

  Unless you are doing any modifications, there should be no need to build the 
  extension yourself.

Building from source
====================

You can also build manually from the source for more control. First obtain a
copy of the source by either downloading the
`zipball <https://bitbucket.org/ftrack/ftrack-connect-cinema-4d/get/master.zip>`_ or
cloning the public repository::

    git clone git@bitbucket.org:ftrack/ftrack-connect-cinema-4d.git

Obtain `ftrack-connect-spark` and build the distribution files.

Set the required environment variables. Set the environment variable
`FTRACK_CONNECT_SPARK_DIST_DIR` to the directory contining the distribution
files for ftrack-connect-spark.

set the environment variable `FTRACK_CONNECT_CINEMA_4D_PLUGIN_DIR` to the
installation directory  for ftrack-connectc-cinema-4d, e.g.:
`/Users/john/Library/Preferences/MAXON/CINEMA 4D RXX_89538A46/plugins/ftrack`.

Build the plugin (Will build the plugin and dependencies in `build/plugin`)::

    python setup.py build_plugin

Install the plugin (Copy built files to Cinema 4D's plugin directory)::

    python setup.py install_plugin

Building documentation from source
----------------------------------

To build the documentation from source::

    python setup.py build_sphinx

Then view in your browser::

    file:///path/to/ftrack-connect-cinema-4d/build/doc/html/index.html

Running tests against the source
--------------------------------

With a copy of the source it is also possible to run the unit tests::

    python setup.py test

Dependencies
============

* `Python <http://python.org>`_ >= 3.0
