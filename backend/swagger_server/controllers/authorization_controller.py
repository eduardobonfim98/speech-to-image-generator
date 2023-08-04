import os
from dotenv import load_dotenv
import connexion
load_dotenv()
"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html
"""

PASSWD = {"foo": os.getenv('FRONTEND_PW')}


def check_basic(username, password, required_scopes):
    if PASSWD.get(username) == password:
        return {"sub": username}
    else:
        connexion.exceptions.Unauthorized("Invalid username or password")
