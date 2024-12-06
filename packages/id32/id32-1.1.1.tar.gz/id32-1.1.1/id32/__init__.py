import secrets

def id32():
    return "".join("abcdefghijklmnopqrstuvwxyz234567"[b & 31] for b in secrets.token_bytes(32))

__all__ = ['id32']