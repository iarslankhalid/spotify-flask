#!/usr/bin/env python3
"""
Test Google Gemini AI mood analysis functionality
"""

import os
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

def test_gemini_availability():
    """Test if Gemini is properly configured"""
    print("🔍 Testing Gemini Configuration")
    print("=" * 40)
    
    # Check environment variables
    gemini_key = os.getenv('GEMINI_API_KEY')
    ai_provider = os.getenv('AI_PROVIDER', 'auto')
    
    print(f"GEMINI_API_KEY: {'✅ Set' if gemini_key and gemini_key != 'your_gemini_api_key_here' else '❌ Not set or default'}")
    print(f"AI_PROVIDER: {ai_provider}")
    print()
    
    # Test MoodAnalyzer initialization
    try:
        analyzer = MoodAnalyzer()
        print(f"OpenAI Available: {'✅' if analyzer.openai_available else '❌'}")
        print(f"Gemini Available: {'✅' if analyzer.gemini_available else '❌'}")
        print(f"AI Provider Setting: {analyzer.ai_provider}")
        print()
        
        return analyzer
    except Exception as e:
        print(f"❌ MoodAnalyzer initialization failed: {e}")
        return None

def test_gemini_analysis():
    """Test Gemini analysis with a real playlist"""
    print("🎵 Testing Gemini Playlist Analysis")
    print("=" * 50)
    
    analyzer = test_gemini_availability()
    if not analyzer:
        return
    
    if not analyzer.gemini_available:
        print("❌ Gemini not available, cannot test")
        return
    
    # Initialize Spotify client
    spotify_client = SpotifyClient()
    
    try:
        # Test playlist
        playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
        
        print(f"📡 Getting playlist data...")
        playlist_data = spotify_client.analyze_playlist(playlist_url)
        
        if not playlist_data:
            print("❌ Could not get playlist data")
            return
        
        print(f"✅ Got playlist: {playlist_data['playlist_info']['name']}")
        print(f"   Duration: {playlist_data.get('total_duration_formatted', 'Not calculated')}")
        print(f"   Tracks: {playlist_data['total_tracks']}")
        print()
        
        # Test Gemini directly
        print("🤖 Testing Gemini analysis directly...")
        try:
            gemini_result = analyzer.get_gemini_mood_suggestions(playlist_data)
            
            print("✅ Gemini analysis successful!")
            print(f"   Assessment: {gemini_result.get('overall_assessment', 'No assessment')}")
            
            suggestions = gemini_result.get('suggestions', [])
            if suggestions:
                print("📊 Gemini Suggestions:")
                for i, suggestion in enumerate(suggestions, 1):
                    mood = suggestion.get('mood', 'Unknown')
                    confidence = suggestion.get('confidence', 0)
                    reasoning = suggestion.get('reasoning', 'No reasoning')
                    print(f"   {i}. {mood.upper()} ({confidence:.0%} confidence)")
                    print(f"      → {reasoning}")
                    print()
        except Exception as e:
            print(f"❌ Gemini direct test failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test with fallback system
        print("🔄 Testing with fallback system (auto provider selection)...")
        try:
            full_analysis = analyzer.combine_analysis(playlist_data)
            
            print("✅ Full analysis complete!")
            ai_suggestions = full_analysis.get('ai_suggestions', {})
            print(f"   AI Assessment: {ai_suggestions.get('overall_assessment', 'No assessment')}")
            
            if 'error' in ai_suggestions:
                print(f"   Error: {ai_suggestions['error']}")
            
            suggestions = ai_suggestions.get('suggestions', [])
            if suggestions:
                print("📊 Final AI Suggestions:")
                for i, suggestion in enumerate(suggestions, 1):
                    mood = suggestion.get('mood', 'Unknown')
                    confidence = suggestion.get('confidence', 0)
                    print(f"   {i}. {mood.upper()} ({confidence:.0%} confidence)")
            
        except Exception as e:
            print(f"❌ Full analysis failed: {e}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

def test_provider_selection():
    """Test different AI provider configurations"""
    print("🔧 Testing AI Provider Selection")
    print("=" * 40)
    
    # Test different configurations
    test_configs = [
        ('auto', 'Auto-select best available provider'),
        ('openai', 'OpenAI only'),
        ('gemini', 'Gemini only')
    ]
    
    for provider, description in test_configs:
        print(f"\n📋 Testing: {description} (AI_PROVIDER={provider})")
        
        # Temporarily set the provider
        original_provider = os.environ.get('AI_PROVIDER', 'auto')
        os.environ['AI_PROVIDER'] = provider
        
        try:
            analyzer = MoodAnalyzer()
            print(f"   OpenAI Available: {'✅' if analyzer.openai_available else '❌'}")
            print(f"   Gemini Available: {'✅' if analyzer.gemini_available else '❌'}")
            print(f"   Selected Provider: {analyzer.ai_provider}")
        except Exception as e:
            print(f"   ❌ Failed: {e}")
        finally:
            # Restore original setting
            os.environ['AI_PROVIDER'] = original_provider

def main():
    print("🚀 Google Gemini Integration Test")
    print("=" * 60)
    print()
    
    # Run tests
    test_gemini_availability()
    print()
    test_provider_selection()
    print()
    test_gemini_analysis()
    
    print("\n✅ Test completed!")

if __name__ == "__main__":
    main()
