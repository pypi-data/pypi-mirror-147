from typing import Any, ClassVar, Union
import os
import logging
import requests
from requests.adapters import HTTPAdapter, Retry
import json
from urllib.parse import urljoin, quote

from credmark.client.errors import ModelBaseError, create_instance_from_error_dict

GATEWAY_API_URL = 'https://gateway.credmark.com'

RUN_MODEL_PATH = '/v1/model/run'
GET_MODELS_PATH = '/v1/models'
GET_MODEL_PATH_FORMAT = '/v1/models/{}'
GET_MODEL_DEPLOYMENTS_PATH_FORMAT = '/v1/models/{}/deployments'


logger = logging.getLogger(__name__)


class CredmarkClient:
    """
    Credmark API client
    """

    def __init__(self, url: Union[str, None] = None, api_key: Union[str, None] = None,
                 model_run_timeout=600):
        """
        Create a client instance that can be used to make
        requests for model metadata and running models.
        """
        self.__url = url if url is not None else GATEWAY_API_URL
        self.__api_key = api_key if api_key is not None else os.environ.get('CREDMARK_API_KEY')
        self.model_run_timeout = model_run_timeout
        self.__session = requests.Session()
        self.__session.headers.update({'User-Agent': 'credmark-client'})
        if self.__api_key:
            self.__session.headers.update({'Authorization': 'Bearer ' + self.__api_key})

        retries = Retry(total=5, backoff_factor=1, method_whitelist=None,
                        status_forcelist=[429, 502], respect_retry_after_header=True)
        self.__session.mount('http://', HTTPAdapter(max_retries=retries))
        self.__session.mount('https://', HTTPAdapter(max_retries=retries))

    def _get(self, url):
        """
        Return JSON object or None if not found.
        Other errors raise
        """
        resp = None

        try:
            resp = self.__session.get(url)
            resp.raise_for_status()
            return resp.json()
        except requests.exceptions.ConnectionError as err:
            logger.error(
                f'Error running api request for {url}: {err}')
            raise
        except Exception as err:
            if resp is not None:
                logger.error(f'Error api response {resp.status_code} {resp.text}')
            else:
                logger.error(f'Error running api request for {url}: {err}')
            raise
        finally:
            # Ensure the response is closed in case we ever don't
            # read the content.
            if resp is not None:
                resp.close()

    def get_models(self):
        """
        Get list of models metadata
        """
        url = urljoin(self.__url, GET_MODELS_PATH)
        models = self._get(url)
        return models if models is not None else []

    def get_model(self, slug: str):
        """
        Get metadata for a model by slug
        """
        path = GET_MODEL_PATH_FORMAT.format(quote(slug))
        url = urljoin(self.__url, path)
        return self._get(url)

    def get_model_deployments(self, slug: str):
        """
        Get deployments metadata for a model slug
        """
        path = GET_MODEL_DEPLOYMENTS_PATH_FORMAT.format(quote(slug))
        url = urljoin(self.__url, path)
        return self._get(url)

    def run_model(self,  # pylint: disable=too-many-arguments,too-many-locals,too-many-branches
                  slug: str,
                  chain_id: int = 1,
                  block_number: Union[int, str] = 'latest',
                  input: Union[dict, None] = None,
                  raise_error_results=False,
                  version: Union[str, None] = None
                  ) -> dict[str, Any]:
        """
        Run a model
        """
        req = {
            'slug': slug,
            'chainId': chain_id,
            'blockNumber': block_number,
            'input': input if input is not None else {}
        }
        if version is not None:
            req['version'] = version

        resp = None
        resp_obj = None
        url = urljoin(self.__url, RUN_MODEL_PATH)
        try:
            resp = self.__session.post(url, json=req, timeout=self.model_run_timeout)
            resp.raise_for_status()
            resp_obj = resp.json()

            if raise_error_results:
                err_obj = resp_obj.get('error')
                if err_obj is not None:
                    raise create_instance_from_error_dict(err_obj)

            return resp_obj

        except ModelBaseError:
            raise

        except Exception as err:
            logger.error(
                f'Error running api request for {slug} {self.__url}: '
                f'{err} {resp.text if resp else "(no response)"}')
            raise

        finally:
            # Ensure the response is closed in case we ever don't
            # read the content.
            if resp is not None:
                resp.close()
