"""
IEEE 142 Implementation - Electrical Safety Standards
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class GroundingSystem(models.Model):
    """
    IEEE 142 - Grounding System Implementation
    """
    location = models.CharField(max_length=255)
    resistance_value = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(25.0)]
    )
    last_test_date = models.DateTimeField(auto_now=True)
    next_test_date = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('PASS', 'Passed'),
            ('FAIL', 'Failed'),
            ('PENDING', 'Pending Test')
        ]
    )

    def check_resistance(self):
        """IEEE 142 standard resistance check"""
        return self.resistance_value <= 5.0  # IEEE recommended threshold

    def needs_testing(self):
        """Check if system needs testing based on IEEE schedule"""
        from django.utils import timezone
        return self.next_test_date <= timezone.now()

class SafetyInspection(models.Model):
    """
    IEEE 142 - Safety Inspection Implementation
    """
    inspection_date = models.DateTimeField(auto_now_add=True)
    inspector = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    
    # IEEE 142 Standard Checklist
    grounding_check = models.BooleanField(default=False)
    bonding_check = models.BooleanField(default=False)
    equipment_check = models.BooleanField(default=False)
    warning_signs_check = models.BooleanField(default=False)
    
    notes = models.TextField(blank=True)
    
    def is_compliant(self):
        """Check if all IEEE requirements are met"""
        return all([
            self.grounding_check,
            self.bonding_check,
            self.equipment_check,
            self.warning_signs_check
        ])

class SafetyAlert(models.Model):
    """
    IEEE 142 - Safety Alert System
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=255)
    alert_type = models.CharField(
        max_length=20,
        choices=[
            ('GROUND_FAULT', 'Ground Fault'),
            ('BONDING_ISSUE', 'Bonding Issue'),
            ('EQUIPMENT_FAILURE', 'Equipment Failure'),
            ('OTHER', 'Other')
        ]
    )
    severity = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
            ('CRITICAL', 'Critical')
        ]
    )
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    resolution_date = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)

    def escalate_alert(self):
        """Implement IEEE escalation protocols"""
        if self.severity != 'CRITICAL':
            severity_levels = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
            current_index = severity_levels.index(self.severity)
            self.severity = severity_levels[current_index + 1]
            self.save()

    def resolve_alert(self):
        """Mark alert as resolved with current timestamp"""
        from django.utils import timezone
        self.resolved = True
        self.resolution_date = timezone.now()
        self.save() 