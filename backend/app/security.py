"""Salted password hashes and opaque sessions; no password is stored in plain text."""

import hashlib
import hmac
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.scrypt(password.encode(), salt=salt.encode(), n=32768, r=8, p=1, maxmem=67108864)
    return f"scrypt${salt}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, salt, expected = encoded.split("$")
        if algorithm != "scrypt" or len(salt) != 32 or len(expected) != 128:
            return False
        actual = hashlib.scrypt(password.encode(), salt=salt.encode(), n=32768, r=8, p=1, maxmem=67108864)
        return hmac.compare_digest(actual.hex(), expected)
    except (ValueError, TypeError):
        return False


def token_hash(token: str) -> str:
    """The database stores a session fingerprint, not the usable cookie value."""
    return hashlib.sha256(token.encode()).hexdigest()
