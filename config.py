import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Spotify API credentials
    SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID', 'your_spotify_client_id')
    SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET', 'your_spotify_client_secret')
    
    # OpenAI API key
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')
    
    # Google Gemini API key
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your_gemini_api_key')
    
    # AI Provider preference (openai, gemini, or auto)
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'auto')  # auto will try OpenAI first, then Gemini
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev_secret_key_change_in_production')
    
    # Mood categories for mapping
    MOOD_CATEGORIES = {
        'calming': {
            'keywords': ['peaceful', 'relaxing', 'serene', 'tranquil', 'soothing'],
            'audio_features': {
                'energy': (0.0, 0.4),
                'valence': (0.0, 0.6),
                'tempo': (60, 120),
                'acousticness': (0.3, 1.0)
            }
        },
        'euphoric': {
            'keywords': ['uplifting', 'joyful', 'ecstatic', 'blissful', 'elated'],
            'audio_features': {
                'energy': (0.6, 1.0),
                'valence': (0.7, 1.0),
                'tempo': (120, 200),
                'danceability': (0.5, 1.0)
            }
        },
        'introspective': {
            'keywords': ['thoughtful', 'contemplative', 'reflective', 'meditative', 'pensive'],
            'audio_features': {
                'energy': (0.0, 0.5),
                'valence': (0.0, 0.5),
                'acousticness': (0.4, 1.0),
                'instrumentalness': (0.2, 1.0)
            }
        },
        'energetic': {
            'keywords': ['dynamic', 'vigorous', 'powerful', 'intense', 'driving'],
            'audio_features': {
                'energy': (0.7, 1.0),
                'tempo': (130, 200),
                'danceability': (0.6, 1.0),
                'loudness': (-8, 0)
            }
        },
        'melancholic': {
            'keywords': ['sad', 'sorrowful', 'wistful', 'nostalgic', 'melancholy'],
            'audio_features': {
                'energy': (0.0, 0.4),
                'valence': (0.0, 0.3),
                'tempo': (60, 120),
                'mode': 0  # Minor key
            }
        },
        'romantic': {
            'keywords': ['loving', 'tender', 'passionate', 'intimate', 'affectionate'],
            'audio_features': {
                'energy': (0.2, 0.7),
                'valence': (0.4, 0.8),
                'acousticness': (0.3, 1.0),
                'danceability': (0.3, 0.8)
            }
        }
    } 