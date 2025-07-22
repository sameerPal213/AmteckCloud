from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    
    class meta:
        managed = True
        db_table = "Bronze].[accounts_user"
        verbose_name = "user"
        verbose_name_plural = "users"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
