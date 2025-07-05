#!/usr/bin/env python3
"""
Test the specific playlist analysis
"""

import json
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

def test_playlist_analysis():
    """Test the specific playlist"""
    playlist_url = "https://open.spotify.com/playlist/2mT6LpOU4ipJ0BkoCigAiw?si=a9560a2a841542f6&nd=1&dlsi=d54117c9f0434850"
    
    print("🎵 Testing Playlist Analysis")
    print("=" * 50)
    print(f"URL: {playlist_url}")
    print()
    
    try:
        # Initialize clients
        client = SpotifyClient()
        analyzer = MoodAnalyzer()
        
        # Step 1: Get playlist info
        print("Step 1: Getting playlist information...")
        playlist_info = client.get_playlist_info(playlist_url)
        
        if not playlist_info:
            print("❌ Could not fetch playlist info")
            return
        
        print(f"✅ Playlist found:")
        print(f"   Name: {playlist_info['name']}")
        print(f"   Description: {playlist_info.get('description', 'No description')}")
        print(f"   Total tracks: {playlist_info['total_tracks']}")
        print(f"   Owner: {playlist_info['owner']}")
        if playlist_info.get('image'):
            print(f"   Cover image: {playlist_info['image']}")
        print()
        
        # Step 2: Get tracks
        print("Step 2: Getting track listings...")
        tracks = client.get_playlist_tracks(playlist_url)
        
        if tracks:
            print(f"✅ Retrieved {len(tracks)} tracks")
            print("   Sample tracks:")
            for i, track in enumerate(tracks[:5], 1):
                duration_min = track['duration_ms'] // 60000
                duration_sec = (track['duration_ms'] % 60000) // 1000
                print(f"   {i}. {track['name']} by {', '.join(track['artists'])} ({duration_min}:{duration_sec:02d})")
            print()
        else:
            print("❌ Could not retrieve tracks")
            return
        
        # Step 3: Try to get audio features
        print("Step 3: Attempting to get audio features...")
        track_ids = [track['id'] for track in tracks[:10]]  # Test with first 10 tracks
        audio_features = client.get_audio_features(track_ids)
        
        if audio_features:
            print(f"✅ Got audio features for {len(audio_features)} tracks")
            print("   Sample audio features:")
            for feature in audio_features[:3]:
                print(f"   - Track ID: {feature['id'][:10]}...")
                print(f"     Energy: {feature['energy']:.2f}, Valence: {feature['valence']:.2f}")
                print(f"     Tempo: {feature['tempo']:.0f} BPM, Danceability: {feature['danceability']:.2f}")
        else:
            print("❌ Could not get audio features (403 Forbidden)")
            print("   This is likely due to Spotify API access restrictions")
            print("   The playlist is accessible but audio features require special permissions")
        
        print()
        print("📊 SUMMARY:")
        print("=" * 30)
        print(f"✅ Playlist URL: VALID")
        print(f"✅ Playlist Info: ACCESSIBLE")
        print(f"✅ Track Listings: ACCESSIBLE")
        print(f"❌ Audio Features: RESTRICTED (403 error)")
        print()
        print("💡 CONCLUSION:")
        print("The playlist can be analyzed for basic information and track listings,")
        print("but audio feature analysis requires updated Spotify API permissions.")
        
        # Calculate total duration
        total_duration_ms = sum(track['duration_ms'] for track in tracks)
        total_minutes = total_duration_ms // 60000
        total_seconds = (total_duration_ms % 60000) // 1000
        total_hours = total_minutes // 60
        remaining_minutes = total_minutes % 60
        
        print(f"\n⏱️  PLAYLIST DURATION:")
        if total_hours > 0:
            print(f"   Total duration: {total_hours}h {remaining_minutes}m {total_seconds}s")
        else:
            print(f"   Total duration: {total_minutes}m {total_seconds}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_playlist_analysis()
