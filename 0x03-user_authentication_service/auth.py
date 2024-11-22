#!/usr/bin/env python3
"""
    This module returns Hash password
"""
from uuid import uuid4
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    """
        This Hashes the given password using bcrypt
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """
        This Generates a new UUID and
        returns it as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """
        Auth class to interact with the
        authentication database.
    """

    def __init__(self) -> None:
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
            Register a new user and return a user object
            Args:
                email (str): new user's email address
                password (str): new user's password
            Return:
                if no user with given email exists,
                return newly created user
                else raise ValueError
        """
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """
            Validate a user's login credentials and return True
            if they are correct or False if they are not
            Return:
                True if credentials are correct,
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email: str) -> Union[None, str]:
        """
            Return: the session ID. Corresponding to the email,
            generate a new UUID and store it in the database
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id):
        """
            Find user by session ID
                Return: the corresponding User or None
        """
        user = None
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
            Destroy session akes a single user_id integer argument.
                Return: and returns None
        """
        if user_id is None:
            return None
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
            Generate reset password token
                Return: take an email string argument and
                returns a string
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError('User not found')
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
            Reset_token string argument and a password string argument
                Return: None.
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError('Invalid reset token')
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None
        )
