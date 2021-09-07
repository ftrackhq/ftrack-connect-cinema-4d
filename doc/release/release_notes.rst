..
    :copyright: Copyright (c) 2016 ftrack

.. _release/release_notes:

*************
Release Notes
*************

.. release:: 0.2.0
    :date: 2021-09-07

    .. change:: fixed
        :tags: Discover

        Update hook to application launcher.

    .. change:: changed

        Update code to run on python 3.7

.. release:: 0.1.5
    :date: 2017-10-12

    .. change:: fixed
        :tags: Publish

        Only the default "Upload" asset type can be selected before erasing the text.

    .. change:: fixed
        :tags: Publish

        Publish times out after 30 seconds.

.. release:: 0.1.4
    :date: 2017-06-28

    .. change:: fixed

        API version is incompatible with ftrack server version 3.5.

    .. change:: fixed
        :tags: Publish

        Threading issues caused publishes to fail.

.. release:: 0.1.2
    :date: 2016-07-14

    .. change:: fixed
        :tags: Publish

        The published component has no file type if the project has not been
        saved yet.

.. release:: 0.1.1
    :date: 2016-06-14

    .. change:: fixed
        :tags: Publish

        Session not reset when publish fails, making it impossible to try again.

.. release:: 0.1.0
    :date: 2016-06-07

    .. change:: new

        Initial release of the ftrack plugin for Cinema 4D.

        Instantly access project management: Gain a simplified overview of your
        assigned tasks from the ftrack panel. You can browse and drill down to
        any project available in ftrack, making design-based project management
        a breeze.

        Dive into details: Easily access task information, notes and published
        files. Import tracked files from ftrack or share notes.

        Publish your work online: Publish your work to ftrack’s cloud platform
        directly from supported applications. ftrack supports a broad range of
        storage options, including your own file system.

    .. change:: new
        :tags: Publish

        Publish the active Cinema 4D project file to ftrack as a new version.

    .. change:: new
        :tags: Import

        Import Cinema 4D projects and other files from ftrack as XRef objects.
