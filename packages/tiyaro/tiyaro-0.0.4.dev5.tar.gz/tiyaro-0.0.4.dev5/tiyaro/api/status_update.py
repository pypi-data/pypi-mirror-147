import requests

from ..common.constants import STATUS_UPDATE_ENDPOINT_PREFIX, TIYARO_TOKEN, MODEL_VERSION
from ..common.utils import get_tiyaro_token, failed

C_STATUS_INIT = 'init'
C_STATUS_TEST_FAILED = 'test_failed'
C_STATUS_TEST_PASSED = 'test_passed'
C_STATUS_PUSH = 'pushed'
C_STATUS = 'status'

STATUS_UPDATE_API = '{}/{}/{}'

def update_status_init(model_name):
    _update_status(C_STATUS_INIT, model_name)
    pass


def update_status_test_passed(model_name):
    _update_status(C_STATUS_TEST_PASSED, model_name)
    pass


def update_status_test_failed(model_name):
    _update_status(C_STATUS_TEST_FAILED, model_name)
    pass


def update_status_pushed(model_name):
    _update_status(C_STATUS_PUSH, model_name)
    pass

def _update_status(status, name):
    url = STATUS_UPDATE_API.format(
        STATUS_UPDATE_ENDPOINT_PREFIX, name, MODEL_VERSION)
    token = get_tiyaro_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    body = {}
    body[C_STATUS] = status
    resp = requests.post(url, json=body, headers=headers)
    if resp.status_code == 401:
        failed(
            f'Token Authorization Error.  Is your {TIYARO_TOKEN} still valid ?')
        exit(-1)
    if resp.status_code != 200:
        failed(f'Unable to udpate status: {resp.content}')
