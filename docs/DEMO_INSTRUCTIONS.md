# 🚀 QUICK DEMO SETUP

## ⚡ Get Started in 5 Minutes

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Your API Keys (Free!)

**Spotify API** (Required for playlist analysis):
- Go to https://developer.spotify.com/dashboard
- Click "Create an app"
- Name it anything (e.g., "Mood Analyzer Demo")
- Copy your Client ID and Client Secret

**OpenAI API** (Required for AI suggestions):
- Go to https://platform.openai.com/api-keys
- Create new secret key
- Copy the key (starts with `sk-`)

### 3. Create `.env` File
Create a file called `.env` in this folder with your keys:
```
SPOTIFY_CLIENT_ID=your_spotify_client_id_here
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret_here
OPENAI_API_KEY=your_openai_api_key_here
FLASK_ENV=development
FLASK_SECRET_KEY=demo_secret_key_123
```

### 4. Run the Demo
```bash
python app.py
```

Open your browser to: **http://localhost:5000**

---

## 🎬 Demo Script for John

### What You'll Show:

1. **Homepage** - Clean, professional interface
2. **Spotify Integration** - Enter a playlist URL, watch it analyze
3. **AI Mood Suggestions** - See the top 3 moods with confidence scores
4. **Admin Interface** - Show approve/edit/save buttons
5. **Batch Processing** - Demo multiple playlists at once

### Sample Playlists to Use:
- **Chill Vibes**: https://open.spotify.com/playlist/37i9dQZF1DX4WYpdgoIcn6
- **Indie Folk**: https://open.spotify.com/playlist/37i9dQZF1DX2Nc3B70tvx0
- **Electronic**: https://open.spotify.com/playlist/37i9dQZF1DX6J5NfMJS675

### Key Points to Highlight:
- **Automated Analysis**: No more manual mood tagging
- **AI + Data**: Combines Spotify audio features with GPT intelligence
- **Bulk Operations**: Handle 100+ playlists in one batch
- **Admin Control**: John can review, edit, approve all suggestions
- **Firebase Ready**: Integrates with his existing database

### Demo Flow (10 minutes):
1. **Introduction** (2 min): Show the interface and explain the problem it solves
2. **Single Analysis** (4 min): Analyze one playlist, show results, explain the mood suggestions
3. **Batch Processing** (2 min): Demo multiple playlists at once
4. **Admin Features** (2 min): Show approval workflow and Firebase integration

---

## 🔧 Troubleshooting

**If you get API errors:**
- Check your `.env` file has real API keys (not placeholders)
- Make sure there are no spaces around the `=` signs
- Restart the server after updating `.env`

**If playlists won't analyze:**
- Make sure the Spotify playlist is public
- Try with the sample playlists first
- Check your Spotify API keys are correct

**Quick test without API keys:**
- The demo will start but show "Please configure API keys"
- You can still see the interface design

---

## 💡 What Makes This Demo Special

1. **Real Working Code**: Not just mockups - actual Spotify API integration
2. **AI-Powered**: Uses GPT to understand context and suggest appropriate moods
3. **Production Ready**: Can handle John's actual workflow (twice-yearly bulk updates)
4. **Professional UI**: Clean, modern interface that looks trustworthy
5. **Scalable**: Built to handle hundreds of playlists efficiently

**This shows John exactly what he's getting - a complete, working solution that solves his exact problem.**

---

## 📞 Ready to Present?

Once you've tested the demo:
1. Take some screenshots of the results
2. Record a 2-3 minute video showing the workflow
3. Send John the Loom link with the demo explanation

**You've got this! The demo proves your technical skills and shows you understand his exact needs.** 