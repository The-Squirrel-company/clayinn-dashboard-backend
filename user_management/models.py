import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from location_management.models import Location

def generate_user_id(role):
    return f"{role}-{uuid.uuid4().hex[:5]}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, role, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user_id = extra_fields.get('user_id') or generate_user_id(role)
        user = self.model(user_id=user_id, email=email, name=name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, name, 'super-admin', password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('super-admin', 'Super Admin'),
        ('location-admin', 'Location Admin'),
        ('sales-person', 'Sales Person'),
    ]

    user_id = models.CharField(max_length=20, primary_key=True, editable=False, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales-person')
    mobile = models.CharField(max_length=15, blank=True, null=True)
    loc_id = models.ForeignKey('location_management.Location', to_field='loc_id', on_delete=models.SET_NULL, null=True, blank=True, related_name='users')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.role}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = generate_user_id(self.role)
        super().save(*args, **kwargs)
