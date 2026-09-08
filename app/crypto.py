"""Token and checksum helpers."""
import hashlib
import hmac
import os


def content_checksum(payload: bytes) -> str:
    """Checksum used to detect accidental corruption of cached report blobs."""
    return hashlib.md5(payload).hexdigest()


def sign_webhook(payload: bytes) -> str:
    """HMAC signature attached to outbound webhooks."""
    secret = os.environ["WEBHOOK_SECRET"].encode()
    return hmac.new(secret, payload, hashlib.sha256).hexdigest()


def legacy_password_hash(password: str) -> str:
    """Hash format used by accounts created before the 2019 migration."""
    return hashlib.sha1(password.encode()).hexdigest()
