from django.db import models
from activity_log.common.models import BaseModel

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from django.contrib.auth.models import BaseUserManager as BUM


class BaseUserManager(BUM):
    def create_user(self, first_name, last_name, email, is_active=True, is_admin=False, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(first_name=first_name, last_name=last_name, email=self.normalize_email(email.lower()),
                          is_active=is_active, is_admin=is_admin)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            is_active=True,
            is_admin=True,
            password=password,
        )

        user.is_superuser = True
        user.save(using=self._db)

        return user


class BaseUser(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email address", unique=True)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "email"

    # Add custom related_name arguments to avoid reverse accessor clashes
    groups = models.ManyToManyField(Group, related_name='baseuser_set_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='baseuser_set_permissions')


    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


class Profile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    posts_count = models.PositiveIntegerField(default=0)
    subscriber_count = models.PositiveIntegerField(default=0)
    subscription_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.user} >> {self.bio}"
