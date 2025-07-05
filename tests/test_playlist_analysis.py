#!/usr/bin/env python3
"""
Test the specific playlist analysis functionality
"""

import json
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

def main():
    print("🎵 Testing Playlist Analysis")
    print("=" * 50)
    
    # The playlist URL you want to test
    playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
    
    # Initialize clients
    spotify_client = SpotifyClient()
    mood_analyzer = MoodAnalyzer()
    
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
        print(f"   Description: {playlist_info.get('description', 'No description')}")
        print(f"   Total tracks: {playlist_data['total_tracks']}")
        print(f"   Tracks with audio features: {playlist_data['total_with_features']}")
        print()
        
        # Show sample tracks
        print("🎵 Sample tracks:")
        for i, track in enumerate(playlist_data['tracks'][:5], 1):
            artists = ', '.join(track['artists'])
            print(f"   {i}. {track['name']} by {artists}")
        print()
        
        # Step 2: Run mood analysis
        print("Step 2: Running AI mood analysis...")
        mood_analysis = mood_analyzer.combine_analysis(playlist_data)
        
        # Show results
        print("✅ Analysis complete!")
        print()
        print("🎯 MOOD RECOMMENDATIONS:")
        print("=" * 40)
        
        for i, rec in enumerate(mood_analysis['final_recommendations'], 1):
            confidence = int(rec['confidence'] * 100)
            print(f"{i}. {rec['mood'].upper()} - {confidence}% confidence")
            print(f"   Reasoning: {rec['reasoning']}")
            print(f"   Keywords: {', '.join(rec['keywords'][:3])}")
            print()
        
        # Show AI analysis details
        ai_suggestions = mood_analysis.get('ai_suggestions', {})
        if ai_suggestions.get('overall_assessment'):
            print("🤖 AI Assessment:")
            print(f"   {ai_suggestions['overall_assessment']}")
            print()
        
        # Show rule-based analysis status
        rule_based = mood_analysis.get('rule_based_analysis', {})
        if rule_based.get('error'):
            print("⚠️  Note: Audio features unavailable - analysis based on track names and context")
        else:
            print(f"📊 Audio features analyzed for {rule_based.get('total_tracks_analyzed', 0)} tracks")
        
        print()
        print("✅ SUCCESS: The playlist was successfully analyzed!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
