__author__ = 'Andrey Komissarov'
__email__ = 'andrey.komissarov@starwind.com'
__date__ = '2020.03'

import time
from dataclasses import dataclass
from typing import Union
from urllib.parse import urljoin

import plogger
import requests


@dataclass
class TCRestClient:
    """Main class to interact with the TeamCity server through REST API

    https://www.jetbrains.com/help/teamcity/rest-api-reference.html
    """

    base_url: str
    token: str
    logger_enabled: bool = True

    def __post_init__(self):
        self.header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        self.logger = plogger.logger(self.__class__.__name__, enabled=self.logger_enabled)

    def get_server_info(self):
        # /app/rest/server

        url = self._create_url('projects')
        self.logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_all_build_types(self):
        # /app/rest/buildTypes

        url = self._create_url('buildTypes')
        self.logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_build_types_info(self, uid: str):
        """

        :param uid: BuildType ID (VeeamBackupAgent_Update, Voodoo_SetConfigWithL1andL2 etc)
        :return:
        """

        base = self._create_url('buildTypes')
        url = f'{base}/id:{uid}'
        self.logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_build_types_steps(self, uid: str):
        """

        :param uid: BuildType ID (VeeamBackupAgent_Update, Voodoo_SetConfigWithL1andL2 etc)
        :return:
        """

        base = self._create_url('buildTypes')
        url = f'{base}/id:{uid}/steps'
        self.logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def get_all_projects(self):

        url = self._create_url('projects')
        self.logger.info(f'GET | {url}')
        return requests.get(url, headers=self.header)

    def get_project_info(self, uid: str):
        """

        :param uid: ID
        :return:
        """

        base = self._create_url('projects')
        url = f'{base}/id:{uid}'

        self.logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def run_build_types(self, uid: str, comment: str = None):
        """

        :param uid: BuildType ID (VeeamBackupAgent_Update, Voodoo_SetConfigWithL1andL2 etc)
        :param comment:
        :return:
        """

        url = self._create_url('buildQueue')

        comment_ = comment if comment is not None else 'API BOT did it...'
        data = {
            'buildType': {
                'id': uid
            },
            'comment': {
                'text': comment_
            }
        }

        self.logger.info(f'POST | {url}')

        return requests.post(url, headers=self.header, json=data)

    def get_queued_build(self, uid: str):
        # [GET] http://<TeamCity Server host>:<port>/app/rest/buildQueue?locator=<BuildQueueLocator>

        url = self._create_url('buildQueue')
        params = {
            'locator': uid
        }

        self.logger.info(f'GET | {url}, {params = }')

        return requests.get(url, headers=self.header, params=params)

    def get_build_state(self, uid: int):
        # [GET] http://<TeamCity Server host>:<port>/app/rest/buildQueue/XXX

        url = self._create_url(f'buildQueue/id:{uid}')

        self.logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def wait_for_build_completion(self, uid: int):
        response = self.get_build_state(uid)
        state = response.json()['state']
        status = response.json()['status']

        while state == 'running':
            response = self.get_build_state(uid)
            state = response.json()['state']
            status = response.json()['status']
            time.sleep(5)

        self.logger.info(f'WAITING | {state = }, {status = }')
        return status == 'SUCCESS'

    def get_project_parameters(self, uid: str):
        """

        :param uid: Project locator
        :return:
        """

        url = self._create_url(f'projects/{uid}/parameters')

        self.logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def get_project_parameter(self, uid: str, name: str):
        """
        https://www.jetbrains.com/help/teamcity/rest/projectapi.html#getBuildParameter

        :param uid: Project locator
        :param name: Parameter name
        :return:
        """

        url = self._create_url(f'projects/{uid}/parameters/{name}')

        self.logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def set_project_parameter(self, uid: str, parameter: str, value: Union[str, bool]):
        """Update build parameters.

        :param uid: Project locator
        :param parameter:
        :param value:
        :return:
        """

        data = {
            'value': value
        }

        url = self._create_url(f'projects/{uid}/parameters/{parameter}')

        self.logger.info(f'PUT | {url}')

        return requests.put(url, headers=self.header, json=data)

    def get_bt_parameter(self, uid: str):
        """Get configuration's parameters

        :param uid: BuildType locator
        :return:
        """

        url = self._create_url(f'buildTypes/id:{uid}/parameters')

        self.logger.info(f'GET | {url}')

        return requests.get(url, headers=self.header)

    def _create_url(self, url: str):
        """Create full URL

        :param url:
        :return:
        """

        base = f'{self.base_url}/app/rest/'
        return urljoin(base=base, url=url)
