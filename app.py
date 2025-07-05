from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import os
from config import Config
from spotify_client import SpotifyClient
from mood_analyzer import MoodAnalyzer

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize clients
spotify_client = SpotifyClient()
mood_analyzer = MoodAnalyzer()

@app.route('/')
def index():
    """Main demo page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_playlist():
    """Analyze a playlist for mood suggestions"""
    try:
        data = request.get_json()
        playlist_url = data.get('playlist_url')
        
        if not playlist_url:
            return jsonify({'error': 'Playlist URL is required'}), 400
        
        # Analyze playlist with Spotify API
        playlist_data = spotify_client.analyze_playlist(playlist_url)
        
        if not playlist_data:
            return jsonify({'error': 'Could not analyze playlist. Check the URL and try again.'}), 400
        
        # Get mood analysis
        mood_analysis = mood_analyzer.combine_analysis(playlist_data)
        
        return jsonify({
            'success': True,
            'analysis': mood_analysis
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sample-playlists')
def get_sample_playlists():
    """Get sample playlists for demo"""
    return jsonify({
        'playlists': spotify_client.get_sample_playlists()
    })

@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """Analyze multiple playlists (for bulk operations)"""
    try:
        data = request.get_json()
        playlist_urls = data.get('playlist_urls', [])
        
        if not playlist_urls:
            return jsonify({'error': 'Playlist URLs are required'}), 400
        
        results = []
        
        for url in playlist_urls:
            try:
                playlist_data = spotify_client.analyze_playlist(url)
                if playlist_data:
                    mood_analysis = mood_analyzer.combine_analysis(playlist_data)
                    results.append({
                        'url': url,
                        'success': True,
                        'analysis': mood_analysis
                    })
                else:
                    results.append({
                        'url': url,
                        'success': False,
                        'error': 'Could not analyze playlist'
                    })
            except Exception as e:
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total_processed': len(results),
            'successful': len([r for r in results if r['success']])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/mood-info/<mood>')
def get_mood_info(mood):
    """Get detailed information about a mood category"""
    try:
        mood_info = mood_analyzer.get_mood_explanation(mood)
        return jsonify(mood_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playlist-info', methods=['POST'])
def get_playlist_info():
    """Get basic playlist information without full analysis"""
    try:
        data = request.get_json()
        playlist_url = data.get('playlist_url')
        
        if not playlist_url:
            return jsonify({'error': 'Playlist URL is required'}), 400
        
        playlist_info = spotify_client.get_playlist_info(playlist_url)
        
        if not playlist_info:
            return jsonify({'error': 'Could not fetch playlist info'}), 400
        
        return jsonify({
            'success': True,
            'playlist_info': playlist_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/approved-moods', methods=['POST'])
def save_approved_moods():
    """Save approved mood tags (demo endpoint)"""
    try:
        data = request.get_json()
        
        # In a real app, this would save to Firebase
        # For demo, we'll just return success
        return jsonify({
            'success': True,
            'message': 'Moods saved successfully',
            'data': data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'spotify_configured': bool(Config.SPOTIFY_CLIENT_ID != 'your_spotify_client_id'),
        'openai_configured': bool(Config.OPENAI_API_KEY != 'your_openai_api_key'),
        'gemini_configured': bool(Config.GEMINI_API_KEY != 'your_gemini_api_key_here'),
        'ai_provider': Config.AI_PROVIDER
    })

if __name__ == '__main__':
    # Check if SSL certificate files exist
    import os
    if os.path.exists('localhost.crt') and os.path.exists('localhost.key'):
        print("🔒 Starting HTTPS server...")
        print("📱 Demo will be available at: https://localhost:5000")
        print("⚠️  You may need to accept the security warning in your browser")
        app.run(debug=True, host='0.0.0.0', port=5000, 
                ssl_context=('localhost.crt', 'localhost.key'))
    else:
        print("🌐 Starting HTTP server...")
        print("📱 Demo will be available at: http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000) 