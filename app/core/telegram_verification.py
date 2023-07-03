from urllib.parse import parse_qs
from typing import Dict, List
from decouple import config
import hashlib
import hmac
import time

# Get your secret key from the environment variables
SECRET_KEY = config('SECRET_KEY')


def parse_telegram_data(data: str) -> Dict[str, List[str]]:
    return parse_qs(data)


def verify_telegram_data(telegram_data: str) -> bool:
    data_dict = parse_telegram_data(telegram_data)

    # Check the data includes the required parameters
    required_params = {'auth_date', 'query_id', 'user', 'hash'}
    if not required_params.issubset(data_dict.keys()):
        return False

    # Check that the auth_date is not too old
    if time.time() - int(data_dict['auth_date'][0]) > 86400:
        return False

    # Create the data_check_string
    data_check_string = '\n'.join(f'{k}={v[0]}' for k, v in sorted(data_dict.items()) if k != 'hash') + '\n'

    # Create a HMAC-SHA256 hash of the data_check_string
    data_hash = hmac.new(SECRET_KEY.encode(), data_check_string.encode(), hashlib.sha256).hexdigest()

    # Check that the hash matches
    if data_hash != data_dict['hash'][0]:
        return False

    return True
