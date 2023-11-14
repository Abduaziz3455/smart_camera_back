from django.contrib.auth.models import AbstractUser
from django.db.models import *


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        db_table = 'users'


class Client(Model):
    name = CharField(max_length=255, unique=True)
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
    image = ImageField(upload_to='clients/', blank=True)
    last_image = ImageField(upload_to='last_images/', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'client'


class Employee(Model):
    name = CharField(max_length=255)
    image = ImageField(upload_to='employees/', blank=True)
    last_image = ImageField(upload_to='last_images/', blank=True)
    status = BooleanField(default=True)
    created_time = DateTimeField(auto_now_add=True)
    last_enter_time = DateTimeField(auto_now_add=True)
    last_leave_time = DateTimeField(auto_now_add=True)
    stay_time = IntegerField(default=0)
    date = DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'employee'


class EmployeeTime(Model):
    employee = ForeignKey(Employee, on_delete=CASCADE)
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
