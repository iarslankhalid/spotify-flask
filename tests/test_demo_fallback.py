#!/usr/bin/env python3
"""
Test the fallback AI functionality directly
"""

from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

def main():
    print("🎵 Testing Demo AI Fallback")
    print("=" * 40)
    
    # Initialize clients
    spotify_client = SpotifyClient()
    mood_analyzer = MoodAnalyzer()
    
    try:
        # Get playlist data
        playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
        print(f"📡 Getting playlist data...")
        playlist_data = spotify_client.analyze_playlist(playlist_url)
        
        if not playlist_data:
            print("❌ Could not get playlist data")
            return
        
        print(f"✅ Got playlist: {playlist_data['playlist_info']['name']}")
        print(f"   Duration: {playlist_data.get('total_duration_formatted', 'Not calculated')}")
        print()
        
        # Test the demo AI suggestions directly
        print("🎭 Testing demo AI suggestions...")
        demo_result = mood_analyzer.get_demo_ai_suggestions(playlist_data)
        
        print(f"✅ Demo AI suggestions generated!")
        print(f"   Assessment: {demo_result.get('overall_assessment', 'No assessment')}")
        print()
        
        suggestions = demo_result.get('suggestions', [])
        if suggestions:
            print("📊 Demo AI Suggestions:")
            for i, suggestion in enumerate(suggestions, 1):
                mood = suggestion.get('mood', 'Unknown')
                confidence = suggestion.get('confidence', 0)
                reasoning = suggestion.get('reasoning', 'No reasoning provided')
                print(f"   {i}. {mood.upper()} ({confidence:.0%} confidence)")
                print(f"      → {reasoning}")
                print()
        
        # Test the full analysis with fallback
        print("🔄 Testing full analysis with fallback...")
        full_analysis = mood_analyzer.combine_analysis(playlist_data)
        
        print("✅ Full analysis complete!")
        ai_suggestions = full_analysis.get('ai_suggestions', {})
        print(f"   AI Assessment: {ai_suggestions.get('overall_assessment', 'No assessment')}")
        
        final_recs = full_analysis.get('final_recommendations', [])
        if final_recs:
            print(f"   Final recommendations: {len(final_recs)} moods")
            for rec in final_recs[:3]:
                mood = rec.get('mood', 'Unknown')
                score = rec.get('score', 0)
                print(f"      - {mood.upper()}: {score:.2f}")
        
        print("\n✅ SUCCESS: Demo fallback is working!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
