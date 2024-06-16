from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, usercode, name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        if not usercode:
            raise ValueError('The Usercode field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, usercode=usercode, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, usercode, name, password=None):
        user = self.create_user(email, usercode, name, password)
        user.is_admin = True
        user.is_approved = True  
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    name = models.CharField(max_length=255)
    usercode = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['usercode', 'name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
