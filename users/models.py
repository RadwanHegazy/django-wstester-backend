from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser

class UserManager (BaseUserManager) : 
    def create_user (self, password, **kwargs) : 
        user = self.model(**kwargs)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, **kwargs) : 
        kwargs['is_superuser'] = True
        kwargs['is_staff'] = True
        return self.create_user(**kwargs)
    

class User (AbstractUser) : 
    objects = UserManager()
    first_name = None
    last_name = None
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=225)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self) -> str:
        return self.full_name
    
