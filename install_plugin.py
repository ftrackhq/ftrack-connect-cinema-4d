# :coding: utf-8
# :copyright: Copyright (c) 2016 ftrack

import os
import os.path
import shutil


def install_plugin():
    '''Install plugin.'''
    root_path = os.path.dirname(
        os.path.realpath(__file__)
    )

    build_path = os.path.join(
        root_path, 'build'
    )

    staging_path = os.path.join(
        build_path, 'plugin'
    )

    ftrack_connect_cinema_4d_plugin_dir = None
    try:
        ftrack_connect_cinema_4d_plugin_dir = os.path.abspath(
            os.environ['FTRACK_CONNECT_CINEMA_4D_PLUGIN_DIR']
        )
    except KeyError:
        raise ValueError(
            'Please set the environment variable '
            '`FTRACK_CONNECT_CINEMA_4D_PLUGIN_DIR` to the installation directory  '
            'for ftrack-connectc-cinema-4d, e.g.: \n'
            '`/Users/john/Library/Preferences/MAXON/CINEMA 4D R17_89538A46/plugins/ftrack`.'
        )

    # Clean staging path
    shutil.rmtree(ftrack_connect_cinema_4d_plugin_dir, ignore_errors=True)

    # Copy plugin files
    shutil.copytree(
        os.path.join(staging_path, 'ftrack'),
        ftrack_connect_cinema_4d_plugin_dir
    )


if __name__ == '__main__':
    install_plugin()
    print 'Installed plugin.'
