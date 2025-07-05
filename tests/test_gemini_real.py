#!/usr/bin/env python3
"""
Test Gemini playlist analysis with real API
"""

from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

def test_gemini_playlist_analysis():
    print("🎵 Testing Gemini Playlist Analysis")
    print("=" * 45)
    
    # Initialize clients
    spotify_client = SpotifyClient()
    mood_analyzer = MoodAnalyzer()
    
    print(f"Gemini Available: {'✅' if mood_analyzer.gemini_available else '❌'}")
    print(f"AI Provider: {mood_analyzer.ai_provider}")
    print()
    
    try:
        # Test playlist
        playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
        
        print(f"📡 Analyzing playlist...")
        playlist_data = spotify_client.analyze_playlist(playlist_url)
        
        if not playlist_data:
            print("❌ Could not get playlist data")
            return
        
        print(f"✅ Got playlist: {playlist_data['playlist_info']['name']}")
        print(f"   Duration: {playlist_data.get('total_duration_formatted', 'Not calculated')}")
        print(f"   Tracks: {playlist_data['total_tracks']}")
        print()
        
        # Test Gemini analysis
        print("🤖 Running Gemini mood analysis...")
        analysis = mood_analyzer.combine_analysis(playlist_data)
        
        print("✅ Analysis complete!")
        
        # Show results
        ai_suggestions = analysis.get('ai_suggestions', {})
        print(f"\n🎯 AI Assessment:")
        print(f"   {ai_suggestions.get('overall_assessment', 'No assessment')}")
        
        suggestions = ai_suggestions.get('suggestions', [])
        if suggestions:
            print(f"\n📊 Gemini Mood Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                mood = suggestion.get('mood', 'Unknown')
                confidence = suggestion.get('confidence', 0)
                reasoning = suggestion.get('reasoning', 'No reasoning')
                print(f"   {i}. {mood.upper()} ({confidence:.0%} confidence)")
                print(f"      → {reasoning}")
                print()
        
        if 'error' in ai_suggestions:
            print(f"❌ Error: {ai_suggestions['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_gemini_playlist_analysis()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Gemini playlist analysis test")
