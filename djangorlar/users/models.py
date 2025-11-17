from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
#Custom user manager
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames."""

    def create_user(self, email, password, **extra_fields):
        """Create and save a user with the given email and password."""
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using =self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """ Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        extra_fields.setdefault('role', 'admin') # Set role to 'admin' for superuser

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)
    

# Custom user model
class CustomUser(AbstractUser):
    """ Standard User model with email as username field."""
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, blank=True, null=True)

    #Custom fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='employee')

    birth_date = models.DateField(blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Use email as the USERNAME_FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username'] # fields required when creating a superuser

    objects = CustomUserManager()

    def __str__(self):
        return self.email