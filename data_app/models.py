from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class UserLoginManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = extra_fields.get('is_active', 1)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', 1)
        extra_fields.setdefault('is_active', 1)
        user = self.create_user(email, password, **extra_fields)
        return user


class UserLogin(AbstractBaseUser, PermissionsMixin):
    id =  models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=10)
    email = models.CharField(unique=True, max_length=255)
    user = models.CharField(max_length=45)
    is_active = models.IntegerField(default=1)
    is_superuser = models.IntegerField(default=0)
    last_login = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=150)
    created_at = models.DateTimeField(default=timezone.now)
    created_by = models.CharField(max_length=255)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=255, blank=True, null=True)

    objects = UserLoginManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    class Meta:
        managed = False  # because the table already exists
        db_table = 'user_login'

    @property
    def is_staff(self):
        return self.is_superuser == 1

    def has_perm(self, perm, obj=None):
        return self.is_superuser == 1

    def has_module_perms(self, app_label):
        return self.is_superuser == 1
