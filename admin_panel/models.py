from django.contrib.auth.models import AbstractUser
from django.db.models import *
from dev_panel.models import Organization
from uuid import uuid4
# admin_paneldagi user va dev_paneldagi admin


class CustomUser(AbstractUser):
    first_name = None
    last_name = None
    groups = None
    email = None
    is_active = BooleanField(default=True)
    avatar = ImageField(upload_to='users/', blank=True)
    full_name = CharField(max_length=255, blank=True)
    phone = CharField(max_length=255, null=True)
    organization = ForeignKey(Organization, on_delete=CASCADE, null=True)  

    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'


class ClientEmployee(Model):
    id_name = UUIDField(primary_key=True, default=uuid4, editable=False)
    name = CharField(max_length=255)
    phone = CharField(max_length=255, null=True)
    status = BooleanField(default=True)
    array_bytes = BinaryField(null=True, editable=True)
    is_client = BooleanField(default=False)
    created_time = DateTimeField(auto_now_add=True)
    last_time = DateTimeField(auto_now=True)
    last_enter_time = DateTimeField(auto_now_add=True)
    last_leave_time = DateTimeField(auto_now_add=True)
    enter_count = IntegerField(default=0)
    leave_count = IntegerField(default=0)
    stay_time = IntegerField(default=0)
    image = ImageField(upload_to='employees/images', blank=True)
    last_image = ImageField(upload_to='employees/last_images/', blank=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.is_client:
            self._meta.get_field('image').upload_to = 'clients/images'
            self._meta.get_field('last_image').upload_to = 'clients/last_images'

            #self.image.path = 'clients/images'
            #self.last_image.path = 'clients/last_images'
        super().save(*args, **kwargs)        

    class Meta:
        db_table = 'client'


class ClientEmployeeTime(Model):
    employee = ForeignKey(ClientEmployee, on_delete=CASCADE)
    created_time = DateTimeField(auto_now_add=True)
    last_enter_time = DateTimeField(auto_now_add=True)
    last_leave_time = DateTimeField(auto_now_add=True)
    stay_time = IntegerField(default=0)
    date = DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.employee.name} - {self.date}"
    
    class Meta:
        db_table = 'employee_time'


class Camera(Model):
    name = CharField(max_length=255)
    ip_address = CharField(max_length=16)
    login = CharField(max_length=128)
    parol = CharField(max_length=128)
    is_enter = BooleanField(default=True)
    last_time = DateTimeField(auto_now=True)
    created_time = DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'camera'
