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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Implement an is_valid function
    """
    # 'utf-8' converts the string into a byte
    #   representation using UTF-8 encoding.
    # ensures that the password string
    #   is correctly converted into a sequence of bytes.
    # because:bcrypt.checkpw function expects
    #    both the plain text password and the
    #   hashed password to be in bytes.
    is_true = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    return is_true
