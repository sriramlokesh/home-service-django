"""
IEEE Standards Views
"""
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .safety.electrical_safety import GroundingSystem, SafetyInspection, SafetyAlert
from .monitoring.smart_monitoring import SmartMeter, IoTDevice, DeviceData, MonitoringAlert
from .quality_assurance.quality_control import (
    ServiceQuality, QualityMetric, QualityAudit, ImprovementAction
)

# Safety Views
class SafetyDashboardView(LoginRequiredMixin, ListView):
    """Safety Dashboard View"""
    template_name = 'ieee_standards/safety/dashboard.html'
    context_object_name = 'safety_items'

    def get_queryset(self):
        """Get safety related data"""
        return {
            'grounding_systems': GroundingSystem.objects.all()[:5],
            'recent_inspections': SafetyInspection.objects.all()[:5],
            'active_alerts': SafetyAlert.objects.filter(resolved=False)
        }

class GroundingSystemListView(LoginRequiredMixin, ListView):
    """List all grounding systems"""
    model = GroundingSystem
    template_name = 'ieee_standards/safety/grounding_list.html'
    context_object_name = 'systems'

class SafetyInspectionCreateView(LoginRequiredMixin, CreateView):
    """Create new safety inspection"""
    model = SafetyInspection
    template_name = 'ieee_standards/safety/inspection_form.html'
    fields = ['location', 'grounding_check', 'bonding_check', 
              'equipment_check', 'warning_signs_check', 'notes']
    success_url = reverse_lazy('safety-dashboard')

    def form_valid(self, form):
        """Set the inspector to current user"""
        form.instance.inspector = self.request.user
        return super().form_valid(form)

# Monitoring Views
class MonitoringDashboardView(LoginRequiredMixin, ListView):
    """Monitoring Dashboard View"""
    template_name = 'ieee_standards/monitoring/dashboard.html'
    context_object_name = 'monitoring_items'

    def get_queryset(self):
        """Get monitoring related data"""
        return {
            'smart_meters': SmartMeter.objects.all()[:5],
            'iot_devices': IoTDevice.objects.all()[:5],
            'recent_alerts': MonitoringAlert.objects.filter(resolved=False)
        }

class IoTDeviceListView(LoginRequiredMixin, ListView):
    """List all IoT devices"""
    model = IoTDevice
    template_name = 'ieee_standards/monitoring/device_list.html'
    context_object_name = 'devices'

class DeviceDataDetailView(LoginRequiredMixin, DetailView):
    """View device data details"""
    model = DeviceData
    template_name = 'ieee_standards/monitoring/data_detail.html'
    context_object_name = 'data'

# Quality Assurance Views
class QualityDashboardView(LoginRequiredMixin, ListView):
    """Quality Assurance Dashboard View"""
    template_name = 'ieee_standards/quality/dashboard.html'
    context_object_name = 'quality_items'

    def get_queryset(self):
        """Get quality related data"""
        return {
            'service_quality': ServiceQuality.objects.all()[:5],
            'recent_audits': QualityAudit.objects.all()[:5],
            'improvement_actions': ImprovementAction.objects.filter(
                status__in=['PLANNED', 'IN_PROGRESS']
            )
        }

class QualityAuditCreateView(LoginRequiredMixin, CreateView):
    """Create new quality audit"""
    model = QualityAudit
    template_name = 'ieee_standards/quality/audit_form.html'
    fields = ['audit_type', 'documentation_check', 'process_check',
              'safety_check', 'training_check', 'findings', 'recommendations']
    success_url = reverse_lazy('quality-dashboard')

    def form_valid(self, form):
        """Set the auditor to current user"""
        form.instance.auditor = self.request.user
        return super().form_valid(form)

class ImprovementActionUpdateView(LoginRequiredMixin, UpdateView):
    """Update improvement action"""
    model = ImprovementAction
    template_name = 'ieee_standards/quality/improvement_form.html'
    fields = ['status', 'description']
    success_url = reverse_lazy('quality-dashboard') 