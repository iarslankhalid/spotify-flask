#!/usr/bin/env python3
"""
Simple Gemini API test
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

def test_gemini_simple():
    print("🤖 Testing Gemini API")
    print("=" * 30)
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"API Key: {'✅ Found' if api_key and api_key != 'your_gemini_api_key_here' else '❌ Not found'}")
    
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ Please set a valid GEMINI_API_KEY in .env")
        return False
    
    try:
        # Configure Gemini
        genai.configure(api_key=api_key)
        print("✅ Gemini configured")
        
        # List available models
        print("\n📋 Available models:")
        models = list(genai.list_models())
        for model in models[:3]:  # Show first 3
            if 'generateContent' in model.supported_generation_methods:
                print(f"   ✅ {model.name}")
        
        # Test with a simple prompt
        print("\n🧪 Testing with simple prompt...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        response = model.generate_content("Analyze this music: 'Chill ambient track for relaxation'. What mood does it suggest? Respond in one sentence.")
        
        print(f"✅ Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_simple()
