import time
from functools import wraps

from utils.utils import is_token_expired, refresh_omnicomm


def refresh_jwt_if_needed():
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Assuming self.token is the current JWT and self.token_expiry is the expiry timestamp
            token_expiry = is_token_expired(self.auth_data)
            if token_expiry:
                print("Refreshing JWT token...")
                refresh_omnicomm(self.auth_data)
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
