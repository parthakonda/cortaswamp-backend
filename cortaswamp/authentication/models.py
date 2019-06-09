import uuid
from django.db import models
from cortaswamp import enums
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.postgres.fields import JSONField


class UserAccountManager(UserManager):
    def get_by_natural_key(self, username):
        """
        To match against case insensitive
        """
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class User(AbstractBaseUser):
    objects = UserAccountManager()

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(
        help_text='First Name of user', max_length=200, null=True)
    last_name = models.CharField(
        help_text='Last Name of user', max_length=200, null=True)
    username = models.CharField(
        help_text='Username for the user',
        max_length=200,
        null=False,
        unique=True)
    email = models.EmailField(
        help_text='Email of the user', max_length=200, null=False, unique=True)
    login_attempts = models.IntegerField(
        help_text='To track no of invalid login attempts', default=0)

    USERNAME_FIELD = 'email'

    class Meta:
        db_table = 'user'


class ForgotPassword(models.Model):
    """
    To maintain all the password reset links
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        help_text='Email of the user', max_length=200, null=False)
    valid_upto = models.DateTimeField(
        help_text='DateTime valid upto', null=False)
    expired = models.BooleanField(
        help_text='If True - Link can not be used, False - Link can be used',
        default=False)
    created_on = models.DateTimeField(
        help_text='Reset link creation date', auto_now_add=True)

    class Meta:
        db_table = 'forgot_password'
