import os
from dotenv import load_dotenv
import google.generativeai as genai

def test_api():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables")
        return False
        
    try:
        # Configure the API
        genai.configure(api_key=api_key)
        
        # Create a model instance
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Test with a simple prompt
        response = model.generate_content("Hello, this is a test message.")
        
        if response and response.text:
            print("Success! API is working correctly.")
            print("Response:", response.text)
            return True
        else:
            print("Error: Received empty response")
            return False
            
    except Exception as e:
        print(f"Error testing API: {str(e)}")
        return False

if __name__ == "__main__":
    test_api() 