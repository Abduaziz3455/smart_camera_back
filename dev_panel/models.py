from django.contrib.auth.models import AbstractUser
from django.db.models import *


class Organization(Model):
    name = CharField(max_length=255)
    brand_name = CharField(max_length=255)
    subscription_ends_date = DateField()
    status = BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'organization'
