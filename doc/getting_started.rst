..
    :copyright: Copyright (c) 2016 ftrack

***************
Getting started
***************

Getting started with the Cinema 4D plugin is really easy, just follow this guide
and you will be up and running in no time.

Requirements
------------

The plugin requires Cinema 4D R17 or later and either Windows (7 or later with
Internet Explorer 11 installed), or macOS (10.11 or newer).

.. _getting_started/signup:

1. Signup to ftrack (only for new users)
----------------------------------------

If you haven't already got an ftrack account you can sign up for a 30 day
free trial at our `Sign up page <https://www.ftrack.com/signup>`_. 

2. Connect
----------

Download and install ftrack Connect for your platform at
`Connect download page <https://www.ftrack.com/portfolio/connect>`_.

Open Connect and sign in with your company's ftrack URL, e.g.
<company-url>.ftrackapp.com.

.. note::

    If this is the first time you use ftrack and Connect you will be asked to
    configure a Storage scenario to let ftrack now how to publish your files.
    See
    `this article <http://ftrack.rtd.ftrack.com/en/stable/administering/configure_storage_scenario.html>`_
    for more information.

3. Cinema 4D plugin
-------------------

1 Start c4d and from edit -> preferences -> plugins add a new folder pointing to:: 

 /ftrack Connect-<version>re/source/connect-standard-plugins/ftrack-connect-cinema-4d-<version>\plugin

2 close and restart cinema then open the ftrack dialog from the ftrack menu.
