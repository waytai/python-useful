import random

from .getters import get_object_or_none

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import validate_email, ValidationError


def get_random_password(size=7, cadre='abcdehkmnprstuvxyz2345678923456789'):
    """
    Returns the password composed of the easily readable letters and digits
    by default (digits doubled to increase the occurrence).
    """
    random.seed()
    return ''.join(random.choice(cadre) for unused_i in xrange(size))


def get_unique_username(username):
    """
    Returns the first available username with appended numbering
    (started from 2) that is not yet present in the User table.
    """
    assert username
    base = username
    idx = 2
    while True:
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            break
        username = '%s%d' % (base, idx)
        idx += 1
    return username


class EmailLoginModelBackend(ModelBackend):
    """
    Logs the user in using his/her e-mail (case insensitively by default).
    Set up by the following Django setting::

        AUTHENTICATION_BACKENDS = ('useful.django.auth.EmailLoginModelBackend',)

    """
    EMAIL_CASE_SENSITIVE = False

    def get_user_by_email(self, email):
        try:
            validate_email(email)
            if self.EMAIL_CASE_SENSITIVE:
                user = User.objects.get(email__exact=email)
            else:
                user = User.objects.get(email__iexact=email)
        except (User.DoesNotExist, ValidationError):
            user = None

        return user

    def authenticate(self, username=None, password=None):
        user = self.get_user_by_email(username)
        return user if user and user.check_password(password) else None


class UsernameOrEmailLoginModelBackend(EmailLoginModelBackend):
    """
    Tries to identify the given login-name as username or email
    (both case-insensitive by default).
    Set up by the following Django setting::

        AUTHENTICATION_BACKENDS = ('useful.django.auth.UsernameOrEmailLoginModelBackend',)
    """
    USERNAME_CASE_SENSITIVE = False

    def authenticate(self, username=None, password=None):
        if self.USERNAME_CASE_SENSITIVE:
            user = get_object_or_none(User, username__exact=username)
        else:
            user = get_object_or_none(User, username__iexact=username)

        if user is None:
            user = self.get_user_by_email(username)

        return user if user and user.check_password(password) else None