from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Safety Models
class GroundingSystem(models.Model):
    system_id = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=200)
    installation_date = models.DateField()
    last_inspection_date = models.DateField()
    resistance_value = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Grounding resistance in ohms"
    )
    is_compliant = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Grounding System {self.system_id} at {self.location}"

    class Meta:
        verbose_name = "Grounding System"
        verbose_name_plural = "Grounding Systems"

class SafetyInspection(models.Model):
    INSPECTION_TYPES = [
        ('ROUTINE', 'Routine Inspection'),
        ('INCIDENT', 'Incident Investigation'),
        ('COMPLIANCE', 'Compliance Check'),
    ]

    inspection_id = models.CharField(max_length=50, unique=True)
    inspection_type = models.CharField(max_length=20, choices=INSPECTION_TYPES)
    inspector = models.ForeignKey(User, on_delete=models.PROTECT)
    inspection_date = models.DateTimeField()
    findings = models.TextField()
    recommendations = models.TextField()
    is_passed = models.BooleanField(default=False)
    next_inspection_date = models.DateField()

    def __str__(self):
        return f"{self.inspection_type} - {self.inspection_date.date()}"

class SafetyAlert(models.Model):
    ALERT_TYPES = [
        ('CRITICAL', 'Critical'),
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]

    alert_id = models.CharField(max_length=50, unique=True)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    resolved_date = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )

    def __str__(self):
        return f"{self.alert_type} Alert - {self.alert_id}"

# Monitoring Models
class SmartMeter(models.Model):
    METER_TYPES = [
        ('POWER', 'Power Meter'),
        ('WATER', 'Water Meter'),
        ('GAS', 'Gas Meter'),
    ]

    device_id = models.CharField(max_length=50, unique=True)
    meter_type = models.CharField(max_length=20, choices=METER_TYPES)
    location = models.CharField(max_length=200)
    installation_date = models.DateField()
    last_calibration_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.meter_type} Meter - {self.device_id}"

class IoTDevice(models.Model):
    DEVICE_TYPES = [
        ('SENSOR', 'Sensor'),
        ('ACTUATOR', 'Actuator'),
        ('CONTROLLER', 'Controller'),
    ]

    device_id = models.CharField(max_length=50, unique=True)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    location = models.CharField(max_length=200)
    installation_date = models.DateField()
    firmware_version = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    last_maintenance_date = models.DateField()

    def __str__(self):
        return f"{self.device_type} - {self.device_id}"

class DeviceData(models.Model):
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    data_value = models.FloatField()
    data_unit = models.CharField(max_length=20)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f"Data from {self.device.device_id} at {self.timestamp}"

class MonitoringAlert(models.Model):
    ALERT_TYPES = [
        ('CRITICAL', 'Critical'),
        ('WARNING', 'Warning'),
        ('INFO', 'Information'),
    ]

    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    resolved_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.alert_type} Alert for {self.device.device_id}"

# Quality Assurance Models
class ServiceQuality(models.Model):
    SERVICE_TYPES = [
        ('ELECTRICAL', 'Electrical'),
        ('PLUMBING', 'Plumbing'),
        ('HVAC', 'HVAC'),
        ('SECURITY', 'Security'),
    ]

    service_id = models.CharField(max_length=50, unique=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    provider = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.service_type} Service - {self.service_id}"

    class Meta:
        verbose_name = "Service Quality"
        verbose_name_plural = "Service Qualities"

class QualityMetric(models.Model):
    METRIC_TYPES = [
        ('RELIABILITY', 'Reliability'),
        ('RESPONSE_TIME', 'Response Time'),
        ('CUSTOMER_SAT', 'Customer Satisfaction'),
        ('COMPLIANCE', 'Compliance'),
    ]

    service = models.ForeignKey(ServiceQuality, on_delete=models.CASCADE)
    metric_type = models.CharField(max_length=20, choices=METRIC_TYPES)
    value = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)]
    )
    measurement_date = models.DateField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.metric_type} for {self.service.service_id}"

class QualityAudit(models.Model):
    AUDIT_TYPES = [
        ('INTERNAL', 'Internal Audit'),
        ('EXTERNAL', 'External Audit'),
        ('CERTIFICATION', 'Certification Audit'),
    ]

    audit_id = models.CharField(max_length=50, unique=True)
    audit_type = models.CharField(max_length=20, choices=AUDIT_TYPES)
    auditor = models.ForeignKey(User, on_delete=models.PROTECT)
    audit_date = models.DateField()
    findings = models.TextField()
    recommendations = models.TextField()
    is_passed = models.BooleanField(default=False)
    next_audit_date = models.DateField()

    def __str__(self):
        return f"{self.audit_type} - {self.audit_date}"

class ImprovementAction(models.Model):
    PRIORITY_LEVELS = [
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('PLANNED', 'Planned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    action_id = models.CharField(max_length=50, unique=True)
    related_audit = models.ForeignKey(QualityAudit, on_delete=models.CASCADE)
    action_type = models.CharField(max_length=100)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT)
    created_date = models.DateField(auto_now_add=True)
    target_completion_date = models.DateField()
    actual_completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.action_type} - {self.status}" 