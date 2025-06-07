import google.generativeai as genai
import sys

def test_gemini_api():
    try:
        # Configure the API
        api_key = 'AIzaSyDxW_BPq6U2VJbStF7WdFvHnAPwWFmRBqA'
        print(f"Testing with API key: {api_key[:10]}...")
        
        genai.configure(api_key=api_key)
        
        # Create a model instance with the correct model name
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a service booking query
        test_query = "I want to book a service"
        
        print("\nTesting with query:", test_query)
        
        # Define available services
        available_services = """
        Our available services include:
        1. Plumbing Services
           - Pipe repairs
           - Drain cleaning
           - Fixture installation
        2. Electrical Services
           - Wiring
           - Lighting installation
           - Electrical repairs
        3. Cleaning Services
           - House cleaning
           - Deep cleaning
           - Move-in/out cleaning
        4. Landscaping
           - Lawn maintenance
           - Tree trimming
           - Garden design
        5. Pest Control
           - Pest inspection
           - Treatment
           - Prevention
        """
        
        context = f"""
        You are an AI assistant for a home services website. When someone asks about booking a service:
        1. First ask them which specific service they're interested in from our available services:
        {available_services}
        2. Once they specify the service, guide them through the booking process for that specific service
        3. Include information about:
           - What information they'll need to provide
           - Estimated timeframes
           - What to expect during the service
           - Payment options
        4. Always be helpful and professional
        """
        
        response = model.generate_content([context, test_query])
        
        if response and response.text:
            print("\nSuccess! Here's the AI's response:")
            print("-" * 50)
            print(response.text)
            print("-" * 50)
            return True
        else:
            print("Error: Received empty response")
            return False
            
    except Exception as e:
        print(f"Error testing Gemini API: {str(e)}", file=sys.stderr)
        return False

if __name__ == "__main__":
    test_gemini_api() 