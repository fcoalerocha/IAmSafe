from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    state = models.BooleanField( default=False )
    code = models.IntegerField( null=False )
