#!/usr/bin/env python3
"""
Test the mood analysis with a mock OpenAI response to verify the complete flow
"""

import json
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

class MockOpenAI:
    """Mock OpenAI client for testing"""
    
    class Chat:
        class Completions:
            def create(self, **kwargs):
                # Mock response that matches the expected format
                mock_response = {
                    "suggestions": [
                        {
                            "mood": "ambient",
                            "confidence": 0.92,
                            "reasoning": "The playlist features ambient and drone artists like Stars Of The Lid, which are characteristic of ambient, meditative music designed for therapeutic purposes."
                        },
                        {
                            "mood": "meditative",
                            "confidence": 0.85,
                            "reasoning": "The therapeutic nature and the long-form, contemplative tracks suggest a meditative mood intended for healing and introspection."
                        },
                        {
                            "mood": "downtempo",
                            "confidence": 0.78,
                            "reasoning": "The slow, atmospheric nature of the tracks and artists like Harold Budd indicate a downtempo, relaxed approach to music."
                        }
                    ],
                    "overall_assessment": "This playlist appears to be specifically curated for therapeutic and meditative purposes, featuring ambient drone and neo-classical artists known for creating immersive, healing soundscapes."
                }
                
                class MockResponse:
                    def __init__(self, content):
                        self.choices = [type('obj', (object,), {
                            'message': type('obj', (object,), {
                                'content': json.dumps(content)
                            })()
                        })()]
                
                return MockResponse(mock_response)
    
    def __init__(self, **kwargs):
        self.chat = self.Chat()
        self.chat.completions = self.Chat.Completions()

def main():
    print("🎵 Testing Playlist Analysis with Mock OpenAI")
    print("=" * 60)
    
    # The playlist URL you want to test
    playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
    
    # Initialize clients
    spotify_client = SpotifyClient()
    mood_analyzer = MoodAnalyzer()
    
    # Replace OpenAI client with mock
    mood_analyzer.openai_client = MockOpenAI()
    
    try:
        print(f"📡 Analyzing playlist: {playlist_url}")
        print()
        
        # Step 1: Get playlist data
        print("Step 1: Getting playlist info and tracks...")
        playlist_data = spotify_client.analyze_playlist(playlist_url)
        
        if not playlist_data:
            print("❌ Could not analyze playlist")
            return
        
        playlist_info = playlist_data['playlist_info']
        print(f"✅ Found playlist: '{playlist_info['name']}'")
        print(f"   Description: {playlist_info.get('description', 'No description')[:100]}...")
        print(f"   Total tracks: {playlist_data['total_tracks']}")
        print(f"   Tracks with audio features: {playlist_data['total_with_features']}")
        print(f"   Total duration: {playlist_data.get('total_duration_formatted', 'Not calculated')}")
        print()
        
        # Show sample tracks
        print("🎵 Sample tracks:")
        for i, track in enumerate(playlist_data['tracks'][:5], 1):
            artists = ', '.join(track['artists'])
            print(f"   {i}. {track['name']} by {artists}")
        print()
        
        # Step 2: Run mood analysis
        print("Step 2: Running AI mood analysis with mock...")
        mood_analysis = mood_analyzer.combine_analysis(playlist_data)
        
        # Show results
        print("✅ Analysis complete!")
        print()
        print("🎯 MOOD RECOMMENDATIONS:")
        print("=" * 40)
        
        # AI suggestions
        ai_suggestions = mood_analysis.get('ai_suggestions', {})
        print(f"🤖 AI Assessment:")
        print(f"   {ai_suggestions.get('overall_assessment', 'No assessment available')}")
        print()
        
        suggestions = ai_suggestions.get('suggestions', [])
        if suggestions:
            print("📊 Top AI-suggested moods:")
            for i, suggestion in enumerate(suggestions, 1):
                mood = suggestion.get('mood', 'Unknown')
                confidence = suggestion.get('confidence', 0)
                reasoning = suggestion.get('reasoning', 'No reasoning provided')
                print(f"   {i}. {mood.upper()} ({confidence:.0%} confidence)")
                print(f"      → {reasoning}")
                print()
        
        # Final recommendations
        final_recs = mood_analysis.get('final_recommendations', [])
        if final_recs:
            print("🎯 Final Recommendations:")
            for i, rec in enumerate(final_recs, 1):
                mood = rec.get('mood', 'Unknown')
                score = rec.get('score', 0)
                source = rec.get('source', 'Unknown')
                print(f"   {i}. {mood.upper()} - Score: {score:.2f} (Source: {source})")
        
        if playlist_data['total_with_features'] == 0:
            print()
            print("⚠️  Note: Audio features unavailable - analysis based on track names and context")
        
        print()
        print("✅ SUCCESS: The complete mood analysis pipeline is working!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
