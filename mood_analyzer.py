from typing import Dict, List, Tuple
from config import Config
from openai import OpenAI
import google.generativeai as genai
import os
import json

class MoodAnalyzer:
    def __init__(self):
        self.mood_categories = Config.MOOD_CATEGORIES
        self.ai_provider = Config.AI_PROVIDER.lower()
        
        # Initialize OpenAI client
        try:
            self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
            self.openai_available = bool(Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != 'your_openai_api_key')
        except Exception as e:
            print(f"OpenAI initialization failed: {e}")
            self.openai_client = None
            self.openai_available = False
        
        # Initialize Gemini client
        try:
            if Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'your_gemini_api_key_here':
                genai.configure(api_key=Config.GEMINI_API_KEY)
                # Use the current Gemini model name
                self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
                self.gemini_available = True
            else:
                self.gemini_model = None
                self.gemini_available = False
        except Exception as e:
            print(f"Gemini initialization failed: {e}")
            self.gemini_model = None
            self.gemini_available = False
    
    def calculate_feature_score(self, feature_value: float, feature_range: tuple) -> float:
        """Calculate how well a feature value fits within a range (0-1)"""
        if len(feature_range) == 2:
            min_val, max_val = feature_range
            if min_val <= feature_value <= max_val:
                return 1.0
            else:
                distance = min(abs(feature_value - min_val), abs(feature_value - max_val))
                return max(0.0, 1.0 - distance)
        else:
            return 1.0 if feature_value == feature_range else 0.0
    
    def analyze_track_mood(self, audio_features: Dict) -> Dict[str, float]:
        """Analyze a single track's mood based on audio features"""
        mood_scores = {}
        
        for mood, config in self.mood_categories.items():
            score = 0.0
            feature_count = 0
            
            for feature_name, feature_range in config['audio_features'].items():
                if feature_name in audio_features:
                    feature_value = audio_features[feature_name]
                    feature_score = self.calculate_feature_score(feature_value, feature_range)
                    score += feature_score
                    feature_count += 1
            
            if feature_count > 0:
                mood_scores[mood] = score / feature_count
            else:
                mood_scores[mood] = 0.0
        
        return mood_scores
    
    def analyze_playlist_mood(self, playlist_data: Dict) -> Dict:
        """Analyze overall playlist mood"""
        tracks = playlist_data['tracks']
        track_moods = []
        
        for track in tracks:
            if track.get('audio_features'):
                track_mood = self.analyze_track_mood(track['audio_features'])
                track_moods.append(track_mood)
                track['mood_scores'] = track_mood
        
        if not track_moods:
            return {'error': 'No tracks with audio features found'}
        
        # Calculate average mood scores across all tracks
        mood_averages = {}
        for mood in self.mood_categories.keys():
            scores = [track_mood.get(mood, 0) for track_mood in track_moods]
            mood_averages[mood] = sum(scores) / len(scores) if scores else 0.0
        
        top_moods = sorted(mood_averages.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            'playlist_info': playlist_data['playlist_info'],
            'mood_averages': mood_averages,
            'top_moods': top_moods,
            'total_tracks_analyzed': len(track_moods)
        }
    
    def get_ai_mood_suggestions(self, playlist_data: Dict) -> Dict:
        """Use AI to suggest moods based on playlist info"""
        try:
            playlist_info = playlist_data['playlist_info']
            
            context = f"""
            Playlist: {playlist_info['name']}
            Description: {playlist_info.get('description', 'No description')}
            Total Tracks: {playlist_data['total_tracks']}
            
            Sample tracks:
            """
            
            # Show more tracks if no audio features available
            sample_count = 10 if not any(track.get('audio_features') for track in playlist_data['tracks'][:10]) else 5
            
            for i, track in enumerate(playlist_data['tracks'][:sample_count]):
                context += f"\n{i+1}. {track['name']} by {', '.join(track['artists'])}"
                if track.get('audio_features'):
                    af = track['audio_features']
                    context += f" (Energy: {af.get('energy', 0):.2f}, Valence: {af.get('valence', 0):.2f})"
                
            # Add note about missing audio features if applicable
            if not any(track.get('audio_features') for track in playlist_data['tracks'][:5]):
                context += f"\n\nNote: Audio features not available, analyzing based on track names, artists, and playlist context."
            
            mood_list = list(self.mood_categories.keys())
            context += f"\n\nAvailable moods: {', '.join(mood_list)}"
            
            prompt = f"""
            Based on this playlist, suggest the top 3 most appropriate moods from the available options and explain why.
            
            {context}
            
            Available moods: {', '.join(mood_list)}
            
            Rules:
            - Only suggest moods from the available list
            - Provide confidence between 0.0 and 1.0
            - Give clear reasoning for each suggestion
            
            Respond in JSON format:
            {{
                "suggestions": [
                    {{
                        "mood": "mood_name",
                        "confidence": 0.85,
                        "reasoning": "explanation"
                    }}
                ],
                "overall_assessment": "brief description"
            }}
            """
            
            print(f"🤖 Sending request to OpenAI...")
            print(f"📝 Prompt length: {len(prompt)} characters")
            print(f"🔑 API Key present: {'sk-' in os.getenv('OPENAI_API_KEY', '')}")
            
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            content = response.choices[0].message.content
            print(f"✅ OpenAI response received: {len(content)} characters")
            print(f"📄 Raw response: {content[:200]}...")
            
            if not content:
                raise ValueError("No content in OpenAI response")
            
            result = json.loads(content)
            print(f"📊 AI suggested {len(result.get('suggestions', []))} moods")
            return result
            
        except Exception as e:
            error_str = str(e).lower()
            print(f"❌ OpenAI Error: {type(e).__name__}: {str(e)}")
            
            # Re-raise API-related errors so fallback can handle them
            if any(keyword in error_str for keyword in ['quota', 'rate limit', 'authentication', 'invalid_api_key', 'invalid api key']):
                raise e
            
            # For other errors, return error response
            import traceback
            print(f"🔍 Full traceback: {traceback.format_exc()}")
            return {
                "suggestions": [],
                "overall_assessment": "Unable to generate AI suggestions",
                "error": str(e)
            }
    
    def get_ai_mood_suggestions_with_fallback(self, playlist_data: Dict) -> Dict:
        """Get AI mood suggestions with intelligent provider selection and fallback"""
        
        # Determine which AI provider to use
        providers_to_try = []
        
        if self.ai_provider == 'openai' and self.openai_available:
            providers_to_try = ['openai']
        elif self.ai_provider == 'gemini' and self.gemini_available:
            providers_to_try = ['gemini']
        elif self.ai_provider == 'auto':
            # Try OpenAI first, then Gemini
            if self.openai_available:
                providers_to_try.append('openai')
            if self.gemini_available:
                providers_to_try.append('gemini')
        
        # Try each provider in order
        for provider in providers_to_try:
            try:
                print(f"🤖 Trying {provider.upper()} for mood analysis...")
                if provider == 'openai':
                    return self.get_ai_mood_suggestions(playlist_data)
                elif provider == 'gemini':
                    return self.get_gemini_mood_suggestions(playlist_data)
            except Exception as e:
                error_str = str(e).lower()
                print(f"❌ {provider.upper()} failed: {str(e)[:100]}...")
                
                # If this was an API issue, try the next provider
                if any(keyword in error_str for keyword in ['quota', 'rate limit', 'authentication', 'invalid_api_key', 'invalid api key', 'api_key']):
                    continue
                else:
                    # For other errors, stop trying
                    break
        
        # If all AI providers failed, use demo fallback
        print("🎭 All AI providers failed, using demo fallback...")
        return self.get_demo_ai_suggestions(playlist_data)
    
    def get_demo_ai_suggestions(self, playlist_data: Dict) -> Dict:
        """Generate demo AI suggestions based on track analysis"""
        tracks = playlist_data.get('tracks', [])
        playlist_name = playlist_data.get('playlist_info', {}).get('name', '').lower()
        
        # Analyze track names and artists for mood hints
        all_text = ' '.join([
            playlist_name,
            ' '.join([track.get('name', '') for track in tracks[:10]]),
            ' '.join([' '.join(track.get('artists', [])) for track in tracks[:10]])
        ]).lower()
        
        # Simple keyword-based mood detection
        mood_scores = {}
        for mood, keywords in {
            'energetic': ['pump', 'energy', 'power', 'rock', 'metal', 'dance', 'electronic'],
            'relaxed': ['chill', 'relax', 'calm', 'peaceful', 'soft', 'acoustic'],
            'happy': ['happy', 'joy', 'fun', 'party', 'celebration', 'upbeat'],
            'melancholic': ['sad', 'blue', 'melancholy', 'sorrow', 'lonely'],
            'ambient': ['ambient', 'atmospheric', 'drone', 'soundscape', 'space'],
            'romantic': ['love', 'romantic', 'tender', 'sweet', 'intimate'],
            'meditative': ['meditation', 'zen', 'spiritual', 'therapy', 'healing'],
            'aggressive': ['aggressive', 'heavy', 'intense', 'brutal', 'hardcore'],
            'nostalgic': ['retro', 'vintage', 'classic', 'old', 'memories'],
            'focus': ['study', 'focus', 'concentration', 'work', 'productivity'],
            'party': ['party', 'club', 'dance', 'festival', 'celebration'],
            'downtempo': ['downtempo', 'slow', 'laid-back', 'lounge']
        }.items():
            score = sum(1 for keyword in keywords if keyword in all_text)
            if score > 0:
                mood_scores[mood] = score
        
        # Generate suggestions based on scores
        sorted_moods = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        suggestions = []
        for i, (mood, score) in enumerate(sorted_moods):
            confidence = min(0.95, 0.6 + (score * 0.1))
            suggestions.append({
                'mood': mood,
                'confidence': confidence,
                'reasoning': f"Analysis of track names and playlist context suggests {mood} characteristics."
            })
        
        # Fallback if no matches
        if not suggestions:
            suggestions = [{
                'mood': 'ambient',
                'confidence': 0.7,
                'reasoning': "Default mood suggestion based on general music analysis patterns."
            }]
        
        return {
            'suggestions': suggestions,
            'overall_assessment': f"Demo analysis of playlist based on track names and context. {len(tracks)} tracks analyzed."
        }
    
    def combine_analysis(self, playlist_data: Dict) -> Dict:
        """Combine rule-based and AI analysis"""
        rule_based = self.analyze_playlist_mood(playlist_data)
        ai_suggestions = self.get_ai_mood_suggestions_with_fallback(playlist_data)
        
        combined_result = {
            'playlist_info': playlist_data['playlist_info'],
            'rule_based_analysis': rule_based,
            'ai_suggestions': ai_suggestions,
            'final_recommendations': []
        }
        
        # Check if we have audio features for rule-based analysis
        has_audio_features = not rule_based.get('error') and rule_based.get('top_moods')
        
        if has_audio_features:
            # Combine scores (60% rule-based, 40% AI)
            mood_scores = {}
            
            for mood, score in rule_based.get('top_moods', []):
                mood_scores[mood] = score * 0.6
            
            for suggestion in ai_suggestions.get('suggestions', []):
                mood = suggestion.get('mood')
                confidence = suggestion.get('confidence', 0.5)
                if mood in mood_scores:
                    mood_scores[mood] += confidence * 0.4
                else:
                    mood_scores[mood] = confidence * 0.4
        else:
            # Use 100% AI analysis when audio features are not available
            mood_scores = {}
            for suggestion in ai_suggestions.get('suggestions', []):
                mood = suggestion.get('mood')
                confidence = suggestion.get('confidence', 0.5)
                mood_scores[mood] = confidence
        
        final_top = sorted(mood_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for mood, score in final_top:
            ai_reasoning = next(
                (s['reasoning'] for s in ai_suggestions.get('suggestions', []) if s.get('mood') == mood),
                'Based on track names and playlist context' if not has_audio_features else 'Based on audio feature analysis'
            )
            
            combined_result['final_recommendations'].append({
                'mood': mood,
                'confidence': score,
                'reasoning': ai_reasoning,
                'keywords': self.mood_categories.get(mood, {}).get('keywords', ['mood-based', 'AI-suggested'])
            })
        
        return combined_result
    
    def get_mood_explanation(self, mood: str) -> Dict:
        """Get detailed explanation of a mood category"""
        if mood not in self.mood_categories:
            return {'error': f'Mood "{mood}" not found'}
        
        config = self.mood_categories[mood]
        return {
            'mood': mood,
            'keywords': config['keywords'],
            'audio_features': config['audio_features'],
            'description': f"Music characterized by {', '.join(config['keywords'][:3])} qualities"
        }
    
    def get_gemini_mood_suggestions(self, playlist_data: Dict) -> Dict:
        """Get AI mood suggestions using Google Gemini"""
        try:
            if not self.gemini_available:
                raise Exception("Gemini API not available")
            
            context = f"""
            Playlist: {playlist_data['playlist_info']['name']}
            Description: {playlist_data['playlist_info'].get('description', 'No description')}
            Total Tracks: {playlist_data['total_tracks']}
            
            Sample tracks:
            """
            
            # Show more tracks if no audio features available
            sample_count = 10 if not any(track.get('audio_features') for track in playlist_data['tracks'][:10]) else 5
            
            for i, track in enumerate(playlist_data['tracks'][:sample_count]):
                context += f"\n{i+1}. {track['name']} by {', '.join(track['artists'])}"
                if track.get('audio_features'):
                    af = track['audio_features']
                    context += f" (Energy: {af.get('energy', 0):.2f}, Valence: {af.get('valence', 0):.2f})"
                
            # Add note about missing audio features if applicable
            if not any(track.get('audio_features') for track in playlist_data['tracks'][:5]):
                context += f"\n\nNote: Audio features not available, analyzing based on track names, artists, and playlist context."
            
            mood_list = list(self.mood_categories.keys())
            context += f"\n\nAvailable moods: {', '.join(mood_list)}"
            
            prompt = f"""
            Based on this playlist, suggest the top 3 most appropriate moods from the available options and explain why.
            
            {context}
            
            Available moods: {', '.join(mood_list)}
            
            Rules:
            - Only suggest moods from the available list
            - Provide confidence between 0.0 and 1.0
            - Give clear reasoning for each suggestion
            
            Respond in JSON format:
            {{
                "suggestions": [
                    {{
                        "mood": "mood_name",
                        "confidence": 0.85,
                        "reasoning": "explanation"
                    }}
                ],
                "overall_assessment": "brief description"
            }}
            """
            
            print(f"🤖 Sending request to Gemini...")
            print(f"📝 Prompt length: {len(prompt)} characters")
            print(f"🔑 API Key present: {bool(Config.GEMINI_API_KEY and Config.GEMINI_API_KEY != 'your_gemini_api_key_here')}")
            
            response = self.gemini_model.generate_content(prompt)
            
            content = response.text
            print(f"✅ Gemini response received: {len(content)} characters")
            print(f"📄 Raw response: {content[:200]}...")
            
            if not content:
                raise ValueError("No content in Gemini response")
            
            # Clean up the response - remove markdown code blocks if present
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
            
            result = json.loads(content)
            print(f"📊 Gemini suggested {len(result.get('suggestions', []))} moods")
            return result
            
        except Exception as e:
            error_str = str(e).lower()
            print(f"❌ Gemini Error: {type(e).__name__}: {str(e)}")
            
            # Re-raise API-related errors so fallback can handle them
            if any(keyword in error_str for keyword in ['quota', 'rate limit', 'authentication', 'invalid_api_key', 'invalid api key', 'api_key']):
                raise e
            
            # For other errors, return error response
            import traceback
            print(f"🔍 Full traceback: {traceback.format_exc()}")
            return {
                "suggestions": [],
                "overall_assessment": "Unable to generate Gemini suggestions",
                "error": str(e)
            }