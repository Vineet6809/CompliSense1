"""Security behaviors: changing a password or session must invalidate access."""

from app.security import hash_password, verify_password


def test_password_hash_does_not_store_password_and_checks_correct_value():
    encoded = hash_password("a-long-test-password")
    assert "a-long-test-password" not in encoded
    assert verify_password("a-long-test-password", encoded)
    assert not verify_password("wrong-password", encoded)


def test_each_password_hash_uses_a_new_salt():
    assert hash_password("same-password") != hash_password("same-password")


def test_invalid_hash_is_rejected_without_crashing():
    assert not verify_password("password", "not-a-valid-hash")
