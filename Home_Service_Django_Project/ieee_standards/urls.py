"""
IEEE Standards URLs Configuration
"""
from django.urls import path
from . import views

app_name = 'ieee_standards'

urlpatterns = [
    # Safety URLs
    path('safety/', views.SafetyDashboardView.as_view(), name='safety-dashboard'),
    path('safety/grounding/', views.GroundingSystemListView.as_view(), name='grounding-list'),
    path('safety/inspection/new/', views.SafetyInspectionCreateView.as_view(), name='inspection-create'),

    # Monitoring URLs
    path('monitoring/', views.MonitoringDashboardView.as_view(), name='monitoring-dashboard'),
    path('monitoring/devices/', views.IoTDeviceListView.as_view(), name='device-list'),
    path('monitoring/data/<int:pk>/', views.DeviceDataDetailView.as_view(), name='data-detail'),

    # Quality Assurance URLs
    path('quality/', views.QualityDashboardView.as_view(), name='quality-dashboard'),
    path('quality/audit/new/', views.QualityAuditCreateView.as_view(), name='audit-create'),
    path('quality/improvement/<int:pk>/', views.ImprovementActionUpdateView.as_view(), name='improvement-update'),
] 