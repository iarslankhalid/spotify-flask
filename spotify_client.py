import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from config import Config

class SpotifyClient:
    def __init__(self):
        self.client_credentials_manager = SpotifyClientCredentials(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
    
    def extract_playlist_id(self, spotify_url):
        """Extract playlist ID from Spotify URL"""
        # Handle different Spotify URL formats
        patterns = [
            r'spotify:playlist:([a-zA-Z0-9]+)',
            r'open\.spotify\.com/playlist/([a-zA-Z0-9]+)',
            r'spotify\.com/playlist/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, spotify_url)
            if match:
                return match.group(1)
        
        # If no pattern matches, assume it's already a playlist ID
        return spotify_url
    
    def get_playlist_info(self, playlist_url):
        """Get basic playlist information"""
        try:
            playlist_id = self.extract_playlist_id(playlist_url)
            playlist = self.sp.playlist(playlist_id)
            
            return {
                'id': playlist['id'],
                'name': playlist['name'],
                'description': playlist.get('description', ''),
                'total_tracks': playlist['tracks']['total'],
                'url': playlist['external_urls']['spotify'],
                'image': playlist['images'][0]['url'] if playlist['images'] else None,
                'owner': playlist['owner']['display_name']
            }
        except Exception as e:
            print(f"Error fetching playlist info: {str(e)}")
            return None
    
    def get_playlist_tracks(self, playlist_url):
        """Get all tracks from a playlist"""
        try:
            playlist_id = self.extract_playlist_id(playlist_url)
            
            tracks = []
            results = self.sp.playlist_tracks(playlist_id)
            
            while results:
                for item in results['items']:
                    if item['track'] and item['track']['id']:
                        track_info = {
                            'id': item['track']['id'],
                            'name': item['track']['name'],
                            'artists': [artist['name'] for artist in item['track']['artists']],
                            'album': item['track']['album']['name'],
                            'duration_ms': item['track']['duration_ms'],
                            'popularity': item['track']['popularity'],
                            'preview_url': item['track']['preview_url'],
                            'external_urls': item['track']['external_urls']
                        }
                        tracks.append(track_info)
                
                results = self.sp.next(results) if results['next'] else None
            
            return tracks
        except Exception as e:
            print(f"Error fetching playlist tracks: {str(e)}")
            return []
    
    def get_audio_features(self, track_ids):
        """Get audio features for multiple tracks"""
        try:
            # Spotify API can handle up to 100 tracks at once
            audio_features = []
            
            for i in range(0, len(track_ids), 100):
                batch = track_ids[i:i+100]
                features = self.sp.audio_features(batch)
                
                for feature in features:
                    if feature:  # Some tracks might not have audio features
                        audio_features.append({
                            'id': feature['id'],
                            'acousticness': feature['acousticness'],
                            'danceability': feature['danceability'],
                            'energy': feature['energy'],
                            'instrumentalness': feature['instrumentalness'],
                            'liveness': feature['liveness'],
                            'loudness': feature['loudness'],
                            'speechiness': feature['speechiness'],
                            'tempo': feature['tempo'],
                            'valence': feature['valence'],
                            'mode': feature['mode'],
                            'key': feature['key'],
                            'time_signature': feature['time_signature']
                        })
            
            return audio_features
        except Exception as e:
            print(f"Error fetching audio features: {str(e)}")
            return []
    
    def analyze_playlist(self, playlist_url):
        """Complete playlist analysis with tracks and audio features"""
        try:
            # Get playlist info
            playlist_info = self.get_playlist_info(playlist_url)
            if not playlist_info:
                return None
            
            # Get tracks
            tracks = self.get_playlist_tracks(playlist_url)
            if not tracks:
                return None
            
            # Get audio features
            track_ids = [track['id'] for track in tracks]
            audio_features = self.get_audio_features(track_ids)
            
            # Combine track info with audio features
            features_dict = {f['id']: f for f in audio_features}
            
            for track in tracks:
                track['audio_features'] = features_dict.get(track['id'], {})
            
            # Calculate total duration
            total_duration_ms = sum(track.get('duration_ms', 0) for track in tracks)
            total_duration_formatted = self.format_duration(total_duration_ms)
            
            return {
                'playlist_info': playlist_info,
                'tracks': tracks,
                'total_tracks': len(tracks),
                'total_with_features': len([t for t in tracks if t['audio_features']]),
                'total_duration_ms': total_duration_ms,
                'total_duration_formatted': total_duration_formatted
            }
        except Exception as e:
            print(f"Error analyzing playlist: {str(e)}")
            return None
    
    def format_duration(self, duration_ms):
        """Format duration from milliseconds to human-readable format"""
        if not duration_ms:
            return "0:00"
        
        total_seconds = duration_ms // 1000
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}"
    
    def get_sample_playlists(self):
        """Sample playlists for demo purposes - using verified working URLs"""
        return [
            {
                'name': 'Today\'s Top Hits',
                'url': 'https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M',
                'description': 'The hottest tracks right now'
            },
            {
                'name': 'Peaceful Piano',
                'url': 'https://open.spotify.com/playlist/37i9dQZF1DX4sWSpwABIL4', 
                'description': 'Peaceful piano music for relaxation'
            },
            {
                'name': 'Chill Hits',
                'url': 'https://open.spotify.com/playlist/37i9dQZF1DX0XUfTFmNBRM',
                'description': 'Chill out with these laid-back hits'
            },
            {
                'name': 'Happy Hits',
                'url': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC',
                'description': 'Feel good music to brighten your day'
            }
        ]