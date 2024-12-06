import os
from functools import cached_property
from typing import Any, Dict

from synapse_sdk.clients.backend import BackendClient
from synapse_sdk.loggers import BackendLogger, ConsoleLogger
from synapse_sdk.plugins.utils import read_plugin_config
from synapse_sdk.utils.storage import get_storage
from synapse_sdk.utils.string import hash_text


class PluginRelease:
    config: Dict[str, Any]

    def __init__(self, config=None, plugin_path=None):
        if config:
            self.config = config
        else:
            self.config = read_plugin_config(plugin_path=plugin_path)

    @cached_property
    def plugin(self):
        return self.config['code']

    @cached_property
    def version(self):
        return self.config['version']

    @cached_property
    def code(self):
        return f'{self.plugin}@{self.version}'

    @cached_property
    def category(self):
        return self.config['category']

    @cached_property
    def name(self):
        return self.config['name']

    @cached_property
    def checksum(self):
        return hash_text(self.code)

    @cached_property
    def actions(self):
        return list(self.config['actions'].keys())

    def setup_runtime_env(self):
        # TODO ray에 해당 plugin release runtime env 캐싱
        pass

    def get_action_config(self, action):
        return self.config['actions'][action]

    def get_url(self, storage_url):
        storage = get_storage(storage_url)
        return storage.get_url(f'{self.checksum}.zip')

    def get_serve_url(self, serve_address, path):
        return os.path.join(serve_address, self.checksum, path)


class Run:
    logger = None
    job_id = None
    context = None

    def __init__(self, job_id, context):
        self.job_id = job_id
        self.context = context
        self.set_logger()

    def set_logger(self):
        if self.job_id:
            client = BackendClient(
                self.context['envs']['SYNAPSE_PLUGIN_RUN_HOST'],
                self.context['envs']['SYNAPSE_PLUGIN_RUN_USER_TOKEN'],
                self.context['envs']['SYNAPSE_PLUGIN_RUN_TENANT'],
            )
            self.logger = BackendLogger(client, self.job_id)
        else:
            self.logger = ConsoleLogger()

    def set_progress(self, current, total, category=''):
        self.logger.set_progress(current, total, category)

    def log(self, action, data):
        self.logger.log(action, data)

    def log_event(self, message):
        self.logger.log('event', {'content': message})

    def end_log(self):
        self.log_event('Plugin run is complete.')
