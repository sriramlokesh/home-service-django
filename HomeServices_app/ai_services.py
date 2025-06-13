from django.conf import settings
import google.generativeai as genai
import requests
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIServices:
    """Class to handle AI-related services for the home service application using Gemini"""
    
    # Define available services
    AVAILABLE_SERVICES = """
    Our available services include:
    1. Plumbing Services
       - Pipe repairs and maintenance
       - Drain cleaning and unclogging
       - Fixture installation and repair
       - Water heater services
       - Emergency plumbing
    
    2. Electrical Services
       - Wiring installation and repair
       - Lighting installation
       - Electrical repairs and maintenance
       - Circuit breaker services
       - Emergency electrical work
    
    3. Cleaning Services
       - Regular house cleaning
       - Deep cleaning
       - Move-in/out cleaning
       - Window cleaning
       - Carpet cleaning
    
    4. Landscaping Services
       - Lawn maintenance
       - Tree trimming and removal
       - Garden design and maintenance
       - Irrigation system services
       - Seasonal cleanup
    
    5. Pest Control Services
       - Pest inspection
       - Treatment and extermination
       - Prevention and maintenance
       - Termite control
       - Emergency pest control
    """
    
    def __init__(self):
        try:
            # Try to get the API key from settings first, then environment
            self.gemini_key = getattr(settings, 'GEMINI_API_KEY', None)
            if not self.gemini_key:
                self.gemini_key = os.getenv('GEMINI_API_KEY')
                
            if not self.gemini_key:
                logger.error("Gemini API key not found in settings or environment")
                return
                
            # Log the first few characters of the API key for verification
            logger.info("Found API key starting with: %s", self.gemini_key[:10])
            
            # Configure the Gemini client
            genai.configure(api_key=self.gemini_key)
            
            # Test the configuration with a simple prompt
            logger.info("Testing Gemini API configuration...")
            model = genai.GenerativeModel('gemini-1.5-flash')  # Using flash model for better rate limits
            response = model.generate_content("Test connection")
            
            if not response:
                logger.error("Received empty response from Gemini API")
                self.gemini_key = None
                return
                
            if not hasattr(response, 'text'):
                logger.error("Response missing text attribute")
                self.gemini_key = None
                return
                
            if not response.text:
                logger.error("Response text is empty")
                self.gemini_key = None
                return
                
            logger.info("Gemini API configured successfully")
            
        except Exception as e:
            logger.error(f"Error during Gemini API configuration: {str(e)}")
            self.gemini_key = None

    def get_service_recommendation(self, user_description, use_direct_api=False):
        """Get AI-powered service recommendations based on user description"""
        if not self.gemini_key:
            logger.error("Gemini API key not available or invalid")
            return {
                "error": True,
                "message": "Gemini AI service is currently unavailable. Please check your API key configuration."
            }
            
        if not user_description or not user_description.strip():
            logger.warning("Empty or invalid user description received")
            return {
                "error": True,
                "message": "Please provide a valid service description."
            }
            
        try:
            logger.info(f"Processing recommendation request using {'direct API' if use_direct_api else 'Python client'}")
            if use_direct_api:
                return self._get_gemini_direct_api(
                    f"You are a home service expert. Provide a detailed recommendation for this request: {user_description}"
                )
            else:
                return self._get_gemini_recommendation(user_description)
        except Exception as e:
            logger.error(f"Error in get_service_recommendation: {str(e)}")
            return {
                "error": True,
                "message": f"Error processing request: {str(e)}"
            }

    def _get_gemini_direct_api(self, prompt_text):
        """Get response using direct Gemini API call"""
        try:
            logger.info("Making direct API call to Gemini")
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
            
            # Enhanced context with user/worker specific guidance
            context = f"""You are HomeHelper, an AI assistant for a home services platform that serves both service users and service providers.
            First, identify if the user is a service user or a service provider (worker) based on their query or context.
            
            For Service Users:
            1. Service Selection & Booking
               - Help choose the right service
               - Explain booking process
               - Provide cost estimates
               - Share preparation tips
            
            2. Emergency Assistance
               - Identify emergency situations
               - Guide to immediate help
               - Provide safety instructions
            
            3. Service Tracking
               - Explain tracking process
               - Help with status checks
               - Guide through feedback
            
            4. Maintenance Tips
               - Share preventive advice
               - Recommend service schedules
               - Provide DIY safety tips
            
            For Service Providers (Workers):
            1. Job Management
               - Explain assignment process
               - Share best practices
               - Guide through status updates
               - Help with scheduling
            
            2. Service Guidelines
               - Share service standards
               - Explain quality requirements
               - Provide safety protocols
               - Detail reporting procedures
            
            3. Emergency Protocols
               - Guide through emergencies
               - Share safety procedures
               - Explain urgent reporting
            
            4. Customer Service Tips
               - Communication best practices
               - Service quality guidelines
               - Customer satisfaction tips
            
            Available Services:
            {self.AVAILABLE_SERVICES}
            
            Interaction Guidelines:
            1. First identify if speaking to a user or worker
            2. Use appropriate terminology for each group
            3. For users: Focus on service selection and preparation
            4. For workers: Focus on service delivery and quality
            5. Always maintain professionalism
            6. Include safety warnings when relevant
            7. Recommend best practices
            8. Share relevant tips based on role
            
            Emergency Situations:
            - Always prioritize safety
            - Provide immediate action steps
            - Guide to emergency contacts
            - Share safety precautions
            
            Quality Standards:
            - Explain service standards
            - Share best practices
            - Guide through procedures
            - Focus on customer satisfaction
            
            Remember to:
            1. Be professional and courteous
            2. Provide role-specific guidance
            3. Include safety information
            4. Share relevant tips and best practices
            5. Guide through processes step by step
            6. Maintain focus on quality service
            """
            
            full_prompt = f"{context}\n\nUser request: {prompt_text}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "safetySettings": [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024
                }
            }
            
            headers = {
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, headers=headers, json=payload)
            logger.info(f"API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                response_data = response.json()
                logger.debug(f"API Response: {response_data}")
                
                if 'candidates' in response_data:
                    return {
                        "error": False,
                        "message": response_data['candidates'][0]['content']['parts'][0]['text']
                    }
                logger.error("No candidates in response")
                return {
                    "error": True,
                    "message": "No response generated. Please try again."
                }
            else:
                logger.error(f"API Error: {response.status_code} - {response.text}")
                return {
                    "error": True,
                    "message": f"API Error: {response.status_code} - Please try again."
                }
                
        except Exception as e:
            logger.error(f"Error in direct API call: {str(e)}")
            return {
                "error": True,
                "message": f"Error with Gemini API call: {str(e)}"
            }
            
    def _get_gemini_recommendation(self, user_description):
        """Get recommendation using Gemini Python client"""
        try:
            logger.info("Getting recommendation using Python client")
            model = genai.GenerativeModel('gemini-1.5-flash')  # Using flash model for better rate limits
            
            # Add context about available services
            context = f"""You are an AI assistant for a home services website. 
            When someone asks about booking a service, first check if they've specified which service they want.
            If they haven't specified a service, ask them to choose from our available services:
            {self.AVAILABLE_SERVICES}
            
            Once they specify a service, guide them through the booking process by:
            1. Explaining what information they'll need to provide
            2. Estimated timeframes for the service
            3. What to expect during the service
            4. Payment options and pricing information
            
            Always be helpful, professional, and thorough in your responses.
            """
            
            response = model.generate_content([
                context,
                f"User request: {user_description}"
            ])
            
            logger.info("Successfully generated recommendation")
            return {
                "error": False,
                "message": response.text
            }
        except Exception as e:
            logger.error(f"Error in Python client: {str(e)}")
            return {
                "error": True,
                "message": f"Error getting recommendation: {str(e)}"
            }
            
    def analyze_service_request(self, request_details, use_direct_api=False):
        """Analyze service request and provide insights"""
        if not self.gemini_key:
            return {
                "error": True,
                "message": "Gemini AI service is currently unavailable. Please check your API key configuration."
            }
            
        try:
            if use_direct_api:
                return self._get_gemini_direct_api(
                    f"As a service request analyzer, please analyze this request: {request_details}"
                )
            else:
                return self._analyze_with_gemini(request_details)
        except Exception as e:
            return {
                "error": True,
                "message": f"Error: {str(e)}"
            }
            
    def _analyze_with_gemini(self, request_details):
        """Analyze request using Gemini"""
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')  # Using flash model for better rate limits
            
            # Add context about available services
            context = f"""You are an AI assistant for a home services website. 
            When analyzing service requests, consider our available services:
            {self.AVAILABLE_SERVICES}
            
            Provide detailed analysis including:
            1. Which service category the request falls under
            2. Estimated scope of work
            3. Potential complications or considerations
            4. Recommended next steps
            
            Be thorough and professional in your analysis.
            """
            
            response = model.generate_content([
                context,
                f"Please analyze this service request: {request_details}"
            ])
            
            return {
                "error": False,
                "message": response.text
            }
        except Exception as e:
            return {
                "error": True,
                "message": f"Error analyzing with Gemini: {str(e)}"
            } 