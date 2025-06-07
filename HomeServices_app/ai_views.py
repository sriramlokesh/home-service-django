from django.http import JsonResponse
from django.views import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .ai_services import AIServices
import logging
import json

logger = logging.getLogger(__name__)

class AITestView(LoginRequiredMixin, View):
    """View to test Gemini API configuration"""
    
    def get(self, request):
        try:
            ai_service = AIServices()
            result = ai_service.get_service_recommendation("Test connection", use_direct_api=False)
            
            if result.get('error', False):
                logger.error(f"API Test Failed: {result['message']}")
                return JsonResponse({
                    'status': 'error',
                    'message': result['message']
                }, status=500)
            
            logger.info("API Test Successful")
            return JsonResponse({
                'status': 'success',
                'message': 'Gemini API is configured and working correctly'
            })
            
        except Exception as e:
            logger.error(f"API Test Error: {str(e)}")
            return JsonResponse({
                'status': 'error',
                'message': f'Error testing API: {str(e)}'
            }, status=500)

class AIRecommendationView(LoginRequiredMixin, View):
    """View to handle AI service recommendations"""
    
    def post(self, request):
        try:
            # Log the user making the request
            logger.info(f"User {request.user.username} requesting recommendation")
            
            description = request.POST.get('description', '').strip()
            use_direct_api = request.POST.get('use_direct_api', 'false').lower() == 'true'
            
            if not description:
                return JsonResponse({
                    'error': True,
                    'message': 'Please provide a service description'
                }, status=400)
                
            logger.info(f"Processing recommendation request for user {request.user.username}: {description[:50]}...")
            ai_service = AIServices()
            
            # Check if AI service is properly initialized
            if not ai_service.gemini_key:
                logger.error("AI service not properly initialized - missing API key")
                return JsonResponse({
                    'error': True,
                    'message': 'AI service is not properly configured. Please check your API key.'
                }, status=503)
            
            # Add user context to the request
            user_context = f"[User: {request.user.username}] {description}"
            result = ai_service.get_service_recommendation(user_context, use_direct_api)
            
            if result.get('error', False):
                logger.error(f"Recommendation Error for user {request.user.username}: {result['message']}")
                return JsonResponse(result, status=500)
                
            logger.info(f"Successfully generated recommendation for user {request.user.username}")
            return JsonResponse({
                'error': False,
                'message': result['message'],
                'api_type': 'direct' if use_direct_api else 'client'
            })
            
        except Exception as e:
            logger.error(f"Recommendation View Error for user {request.user.username}: {str(e)}")
            return JsonResponse({
                'error': True,
                'message': f'An unexpected error occurred: {str(e)}'
            }, status=500)
            
class AIAnalysisView(LoginRequiredMixin, View):
    """View to handle AI analysis of service requests"""
    
    def post(self, request):
        try:
            # Log the user making the request
            logger.info(f"User {request.user.username} requesting analysis")
            
            request_details = request.POST.get('request_details', '')
            use_direct_api = request.POST.get('use_direct_api', 'false').lower() == 'true'
            
            if not request_details:
                return JsonResponse({
                    'error': True,
                    'message': 'Please provide request details'
                }, status=400)
                
            ai_service = AIServices()
            
            # Add user context to the request
            user_context = f"[User: {request.user.username}] {request_details}"
            result = ai_service.analyze_service_request(user_context, use_direct_api)
            
            if result.get('error', False):
                return JsonResponse({
                    'error': True,
                    'message': result['message']
                }, status=500)
                
            return JsonResponse({
                'error': False,
                'message': result['message'],
                'api_type': 'direct' if use_direct_api else 'client'
            })
            
        except Exception as e:
            return JsonResponse({
                'error': True,
                'message': str(e)
            }, status=500)

class AIChatView(LoginRequiredMixin, View):
    """View to handle AI chat interface and messages"""
    
    def get(self, request):
        return render(request, 'ai/chat.html', {
            'title': 'AI Assistant',
            'user': request.user
        })
        
    def post(self, request):
        try:
            # Get the message from either POST data or JSON body
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                message = data.get('message', '').strip()
            else:
                message = request.POST.get('message', '').strip()
            
            if not message:
                return JsonResponse({
                    'error': True,
                    'message': 'Please provide a message'
                }, status=400)
                
            logger.info(f"Processing chat message from user {request.user.username}: {message[:50]}...")
            ai_service = AIServices()
            
            # Check if AI service is properly initialized
            if not ai_service.gemini_key:
                logger.error("AI service not properly initialized - missing API key")
                return JsonResponse({
                    'error': True,
                    'message': 'AI service is not properly configured. Please check your API key.'
                }, status=503)
            
            # Add user context to the message
            user_context = f"[User: {request.user.username}] {message}"
            result = ai_service.get_service_recommendation(user_context)
            
            if result.get('error', False):
                logger.error(f"Chat Error for user {request.user.username}: {result['message']}")
                return JsonResponse(result, status=500)
                
            logger.info(f"Successfully generated chat response for user {request.user.username}")
            return JsonResponse({
                'error': False,
                'response': result['message']
            })
            
        except Exception as e:
            logger.error(f"Chat View Error for user {request.user.username}: {str(e)}")
            return JsonResponse({
                'error': True,
                'message': f'An unexpected error occurred: {str(e)}'
            }, status=500) 