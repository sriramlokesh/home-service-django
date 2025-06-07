"""
IEEE 1901 and 2413 Implementation - Smart Monitoring System
"""
from django.db import models
from django.core.validators import MinValueValidator

class SmartMeter(models.Model):
    """
    IEEE 1901 - Smart Meter Implementation
    """
    device_id = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255)
    installation_date = models.DateTimeField(auto_now_add=True)
    last_reading_date = models.DateTimeField(auto_now=True)
    power_consumption = models.FloatField(
        validators=[MinValueValidator(0.0)]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('ACTIVE', 'Active'),
            ('INACTIVE', 'Inactive'),
            ('MAINTENANCE', 'Under Maintenance')
        ]
    )

    def get_consumption_data(self):
        """IEEE 1901 standard power consumption monitoring"""
        return {
            'device_id': self.device_id,
            'consumption': self.power_consumption,
            'timestamp': self.last_reading_date
        }

class IoTDevice(models.Model):
    """
    IEEE 2413 - IoT Device Implementation
    """
    device_id = models.CharField(max_length=100, unique=True)
    device_type = models.CharField(max_length=50)
    location = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    last_seen = models.DateTimeField(auto_now=True)
    firmware_version = models.CharField(max_length=50)
    
    # IEEE 2413 Security Requirements
    encryption_enabled = models.BooleanField(default=True)
    authentication_method = models.CharField(
        max_length=20,
        choices=[
            ('NONE', 'None'),
            ('BASIC', 'Basic'),
            ('TOKEN', 'Token Based'),
            ('CERT', 'Certificate Based')
        ]
    )

    def check_security_compliance(self):
        """Check if device meets IEEE 2413 security standards"""
        return self.encryption_enabled and self.authentication_method != 'NONE'

class DeviceData(models.Model):
    """
    IEEE 2413 - IoT Data Collection
    """
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    data_type = models.CharField(max_length=50)
    value = models.JSONField()
    
    class Meta:
        indexes = [
            models.Index(fields=['device', 'timestamp']),
            models.Index(fields=['data_type'])
        ]

class MonitoringAlert(models.Model):
    """
    IEEE 2413 - Monitoring Alert System
    """
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(
        max_length=20,
        choices=[
            ('OFFLINE', 'Device Offline'),
            ('SECURITY', 'Security Issue'),
            ('PERFORMANCE', 'Performance Issue'),
            ('OTHER', 'Other')
        ]
    )
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    resolution_date = models.DateTimeField(null=True, blank=True)

    def resolve_alert(self):
        """Mark alert as resolved"""
        from django.utils import timezone
        self.resolved = True
        self.resolution_date = timezone.now()
        self.save() 