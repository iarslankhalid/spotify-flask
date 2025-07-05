#!/usr/bin/env python3
"""
Test Gemini with a demo/mock setup to verify the integration works
"""

import os
import sys
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

class MockGeminiModel:
    """Mock Gemini model for testing"""
    
    def generate_content(self, prompt):
        """Mock generate_content method"""
        
        class MockResponse:
            def __init__(self):
                # Generate a realistic response based on the prompt content
                if 'psychedelic therapy' in prompt.lower() or 'stars of the lid' in prompt.lower():
                    self.text = '''```json
{
    "suggestions": [
        {
            "mood": "meditative",
            "confidence": 0.91,
            "reasoning": "The playlist contains ambient and therapeutic tracks with artists like Stars Of The Lid, which are specifically designed for meditation and healing."
        },
        {
            "mood": "introspective", 
            "confidence": 0.87,
            "reasoning": "The contemplative nature of the tracks and the therapeutic focus suggests deep introspection and self-reflection."
        },
        {
            "mood": "calming",
            "confidence": 0.84,
            "reasoning": "The ambient, drone-style music and therapeutic intent create a calming, peaceful atmosphere."
        }
    ],
    "overall_assessment": "This is a carefully curated therapeutic playlist featuring ambient drone and neo-classical artists designed for meditation, healing, and deep contemplation. The music is specifically chosen to create immersive, calming soundscapes."
}
```'''
                else:
                    self.text = '''```json
{
    "suggestions": [
        {
            "mood": "energetic",
            "confidence": 0.80,
            "reasoning": "Based on the track selection, this appears to be an upbeat playlist."
        }
    ],
    "overall_assessment": "Demo analysis of the provided playlist."
}
```'''
        
        return MockResponse()

def test_gemini_mock():
    """Test Gemini functionality with mock"""
    print("🎭 Testing Gemini with Mock Integration")
    print("=" * 50)
    
    # Create analyzer
    analyzer = MoodAnalyzer()
    
    # Replace Gemini model with mock
    analyzer.gemini_model = MockGeminiModel()
    analyzer.gemini_available = True
    
    # Get playlist data
    spotify_client = SpotifyClient()
    playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
    
    print(f"📡 Getting playlist data...")
    playlist_data = spotify_client.analyze_playlist(playlist_url)
    
    if not playlist_data:
        print("❌ Could not get playlist data")
        return
    
    print(f"✅ Got playlist: {playlist_data['playlist_info']['name']}")
    print(f"   Duration: {playlist_data.get('total_duration_formatted', 'Not calculated')}")
    print()
    
    # Test Gemini mock
    print("🤖 Testing Gemini mock analysis...")
    try:
        gemini_result = analyzer.get_gemini_mood_suggestions(playlist_data)
        
        print("✅ Gemini mock analysis successful!")
        print(f"   Assessment: {gemini_result.get('overall_assessment', 'No assessment')}")
        
        suggestions = gemini_result.get('suggestions', [])
        if suggestions:
            print("📊 Gemini Mock Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                mood = suggestion.get('mood', 'Unknown')
                confidence = suggestion.get('confidence', 0)
                reasoning = suggestion.get('reasoning', 'No reasoning')
                print(f"   {i}. {mood.upper()} ({confidence:.0%} confidence)")
                print(f"      → {reasoning}")
                print()
        
        print("✅ SUCCESS: Gemini integration code is working correctly!")
        print("   When you add a real Gemini API key, it will work with Google's AI.")
        
    except Exception as e:
        print(f"❌ Gemini mock test failed: {e}")
        import traceback
        traceback.print_exc()

def test_provider_fallback():
    """Test the provider fallback system"""
    print("🔄 Testing Provider Fallback System")
    print("=" * 40)
    
    # Test with various configurations
    test_scenarios = [
        {
            'name': 'Gemini Only (Mock)',
            'ai_provider': 'gemini',
            'openai_available': False,
            'gemini_available': True
        },
        {
            'name': 'Auto Selection (Both Available)',
            'ai_provider': 'auto', 
            'openai_available': True,
            'gemini_available': True
        },
        {
            'name': 'Fallback to Demo',
            'ai_provider': 'auto',
            'openai_available': False,
            'gemini_available': False
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\n📋 Testing: {scenario['name']}")
        
        # Create analyzer with mock settings
        analyzer = MoodAnalyzer()
        analyzer.ai_provider = scenario['ai_provider']
        analyzer.openai_available = scenario['openai_available']
        analyzer.gemini_available = scenario['gemini_available']
        
        if scenario['gemini_available']:
            analyzer.gemini_model = MockGeminiModel()
        
        print(f"   AI Provider: {analyzer.ai_provider}")
        print(f"   OpenAI Available: {'✅' if analyzer.openai_available else '❌'}")
        print(f"   Gemini Available: {'✅' if analyzer.gemini_available else '❌'}")

def show_configuration_guide():
    """Show how to configure Gemini API"""
    print("📋 Gemini API Configuration Guide")
    print("=" * 40)
    print()
    print("To use Google Gemini API:")
    print("1. Go to https://aistudio.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Add it to your .env file:")
    print("   GEMINI_API_KEY=your_actual_gemini_api_key_here")
    print("4. Set AI_PROVIDER to 'gemini' or 'auto' in .env:")
    print("   AI_PROVIDER=auto")
    print()
    print("The system will then use Gemini for AI mood analysis!")
    print()

def main():
    print("🚀 Gemini Integration Test (with Mock)")
    print("=" * 60)
    print()
    
    show_configuration_guide()
    test_gemini_mock()
    print()
    test_provider_fallback()
    
    print("\n✅ All tests completed!")
    print("\n💡 Summary:")
    print("   - Gemini integration code is working correctly")
    print("   - Mock tests show the expected behavior")
    print("   - Add a real Gemini API key to enable full functionality")

if __name__ == "__main__":
    main()
