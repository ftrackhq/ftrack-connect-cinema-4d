..
    :copyright: Copyright (c) 2016 ftrack

.. _troubleshooting:

***************
Troubleshooting
***************

.. _troubleshooting/viewing_logs:

Viewing logs
============

You can view logs from inside Cinema 4D by opening
:guilabel:`Script -> Console`. Errors and activity is also stored on disk in the
following directory, in a file named `ftrack_connect_cinema_4d.log`.

:OS X:
    ~/Library/Application Support/ftrack-connect/log

:Windows:
    C:\\Documents and Settings\\<User>\\Application Data\\Local Settings\\ftrack\\ftrack-connect\\log

:Linux:
    ~/.local/share/ftrack-connect/log

Known issues
============

The plugin is not able to communicate with locally hosted ftrack servers
running HTTP when using Cinema 4D R18 (SP0 or SP1) and macOS 10.11 or newer.
Using R17 or R18 SP2 should work.
