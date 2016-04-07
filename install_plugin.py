import os.path
import shutil

ROOT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

BUILD_PATH = os.path.join(
    ROOT_PATH, 'build'
)

STAGING_PATH = os.path.join(
    BUILD_PATH, 'plugin'
)

CINEMA_4D_PLUGIN_DIR = os.path.expanduser(
    '~/Library/Preferences/MAXON/CINEMA 4D R17_89538A46/plugins/ftrack'
)

# Clean staging path
shutil.rmtree(CINEMA_4D_PLUGIN_DIR, ignore_errors=True)

# Copy plugin files
shutil.copytree(
    os.path.join(STAGING_PATH, 'ftrack'),
    CINEMA_4D_PLUGIN_DIR
)