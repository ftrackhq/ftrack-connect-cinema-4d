# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import os.path
import re
import shutil
import pip
import glob

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import setuptools
import setuptools.command.build_py
import distutils.log


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

README_PATH = os.path.join(ROOT_PATH, 'README.rst')

with open(os.path.join(
    SOURCE_PATH, 'ftrack_connect_cinema_4d', '_version.py')
) as _version_file:
    VERSION = re.match(
        r'.*__version__ = \'(.*?)\'', _version_file.read(), re.DOTALL
    ).group(1)


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
        try:
            shutil.copytree(
                os.environ['FTRACK_CONNECT_SPARK_DIST_DIR'],
                os.path.join(STAGING_PATH, 'ftrack', 'ftrack_connect_spark')
            )
        except KeyError:
            raise ValueError(
                'Please set the environment variable '
                '`FTRACK_CONNECT_SPARK_DIST_DIR` to the directory contining '
                'the distribution files for ftrack-connect-spark.'
            )

        # Add dependencies.
        modules = ('appdirs>=1.4.3,<2', 'ftrack-python-api>=1.1.0,<2')
        for module in modules:
            pip.main(
                [
                    'install',
                    '--ignore-installed',
                    module,
                    '--target',
                    os.path.join(STAGING_PATH, 'ftrack', 'dependencies')
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


# Configuration.
setup(
    name='ftrack connect Cinema 4D',
    version=VERSION,
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
        'lowdown >= 0.1.0, < 1'
    ],
    install_requires=[
    ],
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    dependency_links=[
        (
            'https://bitbucket.org/ftrack/lowdown/get/0.1.0.zip'
            '#egg=lowdown-0.1.0'
        )
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
    ]
)
