from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

@receiver(user_logged_in)
def send_login_notification(sender, user, request, **kwargs):
    """
    Send an email notification when a user logs in
    """
    subject = 'New Login to Your All-SERVED-S Account'
    current_time = timezone.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_message = render_to_string('email/login_notification.html', {
        'user': user,
        'login_time': current_time,
    })
    plain_message = strip_tags(html_message)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send login notification email: {str(e)}") 