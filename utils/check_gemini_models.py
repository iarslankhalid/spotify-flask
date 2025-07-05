#!/usr/bin/env python3
"""
Check available Gemini models
"""

import google.generativeai as genai
import os

def check_gemini_models():
    print("🔍 Checking Available Gemini Models")
    print("=" * 40)
    
    try:
        # Configure with the API key from environment
        gemini_key = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key_here')
        if gemini_key == 'your_gemini_api_key_here':
            print("❌ GEMINI_API_KEY not set properly")
            return
        
        genai.configure(api_key=gemini_key)
        
        print("📋 Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"✅ {model.name}")
                print(f"   Display Name: {model.display_name}")
                print(f"   Description: {model.description}")
                print()
        
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_gemini_models()
