import uuid
from django.db import models
from django.utils import timezone, crypto
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from backend.models import BaseModel


class CodeGenerator(object):
    allowed_symbols="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789!@#$%^&*()+-=/:;<>.,"
    allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
    allowed_nums="0123456789"

    @classmethod
    def get_nums(self, length=4):
        return crypto.get_random_string(length, self.allowed_nums)
    
    @classmethod
    def get_chars(self, length=6):
        return crypto.get_random_string(length, self.allowed_chars)

    @classmethod
    def get_symbols(self, length):
        return crypto.get_random_string(length, self.allowed_chars)


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, phone, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(phone, password, **other_fields)

    def create_user(self, phone, password, **other_fields):
        if not phone:
            raise ValueError(_('You must provide a phone number'))

        phone = self.normalize_email(phone)
        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(_('phone number'), max_length=12, editable=False, unique=True, null=False, blank=False)
    email = models.EmailField(_('email address'), null=True, blank=True)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now, editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    user_ref = models.CharField(_('Personal reference'), default=CodeGenerator.get_chars, editable=False, max_length=6, unique=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone


class SmsCode(models.Model):
    phone = models.CharField(primary_key=True, max_length=12)
    code = models.CharField(default=CodeGenerator.get_nums, editable=False, max_length=4)

    def __str__(self) -> str:
        return self.code + ' for ' + self.phone


class Referal(BaseModel):
    parent_user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='parent')
    child_user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name='child')

    def __str__(self) -> str:
        return self.parent_user.__str__() + ' to ' + self.child_user.__str__()

