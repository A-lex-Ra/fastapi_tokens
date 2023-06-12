import tokenstorage
from test_token_getting import get_secret_token, server_url
import pytest
import requests
import json
import os
import time


def get_info(server_url: str, login: str, token: str):
    page_url = 'employee_info'
    params = {
        'login': login,
        'token': token
    }

    response = requests.get(
        os.path.join(server_url, page_url),
        params
    )
    return json.loads(response.text)


@pytest.mark.parametrize('login, password', [('very_cool_login_that_i_like', 'very_cool_pwd'),
                                             ('never_gonna_give_you_up', 'never_gonna_let_you_down'),
                                             ('never_gonna_run_around', 'and desert you')])
def test_data_getting_good(login: str, password: str):
    # Correct token
    token = get_secret_token(server_url, login, password)['token']
    assert get_info(server_url, login, token)['success']


@pytest.mark.parametrize('login, password', [('very_cool_login_that_i_like', 'very_cool_pwd'),
                                             ('never_gonna_give_you_up', 'never_gonna_let_you_down'),
                                             ('never_gonna_run_around', 'and desert you')])
def test_data_getting_IncorrectTokenError(login: str, password: str):
    # Empty token
    resp = get_info(server_url, login, '')
    assert not resp['success'] and resp['error'] == 'IncorrectToken'

    # Wrong token
    new_token_for_new_login = get_secret_token(server_url, login[:-1], password[:-1])['token']
    resp = get_info(server_url, login[:-1], new_token_for_new_login[:-1])
    assert not resp['success'] and resp['error'] == 'IncorrectToken'


@pytest.mark.parametrize('login, password', [('x', 'yo'),
                                             ('y', 'ox'),
                                             ('z', 'zzz')])
def test_data_getting_InactiveTokenError(login: str, password: str):
    # Waits for inactive token from durability 0
    inactive_token = get_secret_token(server_url, login, password, 0)['token']
    time.sleep(tokenstorage.UPDATE_INTERVAL)

    resp = get_info(server_url, login, inactive_token)
    assert not resp['success'] and resp['error'] == 'InactiveToken'