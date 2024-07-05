#!/usr/bin/env python3
"""
Password Encryption Module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt"""
    x = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), x)
    return hashed_pass
