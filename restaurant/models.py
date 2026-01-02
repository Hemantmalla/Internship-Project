from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# --- waiter registration start ---
class waiter(models.Model):
    waiter_id = models.AutoField(primary_key=True)
    waiter_name = models.CharField(max_length=100)
    waiter_email = models.EmailField()
    waiter_password = models.CharField(max_length=100, default='waiter123')
    waiter_phone = models.CharField(max_length=15)
    waiter_shift = models.CharField(
        max_length=50,
        choices=[
            ('morning', 'Morning'),
            ('afternoon', 'Afternoon'),
            ('evening', 'Evening'),
            ('night', 'Night'),
        ]
        )
    
    def __str__(self):
        return self.waiter_name
# --- waiter registration end ---

# --- Reservation ModelForm(reserve page model) Start ---
class Reservation(models.Model):
    res_id = models.AutoField(primary_key=True)
    cus_name = models.CharField(max_length=100)
    cus_email = models.EmailField()
    res_date = models.DateField()
    res_time = models.TimeField()
    num_people = models.PositiveIntegerField()
    
    def __str__(self):
        return self.cus_name

# --- Reservation ModelForm(reserve page model) End ---

# --- Custom User Model Start ---
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('waiter', 'Waiter'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
# --- Custom User Model End ---

# --- menu page model start ---
# ---------- MENU ITEMS UPLOAD MODELS ----------
class SubCategory(models.Model):
    name = models.CharField(max_length=120) 
    slug = models.SlugField(unique=True)      
    order = models.IntegerField(default=0)

    def _str_(self):
        return self.name

def upload_to_menu(instance, filename):
    return f"menu_items/{instance.subcategory.slug}/{filename}"

class MenuItem(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to=upload_to_menu, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} ({self.subcategory.slug})"
# --- menu page model end ---
