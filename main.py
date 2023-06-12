from fastapi import FastAPI
from tokenstorage import TokenStorage
import employeeinfo

app = FastAPI()
tokens = TokenStorage()

INFO_STRING = f'The RESTful service made by A-lex-Ra.\n' \
              f'There is 2 resources (GET /secret_token, GET /employee_info),\n' \
              f'pyShell client for test and some autotests.'
@app.get('/')
def read_root():
    return {'info': INFO_STRING}


@app.get('/secret_token')
def get_secret_token(login: str, password: str, durability: float = None):
    if not employeeinfo.check_auth_validity(login, password):
        return {
            'info': 'Incorrect email address or password.',
            'success': False,
            'error': 'AuthError'
        }
    if tokens.user_has_active_token(login):
        return {
            'info': 'You already have an active token.',
            'success': False,
            'error': 'ActiveToken'
        }

    token = tokens.make_new_token(login, durability)
    return {
        'info': 'Token created successfully.',
        'success': True,
        'token': token
    }


@app.get('/employee_info')
def get_employee_info(login: str, token: str):
    if not tokens.user_has_active_token(login):
        return {
            'info': 'You don`t have an active token yet or previous token has expired. You need to get a new token.',
            'success': False,
            'error': 'InactiveToken'
        }
    if not tokens.check_token_matching(login, token):
        return {
            'info': 'Incorrect token.',
            'success': False,
            'error': 'IncorrectToken'
        }

    employee_info = employeeinfo.get_info_about(login)
    return {
        'info': 'Information received successfully.',
        'success': True,
        'data': employee_info
    }
