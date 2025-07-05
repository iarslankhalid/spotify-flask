#!/usr/bin/env python3
"""
Test Spotify API connectivity and show expected mood analysis output
"""

import os
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

def test_spotify_connection():
    """Test if Spotify API is working"""
    print("🎵 Testing Spotify Connection...")
    
    try:
        client = SpotifyClient()
        
        # Test with a simple, guaranteed working playlist
        test_url = "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"  # Today's Top Hits
        
        print(f"📡 Testing with: {test_url}")
        
        # Test basic playlist info
        playlist_info = client.get_playlist_info(test_url)
        
        if playlist_info:
            print("✅ Spotify API connection successful!")
            print(f"   Playlist: {playlist_info['name']}")
            print(f"   Tracks: {playlist_info['total_tracks']}")
            print(f"   URL: {playlist_info['url']}")
            return True
        else:
            print("❌ Failed to get playlist info")
            return False
            
    except Exception as e:
        print(f"❌ Spotify API Error: {str(e)}")
        return False

def test_mood_analysis():
    """Test mood analysis with sample data"""
    print("\n🧠 Testing Mood Analysis...")
    
    try:
        analyzer = MoodAnalyzer()
        
        # Create sample audio features for testing
        sample_track = {
            'id': 'test123',
            'energy': 0.8,
            'valence': 0.9,
            'tempo': 120,
            'acousticness': 0.1,
            'danceability': 0.7
        }
        
        # Test mood calculation
        mood_scores = analyzer.analyze_track_mood(sample_track)
        
        print("✅ Mood analysis working!")
        print("   Sample mood scores:")
        for mood, score in sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)[:3]:
            print(f"   - {mood}: {score:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Mood Analysis Error: {str(e)}")
        return False

def show_expected_output():
    """Show what the mood recommendations should look like"""
    print("\n🎯 Expected Mood Display Format:")
    print("=" * 50)
    
    sample_recommendations = [
        {
            'mood': 'euphoric',
            'confidence': 0.85,
            'reasoning': 'High energy tracks with positive valence and upbeat tempo',
            'keywords': ['uplifting', 'joyful', 'ecstatic', 'blissful', 'elated']
        },
        {
            'mood': 'energetic', 
            'confidence': 0.72,
            'reasoning': 'Strong danceability and high tempo indicate energetic mood',
            'keywords': ['dynamic', 'vigorous', 'powerful', 'intense', 'driving']
        },
        {
            'mood': 'calming',
            'confidence': 0.45,
            'reasoning': 'Some acoustic elements provide moments of calm',
            'keywords': ['peaceful', 'relaxing', 'serene', 'tranquil', 'soothing']
        }
    ]
    
    for i, rec in enumerate(sample_recommendations, 1):
        confidence = int(rec['confidence'] * 100)
        print(f"\n{i}. {rec['mood'].upper()} - {confidence}% confidence")
        print(f"   Reasoning: {rec['reasoning']}")
        print(f"   Keywords: {', '.join(rec['keywords'][:3])}")

def main():
    """Run all tests"""
    print("🧪 Spotify Mood Analyzer - Connection Test")
    print("=" * 50)
    
    # Test Spotify connection
    spotify_ok = test_spotify_connection()
    
    # Test mood analysis
    mood_ok = test_mood_analysis()
    
    # Show expected output
    show_expected_output()
    
    print("\n" + "=" * 50)
    if spotify_ok and mood_ok:
        print("✅ All systems working! Mood tags should display properly.")
        print("\n💡 If mood tags still don't show in the web interface:")
        print("   1. Check browser console for JavaScript errors")
        print("   2. Try the updated sample playlists")
        print("   3. Ensure .env file has valid API keys")
    else:
        print("❌ Issues detected. Please check:")
        print("   1. Spotify API keys in .env file")
        print("   2. Internet connection")
        print("   3. API key permissions")

if __name__ == "__main__":
    main() 