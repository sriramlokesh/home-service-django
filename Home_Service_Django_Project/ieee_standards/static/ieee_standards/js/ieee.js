// IEEE Standards JavaScript

// Dashboard Auto-refresh
function setupDashboardRefresh() {
    // Refresh dashboard data every 5 minutes
    const REFRESH_INTERVAL = 300000; // 5 minutes in milliseconds
    setInterval(() => {
        if (document.visibilityState === 'visible') {
            location.reload();
        }
    }, REFRESH_INTERVAL);
}

// Alert Management
function setupAlertSystem() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Add close button to alerts
        const closeBtn = document.createElement('button');
        closeBtn.className = 'alert-close';
        closeBtn.innerHTML = '×';
        closeBtn.onclick = () => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        };
        alert.appendChild(closeBtn);
    });
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('invalid');
            
            // Add error message
            let errorMsg = field.nextElementSibling;
            if (!errorMsg || !errorMsg.classList.contains('error-message')) {
                errorMsg = document.createElement('div');
                errorMsg.className = 'error-message';
                field.parentNode.insertBefore(errorMsg, field.nextSibling);
            }
            errorMsg.textContent = 'This field is required';
        }
    });

    return isValid;
}

// Data Charts
function initializeCharts() {
    const charts = document.querySelectorAll('.ieee-chart');
    charts.forEach(chart => {
        const ctx = chart.getContext('2d');
        const data = JSON.parse(chart.dataset.chartData || '{}');
        
        new Chart(ctx, {
            type: chart.dataset.chartType || 'line',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        });
    });
}

// Real-time Updates
function setupWebSocket() {
    const wsScheme = window.location.protocol === 'https:' ? 'wss' : 'ws';
    const socket = new WebSocket(`${wsScheme}://${window.location.host}/ws/ieee/`);

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        updateDashboard(data);
    };

    socket.onclose = function() {
        console.log('WebSocket closed, attempting to reconnect...');
        setTimeout(setupWebSocket, 5000);
    };
}

function updateDashboard(data) {
    // Update safety metrics
    if (data.safety) {
        updateSafetyMetrics(data.safety);
    }

    // Update monitoring data
    if (data.monitoring) {
        updateMonitoringData(data.monitoring);
    }

    // Update quality metrics
    if (data.quality) {
        updateQualityMetrics(data.quality);
    }
}

// Safety Metrics Update
function updateSafetyMetrics(data) {
    const safetyContainer = document.querySelector('.safety-metrics');
    if (!safetyContainer) return;

    // Update grounding systems
    if (data.groundingSystems) {
        updateGroundingSystems(data.groundingSystems);
    }

    // Update safety alerts
    if (data.alerts) {
        updateSafetyAlerts(data.alerts);
    }
}

// Monitoring Data Update
function updateMonitoringData(data) {
    const monitoringContainer = document.querySelector('.monitoring-data');
    if (!monitoringContainer) return;

    // Update IoT devices
    if (data.devices) {
        updateIoTDevices(data.devices);
    }

    // Update smart meters
    if (data.smartMeters) {
        updateSmartMeters(data.smartMeters);
    }
}

// Quality Metrics Update
function updateQualityMetrics(data) {
    const qualityContainer = document.querySelector('.quality-metrics');
    if (!qualityContainer) return;

    // Update service quality
    if (data.serviceQuality) {
        updateServiceQuality(data.serviceQuality);
    }

    // Update improvement actions
    if (data.improvements) {
        updateImprovementActions(data.improvements);
    }
}

// Initialize all functionality
document.addEventListener('DOMContentLoaded', function() {
    setupDashboardRefresh();
    setupAlertSystem();
    initializeCharts();
    setupWebSocket();

    // Form validation setup
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form.id)) {
                e.preventDefault();
            }
        });
    });
}); 