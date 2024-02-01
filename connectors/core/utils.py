""" Copyright start
  Copyright (C) 2008 - 2024 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """
import ast
import json
import requests
import logging

from connectors.core.connector import ConnectorError
from connectors.core.constants import SSL_VALIDATION_ERROR, REQUEST_READ_TIMEOUT, CONNECTION_TIMEOUT, \
    INVALID_URL_OR_CREDENTIALS, UNAUTHORIZED

logger = logging.getLogger(__name__)


def api_health_check(url, method='GET', params=None, body='', headers=None, verify=True,
                     username='', password='', auth_config=None, *args, **kwargs):
    """
    This method can be used to make any generic api call to check health of the api.

    """
    return _api_call(url, method, params, body, headers, verify, username,
                     password, auth_config, *args, **kwargs)


api_health_check.__str__ = lambda: 'Makes Simple Http API Call'


def update_connnector_config(connector_name=None, version=None, updated_config={}, configId=None, agent=None):
    pass


def get_updated_config(configurations, updated_config, configId):
    prev_config = configurations.get('config', None)
    if prev_config:
        newly_added_configs = {k: v for k, v in updated_config.items() if k not in prev_config}
        removed_config = {k: v for k, v in prev_config.items() if k not in updated_config}
        update_config = {k: v for k, v in updated_config.items() if k in prev_config}
        newly_added_configs.update(removed_config)
        newly_added_configs.update(update_config)
        configurations['config'] = newly_added_configs
        return configurations
    else:
        raise ValueError("No configuration found to update. Please config_id or mark a configuration to default")


def _api_call(url, method='GET', params=None, body='', headers=None, verify=True,
              username='', password='', auth_config=None, *args, **kwargs):
    if auth_config:
        auth = (auth_config['username'], auth_config['password'])
    elif username or password:
        auth = (username, password)
    else:
        auth = None

    verify = _convert_verify(verify)

    # build **args for requests call
    request_args = {
        'verify': verify,
    }
    if auth:
        request_args['auth'] = auth
    if params:
        request_args['params'] = params
    if headers:
        request_args['headers'] = headers

    # get rid of the body on GET/HEAD requests
    bodyless_methods = ['head', 'get']
    if method.lower() not in bodyless_methods:
        request_args['data'] = _convert_body(body)

    # actual requests call
    try:
        logger.info('Starting Check health Request: Method %s, Url: %s', method, url)
        response = requests.request(method, url, **request_args)
    except requests.exceptions.SSLError:
        raise ConnectorError('%s for url %s' % (SSL_VALIDATION_ERROR, url))
    except requests.exceptions.ConnectTimeout:
        raise ConnectorError('%s for url %s' % (CONNECTION_TIMEOUT, url))
    except requests.exceptions.ReadTimeout:
        raise ConnectorError('%s for url %s' % (REQUEST_READ_TIMEOUT, url))
    except requests.exceptions.ConnectionError:
        raise ConnectorError('%s for url %s' % (INVALID_URL_OR_CREDENTIALS, url))
    except Exception as e:
        raise ConnectorError(str(e))

    if response.ok:
        return response
    elif response.status_code == 401:
        raise ConnectorError('%s for url %s' % (INVALID_URL_OR_CREDENTIALS, url))
    elif response.status_code == 403:
        raise ConnectorError('%s for url %s' % (UNAUTHORIZED, url))
    else:
        msg = ''
        try:
            msg = response.json()
        except Exception:
            pass
        if not msg:
            try:
                msg = response.text
            except Exception:
                pass
        if not msg:
            try:
                msg = response.content
            except Exception:
                pass
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            msg = '{} :: {} Url: {}'.format(str(e), msg, url)
            raise ConnectorError(msg)


# type conversions :\
def _convert_verify(verify):
    if type(verify) == str and verify:
        try:
            verify = ast.literal_eval(verify.title())
        except Exception as e:
            logger.warn('Str verification failed. %s', str(e))
    if type(verify) != bool:
        # just default to true
        return True
    return verify


def _convert_body(body):
    if body and type(body) == str:
        try:
            logger.info('converting body into json %s', body)
            body = json.loads(body, strict=False)
        except:
            logger.warn('Json conversion failed.')

    if body and type(body) != str:
        body = json.dumps(body)
    return body
