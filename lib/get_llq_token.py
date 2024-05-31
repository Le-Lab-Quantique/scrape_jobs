from typing import NewType
import requests
from .exceptions import NoLLQJWTTokenException
from .utils import base_url
import sys
import logging

BearerToken = NewType("BearerToken", str)


def _get_credentials() -> dict[str, str]:
    return {
        "username": sys.argv[1],
        "password": sys.argv[2],
    }


def get_token() -> BearerToken:
    url = f"{base_url}/wp-json/jwt-auth/v1/token"
    response = requests.post(
        url,
        json=_get_credentials(),
        headers={"Content-Type": "application/json"},
    )
    if response.status_code == 200:
        token = response.json()["token"]
        return BearerToken(f"Bearer {token}")
    else:
        username = _get_credentials()["username"]
        logging.error(
            f"Failed to get LLQ JWT Token for {username}. \nStatus code : {response.status_code} {_get_credentials()} {response.json()}"
        )
        raise NoLLQJWTTokenException(
            f"Failed to get LLQ JWT Token for {username}. \nStatus code : {response.status_code} {_get_credentials()} {response.json()}"
        )
