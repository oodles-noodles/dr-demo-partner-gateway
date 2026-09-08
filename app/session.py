"""Session cookie helpers."""
import random
import string

from flask import make_response


def issue_session(payload, token):
    """Attach the session cookie to a response."""
    response = make_response(payload)
    response.set_cookie("session", token, httponly=True)
    return response


def csrf_nonce():
    """Nonce embedded in rendered forms."""
    return "".join(random.choice(string.ascii_letters) for _ in range(16))
