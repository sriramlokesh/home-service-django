from django.contrib import admin
from .models import Product, Shop, AdminRegistrationRequest, ServiceCatogarys, NewsletterSubscription

# Register your models here.
admin.site.register(Shop)
admin.site.register(ServiceCatogarys)
admin.site.register(NewsletterSubscription)

@admin.register(AdminRegistrationRequest)
class AdminRegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'username', 'email', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    actions = ['approve_requests', 'reject_requests']
    
    def approve_requests(self, request, queryset):
        from django.contrib.auth.models import User
        from django.core.mail import send_mail
        from django.conf import settings
        
        for registration_request in queryset.filter(status='pending'):
            registration_request.status = 'approved'
            registration_request.save()
            
            # Create the admin user
            user = User.objects.create_user(
                username=registration_request.username,
                email=registration_request.email,
                password='temporary_password_123',
                first_name=registration_request.first_name,
                last_name=registration_request.last_name,
                is_staff=True,
                is_superuser=False
            )
            
            # Send approval email
            send_mail(
                'Admin Registration Approved',
                f'Your admin registration has been approved. Username: {registration_request.username}, Temporary Password: temporary_password_123',
                settings.EMAIL_HOST_USER,
                [registration_request.email],
                fail_silently=False,
            )
        
        self.message_user(request, f'{queryset.count()} registration requests have been approved.')
    approve_requests.short_description = "Approve selected registration requests"
    
    def reject_requests(self, request, queryset):
        from django.core.mail import send_mail
        from django.conf import settings
        
        for registration_request in queryset.filter(status='pending'):
            registration_request.status = 'rejected'
            registration_request.save()
            
            # Send rejection email
            send_mail(
                'Admin Registration Request Status',
                'Your admin registration request has not been approved at this time.',
                settings.EMAIL_HOST_USER,
                [registration_request.email],
                fail_silently=False,
            )
        
        self.message_user(request, f'{queryset.count()} registration requests have been rejected.')
    reject_requests.short_description = "Reject selected registration requests"
