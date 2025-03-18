from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set.")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)
    
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES =  [
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('delivery_boy','Delivery_boy'),
        ('owner', 'Owner')
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True, default='user')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=8, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True,blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_groups",  
        blank=True
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_permissions",  
        blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    def is_complete(self):
        required_fields = {
            "email": self.email,
            "username": self.username

        }
        missing_fields = [field for field, value in required_fields.items() if not value]
        return not missing_fields, missing_fields