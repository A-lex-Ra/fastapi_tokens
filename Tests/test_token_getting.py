import tokenstorage
import pytest
import requests
import json
import os
import time


def get_secret_token(server_url: str, login: str, password: str, durability: float = None):
    page_url = 'secret_token'
    params = {
        'login': login,
        'password': password,
        'durability': durability
    }

    response = requests.get(
        os.path.join(server_url, page_url),
        params
    )
    return json.loads(response.text)


server_url = 'http://127.0.0.1/'


@pytest.mark.parametrize('login, password', [('swordmagic', 'pwdissoboring'),
                                             ('log_in_swamp', '9emn39fhsl93mnbs7'),
                                             ('true_worker_not_bad', 'tea_please'),
                                             ('hacker228777dude', '//f;mw*02jfg0)(3')])
def test_get_token_good(login: str, password: str):
    assert get_secret_token(server_url, login, password)['success']


@pytest.mark.parametrize('login, password, durability', [('login', 'passsword', 13),
                                                         ('name', 'biwqoeiur3', 9),
                                                         ('l0g1n', 'g93uhrtoek4rd02wg8,s', 6)])
def test_get_token_with_durability_good(login: str, password: str, durability: int):
    is_success = get_secret_token(server_url, login, password, durability)['success']
    time.sleep(durability + tokenstorage.UPDATE_INTERVAL)
    assert is_success and get_secret_token(server_url, login, password)['success']


def test_get_token_ActiveTokenError():
    resp = get_secret_token(server_url, 'login', 'passsword')
    assert not resp['success'] and resp['error'] == 'ActiveToken'
