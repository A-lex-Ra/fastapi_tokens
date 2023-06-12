import secrets
from time import time
from hashlib import sha3_256
from setintervaldecorator import set_interval
from prettytable import PrettyTable

DEFAULT_TOKEN_DURABILITY = 72 * 60 * 60  # in seconds
CONSOLE_LOGGING = False
UPDATE_INTERVAL = 2


class TokenHash:
    def __init__(self, hash: str, creation_time: float, durability: float = DEFAULT_TOKEN_DURABILITY):
        self.hash = hash
        self.creation_time = creation_time
        self.durability = durability

        # Making of inactive token is forbidden
        self.is_active = True

    def __str__(self):
        return f'{"  Active" if self.is_active else "Inactive"}, hash: {self.hash}, creation time: {self.creation_time}, ' \
               f'durability: {self.durability}s'


class TokenStorage:

    def __init__(self):
        # Here can be connection to database for storing hashes instead of a dictionary
        self._hash_storage = dict()

        self._init_time = time()
        self._stop_update_event = None
        self.start_updating()

    def start_updating(self):
        if not (self._stop_update_event is None or self._stop_update_event.is_set()):
            raise Exception("start_updating is blocked: Server is already updating.")

        self._stop_update_event = self._update_activity_values()

    def stop_updating(self):
        if self._stop_update_event is None or self._stop_update_event.is_set():
            raise Exception("stop_updating is blocked: Server is not updating yet.")

        self._stop_update_event.set()

    def make_new_token(self, login: str, durability: float = None):
        new_token = secrets.token_urlsafe(32)

        if durability is not None and durability >= 0:
            self._set_hash_associated_with(
                TokenHash(
                    sha3_256(new_token.encode()).hexdigest(),
                    time(),
                    durability
                ),
                login
            )
        else:
            self._set_hash_associated_with(
                TokenHash(
                    sha3_256(new_token.encode()).hexdigest(),
                    time()
                ),
                login
            )
        return new_token

    def _set_hash_associated_with(self, tokenhash: TokenHash, login: str):
        # Here can be work with database instead of a dictionary
        self._hash_storage[login] = tokenhash

    def _get_hash_associated_with(self, login: str):
        # Here can be work with database instead of a dictionary
        return self._hash_storage[login].hash

    def associated_token_exists(self, login: str):
        # Here can be work with database instead of a dictionary
        return login in self._hash_storage

    def user_has_active_token(self, login: str):
        # Here can be work with database instead of a dictionary
        return self.associated_token_exists(login) and self._hash_storage[login].is_active

    def check_token_matching(self, login: str, token: str):
        if self.user_has_active_token(login):
            return secrets.compare_digest(
                self._get_hash_associated_with(login),
                sha3_256(token.encode()).hexdigest()
            )

        return False

    @set_interval(UPDATE_INTERVAL)
    def _update_activity_values(self):
        if CONSOLE_LOGGING:
            raw_wt = time() - self._init_time
            wt = round(raw_wt)
            print(f'  --- Working time: {wt // 3600}h {wt // 60}m {wt % 60}s --- {round(raw_wt, 6)}s total')
            log = PrettyTable(['Login', 'Token'])

        for login, tokenhash in self._hash_storage.items():
            if tokenhash.creation_time + tokenhash.durability < time():
                tokenhash.is_active = False

            if CONSOLE_LOGGING:
                log.add_row([login, tokenhash])
        if CONSOLE_LOGGING:
            print(log)
