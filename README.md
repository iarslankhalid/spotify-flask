# 🎵 Spotify Mood Analyzer

An AI-powered Flask web application that analyzes Spotify playlists to suggest appropriate mood tags. The system combines Spotify's audio features with AI analysis to provide intelligent mood categorization for music playlists.

## ✨ Features

- **🎧 Spotify API Integration**: Extracts comprehensive audio features (tempo, energy, valence, danceability, etc.) from playlist tracks
- **🤖 AI Mood Analysis**: Supports both OpenAI GPT and Google Gemini for intelligent mood suggestion
- **📊 Rule-based Mood Mapping**: Combines audio features with predefined mood categories for accurate analysis
- **🖥️ Clean Web Interface**: Simple and intuitive web interface for playlist analysis
- **⚡ Flexible AI Provider**: Auto-fallback between OpenAI and Gemini APIs
- **🔒 Secure Configuration**: Environment-based configuration for API keys

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Spotify Developer Account
- OpenAI API Key (optional) or Google Gemini API Key (optional)

### 1. Clone & Install

```bash
git clone <your-repo-url>
cd spotify-flask
pip install -r requirements.txt
```

### 2. Get API Keys

#### Spotify API (Required):
1. Visit [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Note your `Client ID` and `Client Secret`

#### AI Provider (At least one required):

**Option A - OpenAI:**
1. Visit [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key

**Option B - Google Gemini:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key

### 3. Configure Environment

Copy the example environment file and configure it:
```bash
cp .env.example .env
```

Edit `.env` with your actual API keys:
```env
SPOTIFY_CLIENT_ID=your_actual_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_actual_spotify_client_secret
AI_PROVIDER=auto
OPENAI_API_KEY=your_actual_openai_api_key  # Optional
GEMINI_API_KEY=your_actual_gemini_api_key  # Optional
```

### 4. Run the Application
```bash
python app.py
```

Open your browser and navigate to `http://localhost:5000`

## 🎯 How to Use

### Analyze a Playlist
1. Copy a Spotify playlist URL (e.g., `https://open.spotify.com/playlist/...`)
2. Paste it into the input field on the homepage
3. Click "Analyze Mood"
4. View the AI-generated mood analysis with confidence scores

### Sample Playlists
The application includes sample playlists for testing different mood categories.

## 🔧 How It Works

### 1. Audio Feature Extraction
The system connects to Spotify's Web API to extract detailed audio features:
- Extracts features: energy, valence, tempo, acousticness, danceability, etc.
- Processes all tracks in the playlist

### 2. Mood Mapping Algorithm
- **Rule-based**: Maps audio features to mood categories
  - Calming: Low energy + high acousticness + low tempo
  - Euphoric: High energy + high valence + high danceability
  - Introspective: Low energy + low valence + moderate acousticness
- **AI-assisted**: Uses GPT to analyze playlist context and suggest moods
- **Combined**: Merges both approaches (60% rule-based, 40% AI)

### 3. Admin Review Process
- Shows top 3 mood suggestions with confidence scores
- Provides reasoning for each suggestion
- Allows manual review and approval
- Simulates Firebase integration for saving approved moods

## API Endpoints

- `GET /` - Main demo interface
- `POST /api/analyze` - Analyze single playlist
- `POST /api/analyze-batch` - Analyze multiple playlists
- `GET /api/sample-playlists` - Get sample playlists for testing
- `POST /api/approved-moods` - Save approved mood tags
- `GET /api/health` - Check system configuration

- **Calming**: Peaceful, relaxing, serene music
- **Euphoric**: Uplifting, joyful, high-energy tracks
- **Introspective**: Thoughtful, contemplative, reflective songs
- **Energetic**: Dynamic, vigorous, workout-ready music
- **Melancholic**: Sad, sorrowful, emotional ballads
- **Romantic**: Loving, tender, passionate love songs

## 📁 Project Structure

```
spotify-flask/
├── app.py                 # Main Flask application
├── config.py             # Configuration management
├── mood_analyzer.py      # Mood analysis logic
├── spotify_client.py     # Spotify API integration
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore           # Git ignore rules
├── README.md            # This file
├── templates/           # HTML templates
│   └── index.html      # Main web interface
├── docs/                # Documentation
│   ├── DEMO_INSTRUCTIONS.md
│   └── detail.txt
├── tests/               # Test files
│   ├── test_*.py       # Various test modules
├── utils/               # Utility scripts
│   ├── check_*.py      # API checking utilities
│   ├── run_demo.*      # Demo runners
│   └── temp_analyze.py # Temporary analysis script
└── ssl_certs/          # SSL certificates (for HTTPS)
    ├── *.crt          # Certificate files
    ├── *.key          # Private keys
    └── *ssl*.py       # SSL generation scripts
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main demo interface |
| `POST` | `/api/analyze` | Analyze single playlist |
| `GET` | `/api/sample-playlists` | Get sample playlists for testing |

## 🧪 Testing

Run tests using:
```bash
# Run all tests
python -m pytest tests/

# Run specific test
python tests/test_spotify.py
```

## 🔧 Development

### Utility Scripts
- `utils/check_gemini_models.py` - Check available Gemini models
- `utils/check_https.py` - Verify HTTPS configuration
- `utils/run_demo.py` - Quick demo runner

### SSL Support
The application includes SSL certificate generation for HTTPS development:
```bash
python ssl_certs/generate_ssl.py
```

## 🚀 Deployment

### Environment Variables for Production
```env
FLASK_ENV=production
AI_PROVIDER=auto
SPOTIFY_CLIENT_ID=prod_client_id
SPOTIFY_CLIENT_SECRET=prod_client_secret
OPENAI_API_KEY=prod_openai_key
GEMINI_API_KEY=prod_gemini_key
```

### Docker Support (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `python -m pytest tests/`
6. Commit changes: `git commit -am 'Add feature'`
7. Push to branch: `git push origin feature-name`
8. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**"Invalid Spotify URL"**
- Ensure the URL is a valid Spotify playlist link
- Check that the playlist is public

**"API Key Error"**
- Verify your API keys in the `.env` file
- Check that your Spotify app has the correct permissions

**"No AI Provider Available"**
- Ensure at least one AI provider (OpenAI or Gemini) is configured
- Check your API key validity and quotas

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Verify your API keys and permissions
3. Review the troubleshooting section above
4. Open an issue on GitHub with detailed error information

---

**Made with ❤️ for intelligent music mood analysis**

1. **Twice-yearly Bulk Updates**: Batch analysis handles multiple playlists
2. **Manual Review**: Admin interface for approving/editing suggestions
3. **Firebase Integration**: Ready to connect to existing Firebase database
4. **Spotify Link Processing**: Handles various Spotify URL formats
5. **Confidence Scoring**: Shows how confident the system is in each suggestion

## Sample Playlists

The demo includes sample playlists for testing:
- Chill Vibes (for calming mood)
- Upbeat Pop (for euphoric mood)
- Indie Folk (for introspective mood)
- Electronic Dance (for energetic mood)

## Next Steps for Production

1. **Firebase Integration**: Connect to John's existing Firebase database
2. **User Authentication**: Add login system for admin access
3. **Improved UI**: Enhanced interface with better UX
4. **Advanced Analytics**: Track accuracy and user feedback
5. **Custom Mood Categories**: Allow John to define custom mood categories
6. **YouTube Integration**: Add YouTube playlist support as mentioned

## Technical Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, Bootstrap, JavaScript
- **APIs**: Spotify Web API, OpenAI GPT-3.5
- **Database**: Ready for Firebase integration
- **Deployment**: Can be deployed to any cloud platform

## Contact

This demo shows exactly what you described in your proposal. The system combines Spotify's audio features with AI to automatically suggest moods, provides an admin interface for review, and handles the bulk operations John needs for his twice-yearly updates.

Ready to discuss next steps and implementation details! 