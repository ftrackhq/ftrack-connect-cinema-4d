# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import sys
import subprocess

import os.path
import re
import shutil
import pip
import glob

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import setuptools.command.build_py
import distutils.log
import setuptools_scm



PLUGIN_NAME = 'ftrack-connect-cinema-4d-{0}'

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
    BUILD_PATH,
    PLUGIN_NAME
)

PLUGIN_STAGING_PATH = os.path.join(
    BUILD_PATH, 'plugin'
)

HOOK_PATH = os.path.join(
    RESOURCE_PATH, 'hook'
)


README_PATH = os.path.join(ROOT_PATH, 'README.rst')

release = setuptools_scm.get_version(version_scheme='post-release')
VERSION = '.'.join(release.split('.')[:3])


STAGING_PATH = STAGING_PATH.format(VERSION)


# Custom commands.
class PyTest(TestCommand):
    '''Pytest command.'''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        '''Import pytest and run.'''
        import pytest
        errno = pytest.main(self.test_args)
        raise SystemExit(errno)


class BuildPlugin(setuptools.Command):
    '''Build plugin.'''
    description = 'Download dependencies and build plugin .'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''Run the build step.'''
        # Clean staging path
        shutil.rmtree(BUILD_PATH, ignore_errors=True)

        ############# INTEGRATION ###############

        # Copy hook files
        shutil.copytree(
            HOOK_PATH,
            os.path.join(STAGING_PATH, 'hook')
        )

        # Generate plugin zip
        shutil.make_archive(
            os.path.join(
                BUILD_PATH,
                PLUGIN_NAME.format(VERSION)
            ),
            'zip',
            STAGING_PATH
        )

        ############# PLUGIN ###############
        # Copy plugin files
        shutil.copytree(
            os.path.join(RESOURCE_PATH, 'plugin'),
            PLUGIN_STAGING_PATH
        )

        # Copy source package
        shutil.copytree(
            os.path.join(SOURCE_PATH, 'ftrack_connect_cinema_4d'),
            os.path.join(PLUGIN_STAGING_PATH, 'ftrack', 'ftrack_connect_cinema_4d')
        )

        # Copy spark package
        try:
            shutil.copytree(
                os.environ['FTRACK_CONNECT_SPARK_DIST_DIR'],
                os.path.join(PLUGIN_STAGING_PATH, 'ftrack', 'ftrack_connect_spark')
            )
        except KeyError:
            raise ValueError(
                'Please set the environment variable '
                '`FTRACK_CONNECT_SPARK_DIST_DIR` to the directory contining '
                'the distribution files for ftrack-connect-spark.'
            )

        # Add dependencies.
        modules = ('appdirs>=1.4.3,<2', 'ftrack-python-api>=1.1.1,<3')
        for module in modules:

            subprocess.check_call(
                [
                    sys.executable, '-m', 'pip', 'install','.','--target',
                    os.path.join(PLUGIN_STAGING_PATH, 'ftrack', 'dependencies')
                ]
            )


class InstallPlugin(setuptools.Command):
    '''Install plugin.'''
    description = 'Install plugin to `FTRACK_CONNECT_CINEMA_4D_PLUGIN_DIR`.'

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        '''Install plugin.'''
        ftrack_connect_cinema_4d_plugin_dir = None
        try:
            ftrack_connect_cinema_4d_plugin_dir = os.path.abspath(
                os.environ['FTRACK_CONNECT_CINEMA_4D_PLUGIN_DIR']
            )
        except KeyError:
            raise ValueError(
                'Please set the environment variable '
                '`FTRACK_CONNECT_CINEMA_4D_PLUGIN_DIR` to the installation '
                'directory for ftrack-connectc-cinema-4d, e.g.: \n'
                '`/Users/john/Library/Preferences/MAXON/CINEMA 4D R17_89538A46/plugins/ftrack`.'
            )

        # Clean staging path
        distutils.log.info(
            u'Cleaning target directory: {0}'.format(ftrack_connect_cinema_4d_plugin_dir)
        )
        shutil.rmtree(ftrack_connect_cinema_4d_plugin_dir, ignore_errors=True)

        # Copy plugin files
        plugin_directory = os.path.join(STAGING_PATH, 'ftrack')
        distutils.log.info(
            u'Copying plugin files: {0} -> {1}'.format(
                plugin_directory,
                ftrack_connect_cinema_4d_plugin_dir
            )
        )
        shutil.copytree(
            plugin_directory,
            ftrack_connect_cinema_4d_plugin_dir
        )
        distutils.log.info(
            u'Installed plugin to: {0}'.format(ftrack_connect_cinema_4d_plugin_dir)
        )

version_template = '''
# :coding: utf-8
# :copyright: Copyright (c) 2017-2020 ftrack

__version__ = {version!r}
'''


# Configuration.
setup(
    name='ftrack connect Cinema 4D',
    description='ftrack connect integration for MAXON Cinema 4D.',
    long_description=open(README_PATH).read(),
    keywords='',
    url='https://bitbucket.org/ftrack/ftrack-connect-cinema-4d',
    author='ftrack',
    author_email='support@ftrack.com',
    license='Apache License (2.0)',
    packages=find_packages(SOURCE_PATH),
    package_dir={
        '': 'source'
    },
    setup_requires=[
        'sphinx >= 1.2.2, < 2',
        'sphinx_rtd_theme >= 0.1.6, < 2',
        'lowdown >= 0.1.0, < 1',
        'setuptools>=45.0.0',
        'setuptools_scm'
    ],
    use_scm_version={
        'write_to': 'source/ftrack_connect_cinema_4d/_version.py',
        'write_to_template': version_template,
        'version_scheme': 'post-release'
    },
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    cmdclass={
        'test': PyTest,
        'build_plugin': BuildPlugin,
        'install_plugin': InstallPlugin
    },
    data_files=[
        (
            'ftrack_connect_cinema_4d/hook',
            glob.glob(os.path.join(ROOT_PATH, 'resource', 'hook', '*.py'))
        )
    ],
    python_requires=">=3, <4"
)
