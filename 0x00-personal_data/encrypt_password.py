#!/usr/bin/env python3
"""
    This module encrypts passwords.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
        This Hashes a password using a random salt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

