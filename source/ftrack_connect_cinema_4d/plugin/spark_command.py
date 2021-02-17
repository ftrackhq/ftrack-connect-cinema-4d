# :coding: utf-8
# :copyright: Copyright (c) 2015 ftrack

import os
import sys
import logging
import json
import base64
import uuid

import c4d
import c4d.gui
import appdirs

import ftrack_connect_cinema_4d
import ftrack_connect_cinema_4d.event

# ftrack plug in ID
PLUGIN_ID = 1230004

PLUGIN_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(os.path.realpath(__file__)), '..', '..'
    )
)
SPARK_INDEX_FILE_PATH = os.path.join(
    PLUGIN_ROOT, 'ftrack_connect_spark', 'cinema4d', 'index.html'
)

FTRACK_CONNECT_SPARK_URL = os.environ.get(
    'FTRACK_CONNECT_SPARK_URL',
    'file://' + SPARK_INDEX_FILE_PATH
)


class HtmlViewDialog(c4d.gui.GeDialog):
    '''HTML View Dialog'''
    url = None
    htmlview = None

    def __init__(self, url, *args, **kwargs):
        '''Initialize dialog with *url*.'''
        super(HtmlViewDialog, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )
        self.setUrl(url)

    def setUrl(self, url):
        '''Set new *url*.'''
        self.url = url
        if self.htmlview:
            self.htmlview.SetUrl(url, c4d.URL_ENCODING_UTF16)
            self.logger.info('Loading url: {0}'.format(url))

    def CreateLayout(self):
        '''Create dialog layout.'''
        self.SetTitle('ftrack')
        self.GroupBegin(
            id=0,
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            title='',
            rows=1,
            cols=1,
            groupflags=c4d.BORDER_GROUP_IN
        )
        self.GroupBorderSpace(5, 5, 5, 5)
        settings = c4d.BaseContainer()

        self.htmlview = self.AddCustomGui(
            id=1001,
            pluginid=c4d.CUSTOMGUI_HTMLVIEWER,
            name='',
            flags=c4d.BFH_SCALEFIT|c4d.BFV_SCALEFIT,
            minw=200,
            minh=200,
            customdata=settings
        )
        self.htmlview.SetUrl(self.url, c4d.URL_ENCODING_UTF16)

        self.GroupEnd()
        return True


class SparkCommand(c4d.plugins.CommandData):
    '''Publish plugin, open publish dialog on execution.'''

    def __init__(self, *args, **kwargs):
        '''Instantiate the asset options.'''
        super(SparkCommand, self).__init__(*args, **kwargs)

        self.initialized = False
        self._dialog = None
        self._session = None
        self._hub_thread = None
        self._subscription_id = None
        self._url = 'about:blank'

        self.logger = logging.getLogger(
            __name__ + '.' + self.__class__.__name__
        )
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger('ftrack_api').setLevel(logging.WARNING)

    def _initialize(self):
        '''Initialize plugin'''
        self.logger.info('Creating session')
        try:
            import ftrack_api
        except ImportError:
            self.logger.exception('ftrack api import failed.')
            c4d.gui.MessageDialog(
                'Failed to import ftrack API. '
                'Please ensure plugin is properly installed and launched.'
            )
            raise

        # Try to fetch api credentials.
        config_file = os.path.join(
            appdirs.user_data_dir(
                'ftrack-connect', 'ftrack'
            ),
            'config.json'
        )

        config = None
        if os.path.isfile(config_file):
            self.logger.info(u'Reading config from {0}'.format(config_file))

            with open(config_file, 'r') as file:
                try:
                    config = json.load(file)
                except Exception:
                    self.logger.exception(
                        u'Exception reading json config in {0}.'.format(
                            config_file
                        )
                    )

        server_url = None
        api_user = None
        api_key = None

        try:
            credentials = config['accounts'][0]
            server_url = credentials['server_url']
            api_user = credentials['api_user']
            api_key = credentials['api_key']
        except Exception:
            self.logger.error('Failed to parse credentials from config data.')

        try:
            self._session = ftrack_api.Session(
                server_url=server_url, api_user=api_user, api_key=api_key, auto_connect_event_hub=True
            )
        except Exception:
            self.logger.exception('ftrack api session initialization failed.')
            c4d.gui.MessageDialog(
                'Failed to communicate with the ftrack server.'
            )
            raise

        self.logger.info('Subscribing')
        self._subscription_id = ftrack_connect_cinema_4d.event.subscribe(
            self._session
        )
        self.logger.info('Subscription id: {0}'.format(self._subscription_id))

        self.logger.info('Starting event hub')
        self._hub_thread = ftrack_connect_cinema_4d.event.EventHubThread()
        self._hub_thread.daemon = True
        self._hub_thread.start(self._session)

        self._url = self._get_url(self._session, self._subscription_id)
        self.logger.info('URL: {0}'.format(self._url))
        self._dialog = HtmlViewDialog(self._url)

        self.initialized = True

    def _get_url(self, session, subscription_id):
        '''Return URL to spark'''
        options = dict(
            server_url=session.server_url,
            api_key=session.api_key,
            api_user=session.api_user,
            subscription_id=subscription_id,
            host_version=c4d.GetC4DVersion(),
            plugin_version=ftrack_connect_cinema_4d.__version__
        )
        # strip result base of b%27 start chars
        encodedOptions = base64.b64encode(json.dumps(options).encode('utf-8')).decode('utf-8')
        return '{0}?options={1}'.format(FTRACK_CONNECT_SPARK_URL, encodedOptions)

    def Execute(self, doc):
        '''Open dialog when executed.'''
        self.logger.info('Executing command')

        if not self.initialized:
            self._initialize()

        self.logger.info('Opening dialog')
        return self._dialog.Open(
            dlgtype=c4d.DLG_TYPE_ASYNC,
            pluginid=PLUGIN_ID,
            defaulth=640,
            defaultw=480
        )

    def RestoreLayout(self, sec_ref):
        '''Restore dialog when layout changes.'''
        self.logger.info('Restoring layout')

        if not self.initialized:
            self._initialize()

        return self._dialog.Restore(
            pluginid=PLUGIN_ID,
            secret=sec_ref
        )
