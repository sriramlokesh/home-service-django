from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models

# Create your models here.

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



