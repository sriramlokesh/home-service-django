from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

# Create your models here.

# Indian phone number validator
indian_phone_regex = RegexValidator(
    regex=r'^[6-9]\d{9}$',
    message="Phone number must be a valid Indian mobile number (10 digits starting with 6, 7, 8, or 9)."
)

# Legacy phone regex for backward compatibility
phone_regex = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

class users(models.Model):
    admin = models.ForeignKey(User, on_delete = models.CASCADE)
    contact_number = models.CharField(validators=[phone_regex], max_length=17)
    Address=models.TextField()
    gender = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_pic=models.FileField(upload_to='workers_pic/')

class workers(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(validators=[phone_regex], max_length=17)
    dob = models.DateField(null=True, blank=True)
    Address = models.TextField()
    city=models.CharField(max_length=255)
    gender = models.CharField(max_length=250)
    designation=models.CharField(max_length=255)
    profile_pic=models.FileField(upload_to='workers_pic/')
    acc_activation=models.BooleanField(default=False)
    avalability_status=models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Country(models.Model):
    name = models.CharField(max_length=150)


class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)


class City(models.Model):
    state = models.CharField(max_length=150)
    name = models.CharField(max_length=150)

class ServiceCatogarys(models.Model):
    img=models.ImageField(upload_to='catogry_imgs')
    Name=models.CharField(max_length=255)
    Description=models.TextField()
    
class ServiceRequests(models.Model):
    user=models.ForeignKey(users,on_delete=models.CASCADE)
    Problem_Description=models.TextField()
    service = models.ForeignKey(ServiceCatogarys, on_delete=models.CASCADE)
    Address = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    pin = models.CharField(max_length=10)
    House_No = models.CharField(max_length=20)
    landmark = models.TextField(null=True)
    contact=models.CharField(max_length=200)
    status=models.BooleanField(default=False)
    dateofrequest=models.DateTimeField(auto_now_add=True)

class Response(models.Model):
    requests=models.ForeignKey(ServiceRequests,on_delete=models.CASCADE)
    assigned_worker=models.ForeignKey(workers,on_delete=models.CASCADE)
    Date=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)


class Feedback(models.Model):
    Rating=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    Description=models.TextField()
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    # User=models.ForeignKey(users,on_delete=models.CASCADE)
    Employ=models.ForeignKey(workers,on_delete=models.CASCADE)
    Date=models.DateField()


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    forget_token = models.CharField(max_length=1000)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class ServiceTracking(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    status_update = models.CharField(max_length=255)
    battery_level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estimated_arrival_time = models.DateTimeField(null=True, blank=True)
    signal_strength = models.IntegerField(null=True, blank=True)  # RSSI value in dBm

    def update_signal_strength(self, rssi):
        """Update IEEE 802.11 signal strength"""
        self.signal_strength = rssi
        self.save()

    def calculate_eta(self):
        """Calculate estimated time of arrival"""
        # Implementation for ETA calculation based on location and traffic data
        # This is a placeholder - actual implementation would use Maps API
        from datetime import datetime, timedelta
        self.estimated_arrival_time = datetime.now() + timedelta(minutes=30)
        self.save()

    def __str__(self):
        return f"Tracking for Response #{self.response.id} - {self.status_update}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service Tracking'
        verbose_name_plural = 'Service Trackings'

class Shop(models.Model):
    CATEGORY_CHOICES = [
        ('grocery', 'Grocery'),
        ('electricals', 'Electricals'),
        ('plumbing', 'Plumbing'),
    ]
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='shop_images/', blank=True, null=True)
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    owner_phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        unique=True,
        blank=True,
        null=True,
        help_text="Enter a unique phone number."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('grocery', 'Grocery'),
        ('electricals', 'Electricals'),
        ('plumbing', 'Plumbing'),
    ]
    
    SUBCATEGORY_CHOICES = [
        # Grocery subcategories
        ('fruits_vegetables', 'Fruits & Vegetables'),
        ('dairy_bakery', 'Dairy & Bakery'),
        ('beverages', 'Beverages'),
        ('snacks', 'Snacks'),
        ('household', 'Household'),
        ('personal_care', 'Personal Care'),
        
        # Electricals subcategories
        ('lighting', 'Lighting'),
        ('kitchen_appliances', 'Kitchen Appliances'),
        ('electronics', 'Electronics'),
        ('tools', 'Tools'),
        
        # Plumbing subcategories
        ('pipes_fittings', 'Pipes & Fittings'),
        ('faucets', 'Faucets'),
        ('bathroom', 'Bathroom'),
        ('kitchen_plumbing', 'Kitchen Plumbing'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=30, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    shop = models.ForeignKey('Shop', null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_category_display()}"
    
    class Meta:
        ordering = ['-created_at']

class AdminRegistrationRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(validators=[indian_phone_regex], max_length=10)
    address = models.TextField()
    password = models.CharField(max_length=128, null=True, blank=True)  # Store hashed password
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admin Registration Request'
        verbose_name_plural = 'Admin Registration Requests'



