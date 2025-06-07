from django.core.mail import send_mail
from django.http import JsonResponse
from django.views import View
from .ai_services import AIServices

class TestServicesView(View):
    def get(self, request):
        results = {
            'email': False,
            'ai': False,
            'errors': []
        }
        
        # Test Email
        try:
            send_mail(
                'Test Email from Home Services',
                'This is a test email to verify the email service is working.',
                'home30801@gmail.com',
                ['home30801@gmail.com'],
                fail_silently=False,
            )
            results['email'] = True
        except Exception as e:
            results['errors'].append(f'Email error: {str(e)}')
        
        # Test AI
        try:
            ai_service = AIServices()
            response = ai_service.get_chatbot_response("Hello, is the AI service working?")
            if response:
                results['ai'] = True
        except Exception as e:
            results['errors'].append(f'AI error: {str(e)}')
        
        return JsonResponse(results) 