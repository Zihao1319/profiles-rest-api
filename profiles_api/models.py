from signal import default_int_handler
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager

# Create your models here.


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, name, password=None):
        """create a new user profile"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        #django will automatically encrypt the password, 
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        #is_superuser is automatically created by permissionsmixin
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    #overriding the default function as they uses username as part of the authentication
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=["name"]

    #because we are defining a function in the class itself, we need the self:
    def get_full_name(self):
        """retrieve full name of user"""
        return self.name
    
    def get_short_name(self):
        return self.name

    def __str__(self):
        """return string representation of our user"""
        return self.email
