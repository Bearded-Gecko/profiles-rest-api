from django.db import models
from django.contrib.auth.models import AbstractBaseUser #needed to customize/overwrite the default user django model
from django.contrib.auth.models import PermissionsMixin #needed to customize/overwrite the default user django model
from django.contrib.auth.models import BaseUserManager
from django.conf import settings #used to retrieve settings.py from djangoproject settings


class UserProfileManager(BaseUserManager): #so django knows how to work with the custom userprofile class
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address') #make sure proper email address value has been passed in

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password) #we use set_password to encrypt it, it is converted to hash and not in plain text
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

# Create your models here.
class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager() #custom profile manager

    USERNAME_FIELD = 'email' #to customize default username in django; field is required by default
    REQUIRED_FIELDS = ['name'] #additional required fields

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrive short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email

class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey( #profile that owns or created the user profile feed item
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE #on delete tells db what to do when remote field is deleted; cascades changes down the field, i.e., if user is deleted it cascades to their feed items
    )
    status_text = models.CharField(max_length=255) #status update or content of the feed item
    created_on = models.DateTimeField(auto_now_add=True) #automatically set to current time when item was created

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
