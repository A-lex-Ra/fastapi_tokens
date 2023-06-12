import requests
import json
import os


class Client:
    def __init__(self, server_url: str):
        self._server_url = server_url
        self._login = None
        self._password = None
        self._durability = None

        self.ask_for_input()

    def ask_for_input(self):
        self._login = input('Type your login: ')
        while len(self._login) == 0:
            self._login = input('Type your login: ')

        self._password = input('Type your password: ')
        while len(self._password) == 0:
            self._password = input('Type your password: ')

        while True:
            self._durability = input('Type desired value of token durability (in seconds) or press Enter to continue: ')
            try:
                self._durability = None if self._durability == '' else int(self._durability)
            except ValueError:
                print('Incorrect value! Try again!')
            else:
                break

    # Server interaction example
    def get_secret_token(self, logging: bool = True):
        page_url = 'secret_token'
        params = {
            'login': self._login,
            'password': self._password,
            'durability': self._durability
        }

        response = requests.get(
            os.path.join(self._server_url, page_url),
            params
        )
        if logging:
            print("--- Returned response status code", response.status_code)
        return json.loads(response.text)

    # Server interaction example
    def get_info(self, token: str, logging: bool = True):
        page_url = 'employee_info'
        params = {
            'login': self._login,
            'token': token
        }

        response = requests.get(
            os.path.join(self._server_url, page_url),
            params
        )
        if logging:
            print("--- Returned response status code", response.status_code)
        return json.loads(response.text)


c = Client('http://127.0.0.1:8000/')
print()
# get a secret token
print('Trying to get new token...')
response_dict = c.get_secret_token()
print(response_dict['info'])
if response_dict['success']:
    print('Your token:', response_dict['token'])
    my_token = response_dict['token']
else:
    print('(token not received)')
    my_token = None
print()

# get employee`s wages and advance date
print('Trying to get data...')
if my_token is not None:
    response_dict = c.get_info(my_token)
else:
    response_dict = c.get_info(input('Please, input your token: '))
print(response_dict['info'])
if response_dict['success']:
    print(f'Your wages: {response_dict["data"]["wages"]}\n'
          f'Your advance date: {response_dict["data"]["advance"]}')
print()
