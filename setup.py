# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import re
import shutil
import pip

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import setuptools.command.build_py


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


class BuildPlugin(setuptools.command.build_py.build_py):
    '''Build plugin.'''

    def run(self):
        '''Run the build step.'''
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
                [
                    'install',
                    module,
                    '--target',
                    os.path.join(STAGING_PATH, 'ftrack', 'dependencies')
                ]
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
        'sphinx_rtd_theme >= 0.1.6, < 2'
    ],
    install_requires=[
    ],
    tests_require=[
        'pytest >= 2.3.5, < 3'
    ],
    cmdclass={
        'test': PyTest,
        'build_py': BuildPlugin
    }
)
