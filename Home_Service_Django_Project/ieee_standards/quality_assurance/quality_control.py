"""
IEEE Quality Assurance Implementation
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ServiceQuality(models.Model):
    """
    IEEE Quality Control Implementation
    """
    service_id = models.CharField(max_length=100, unique=True)
    service_type = models.CharField(max_length=100)
    inspection_date = models.DateTimeField(auto_now=True)
    inspector = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    # IEEE Standard Quality Metrics
    safety_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    reliability_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    efficiency_score = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def calculate_overall_score(self):
        """Calculate overall quality score based on IEEE metrics"""
        weights = {
            'safety': 0.4,
            'reliability': 0.3,
            'efficiency': 0.3
        }
        return (
            self.safety_score * weights['safety'] +
            self.reliability_score * weights['reliability'] +
            self.efficiency_score * weights['efficiency']
        )

    def is_compliant(self):
        """Check if service meets IEEE quality standards"""
        return self.calculate_overall_score() >= 75  # IEEE minimum standard

class QualityMetric(models.Model):
    """
    IEEE Quality Metrics Tracking
    """
    metric_name = models.CharField(max_length=100)
    metric_type = models.CharField(
        max_length=20,
        choices=[
            ('SAFETY', 'Safety'),
            ('RELIABILITY', 'Reliability'),
            ('EFFICIENCY', 'Efficiency'),
            ('OTHER', 'Other')
        ]
    )
    value = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['metric_type', 'timestamp'])
        ]

class QualityAudit(models.Model):
    """
    IEEE Quality Audit Implementation
    """
    audit_date = models.DateTimeField(auto_now_add=True)
    auditor = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    audit_type = models.CharField(
        max_length=20,
        choices=[
            ('INTERNAL', 'Internal'),
            ('EXTERNAL', 'External'),
            ('CERTIFICATION', 'Certification')
        ]
    )
    
    # IEEE Standard Audit Checklist
    documentation_check = models.BooleanField(default=False)
    process_check = models.BooleanField(default=False)
    safety_check = models.BooleanField(default=False)
    training_check = models.BooleanField(default=False)
    
    findings = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)
    
    def is_passed(self):
        """Check if audit meets IEEE standards"""
        return all([
            self.documentation_check,
            self.process_check,
            self.safety_check,
            self.training_check
        ])

class ImprovementAction(models.Model):
    """
    IEEE Quality Improvement Implementation
    """
    created_date = models.DateTimeField(auto_now_add=True)
    action_type = models.CharField(
        max_length=20,
        choices=[
            ('CORRECTIVE', 'Corrective'),
            ('PREVENTIVE', 'Preventive'),
            ('IMPROVEMENT', 'Improvement')
        ]
    )
    description = models.TextField()
    priority = models.CharField(
        max_length=20,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High')
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('PLANNED', 'Planned'),
            ('IN_PROGRESS', 'In Progress'),
            ('COMPLETED', 'Completed'),
            ('VERIFIED', 'Verified')
        ]
    )
    completion_date = models.DateTimeField(null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    
    def verify_action(self):
        """Verify improvement action per IEEE standards"""
        from django.utils import timezone
        if self.status == 'COMPLETED':
            self.status = 'VERIFIED'
            self.verification_date = timezone.now()
            self.save() 