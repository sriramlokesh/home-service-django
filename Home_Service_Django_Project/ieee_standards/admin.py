"""
IEEE Standards Admin Configuration
"""
from django.contrib import admin
from .safety.electrical_safety import GroundingSystem, SafetyInspection, SafetyAlert
from .monitoring.smart_monitoring import SmartMeter, IoTDevice, DeviceData, MonitoringAlert
from .quality_assurance.quality_control import (
    ServiceQuality, QualityMetric, QualityAudit, ImprovementAction
)

@admin.register(GroundingSystem)
class GroundingSystemAdmin(admin.ModelAdmin):
    """Admin interface for GroundingSystem"""
    list_display = ('location', 'resistance_value', 'status', 'last_test_date', 'next_test_date')
    list_filter = ('status', 'last_test_date')
    search_fields = ('location',)

@admin.register(SafetyInspection)
class SafetyInspectionAdmin(admin.ModelAdmin):
    """Admin interface for SafetyInspection"""
    list_display = ('location', 'inspector', 'inspection_date', 'is_compliant')
    list_filter = ('inspection_date', 'inspector')
    search_fields = ('location', 'inspector__username')

@admin.register(SafetyAlert)
class SafetyAlertAdmin(admin.ModelAdmin):
    """Admin interface for SafetyAlert"""
    list_display = ('location', 'alert_type', 'severity', 'timestamp', 'resolved')
    list_filter = ('alert_type', 'severity', 'resolved')
    search_fields = ('location', 'description')

@admin.register(SmartMeter)
class SmartMeterAdmin(admin.ModelAdmin):
    """Admin interface for SmartMeter"""
    list_display = ('device_id', 'location', 'status', 'power_consumption', 'last_reading_date')
    list_filter = ('status', 'installation_date')
    search_fields = ('device_id', 'location')

@admin.register(IoTDevice)
class IoTDeviceAdmin(admin.ModelAdmin):
    """Admin interface for IoTDevice"""
    list_display = ('device_id', 'device_type', 'location', 'last_seen', 'encryption_enabled')
    list_filter = ('device_type', 'encryption_enabled', 'authentication_method')
    search_fields = ('device_id', 'location')

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    """Admin interface for DeviceData"""
    list_display = ('device', 'data_type', 'timestamp')
    list_filter = ('data_type', 'timestamp')
    search_fields = ('device__device_id',)

@admin.register(MonitoringAlert)
class MonitoringAlertAdmin(admin.ModelAdmin):
    """Admin interface for MonitoringAlert"""
    list_display = ('device', 'alert_type', 'timestamp', 'resolved')
    list_filter = ('alert_type', 'resolved')
    search_fields = ('device__device_id', 'description')

@admin.register(ServiceQuality)
class ServiceQualityAdmin(admin.ModelAdmin):
    """Admin interface for ServiceQuality"""
    list_display = ('service_id', 'service_type', 'calculate_overall_score', 'is_compliant')
    list_filter = ('service_type', 'inspection_date')
    search_fields = ('service_id',)

@admin.register(QualityMetric)
class QualityMetricAdmin(admin.ModelAdmin):
    """Admin interface for QualityMetric"""
    list_display = ('metric_name', 'metric_type', 'value', 'timestamp')
    list_filter = ('metric_type', 'timestamp')
    search_fields = ('metric_name',)

@admin.register(QualityAudit)
class QualityAuditAdmin(admin.ModelAdmin):
    """Admin interface for QualityAudit"""
    list_display = ('auditor', 'audit_type', 'audit_date', 'is_passed')
    list_filter = ('audit_type', 'audit_date')
    search_fields = ('auditor__username',)

@admin.register(ImprovementAction)
class ImprovementActionAdmin(admin.ModelAdmin):
    """Admin interface for ImprovementAction"""
    list_display = ('action_type', 'priority', 'status', 'created_date')
    list_filter = ('action_type', 'priority', 'status')
    search_fields = ('description',) 