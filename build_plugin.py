# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import shutil
import pip


ROOT_PATH = os.path.dirname(
    os.path.realpath(__file__)
)

SOURCE_PATH = os.path.join(
    ROOT_PATH, 'source'
)

RESOURCE_PATH = os.path.join(
    ROOT_PATH, 'resource'
)

BUILD_PATH = os.path.join(
    ROOT_PATH, 'build'
)

STAGING_PATH = os.path.join(
    BUILD_PATH, 'plugin'
)

# Clean staging path
shutil.rmtree(STAGING_PATH, ignore_errors=True)

# Copy plugin files
shutil.copytree(
    os.path.join(RESOURCE_PATH, 'plugin'),
    STAGING_PATH
)

# Copy source package
shutil.copytree(
    os.path.join(SOURCE_PATH, 'ftrack_connect_cinema_4d'),
    os.path.join(STAGING_PATH, 'ftrack', 'ftrack_connect_cinema_4d')
)

# Copy spark package
shutil.copytree(
    os.environ['FTRACK_CONNECT_SPARK_DIST_DIR'],
    os.path.join(STAGING_PATH, 'ftrack', 'ftrack_connect_spark')
)

# Add dependencies.
modules = ('appdirs', 'ftrack-python-api')
for module in modules:
    pip.main(
        ['install', module, '--target', os.path.join(STAGING_PATH, 'ftrack')]
    )
