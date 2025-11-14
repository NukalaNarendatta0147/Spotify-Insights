import pandas as pd
from datetime import datetime
from collections import Counter

class DataProcessor:
    def __init__(self, spotify_client):
        self.client = spotify_client
    
    def get_top_artists_data(self, time_range='medium_term'):
        """Process top artists data"""
        artists = self.client.get_top_artists(time_range=time_range)
        data = []
        for idx, artist in enumerate(artists['items']):
            data.append({
                'rank': idx + 1,
                'name': artist['name'],
                'genres': ', '.join(artist['genres'][:3]),
                'popularity': artist['popularity'],
                'followers': artist['followers']['total']
            })
        return pd.DataFrame(data)
    
    def get_listening_hours_data(self):
        """Get listening patterns by hour"""
        recent = self.client.get_recently_played(limit=50)
        hours = []
        for item in recent['items']:
            played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
            hours.append(played_at.hour)
        
        hour_counts = Counter(hours)
        return pd.DataFrame([
            {'hour': h, 'plays': hour_counts.get(h, 0)} 
            for h in range(24)
        ])
    
    def get_genre_distribution(self, time_range='medium_term'):
        """Get genre distribution from top artists"""
        artists = self.client.get_top_artists(time_range=time_range)
        all_genres = []
        for artist in artists['items']:
            all_genres.extend(artist['genres'])
        
        genre_counts = Counter(all_genres)
        return pd.DataFrame([
            {'genre': genre, 'count': count}
            for genre, count in genre_counts.most_common(15)
        ])
    
    def get_emotional_patterns(self, time_range='medium_term'):
        """Analyze emotional patterns from audio features"""
        try:
            tracks = self.client.get_top_tracks(time_range=time_range)
            track_ids = [track['id'] for track in tracks['items'][:20]]  # Limit to 20 tracks
            features = self.client.get_audio_features(track_ids)
            
            data = []
            for track, feature in zip(tracks['items'], features):
                if feature:
                    data.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'valence': feature['valence'],  # Happiness
                        'energy': feature['energy'],
                        'danceability': feature['danceability'],
                        'acousticness': feature['acousticness'],
                        'tempo': feature['tempo']
                    })
            
            if not data:
                # Return dummy data if no features available
                return pd.DataFrame([{
                    'name': 'No data',
                    'artist': 'N/A',
                    'valence': 0.5,
                    'energy': 0.5,
                    'danceability': 0.5,
                    'acousticness': 0.5,
                    'tempo': 120
                }])
            return pd.DataFrame(data)
        except Exception as e:
            print(f"Error getting emotional patterns: {e}")
            # Return dummy data on error
            return pd.DataFrame([{
                'name': 'No data',
                'artist': 'N/A',
                'valence': 0.5,
                'energy': 0.5,
                'danceability': 0.5,
                'acousticness': 0.5,
                'tempo': 120
            }])
    
    def get_listening_heatmap_data(self):
        """Get data for day/hour heatmap"""
        recent = self.client.get_recently_played(limit=50)
        data = []
        
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for item in recent['items']:
            played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
            data.append({
                'day': days[played_at.weekday()],
                'hour': played_at.hour,
                'day_num': played_at.weekday()
            })
        
        df = pd.DataFrame(data)
        heatmap_data = df.groupby(['day_num', 'day', 'hour']).size().reset_index(name='plays')
        return heatmap_data

    def get_music_personality(self, time_range='medium_term'):
        """Determine music personality type based on audio features"""
        try:
            tracks = self.client.get_top_tracks(time_range=time_range)
            track_ids = [track['id'] for track in tracks['items'][:50]]
            features = self.client.get_audio_features(track_ids)
            
            # Calculate averages
            avg_energy = sum(f['energy'] for f in features if f) / len(features)
            avg_valence = sum(f['valence'] for f in features if f) / len(features)
            avg_danceability = sum(f['danceability'] for f in features if f) / len(features)
            avg_acousticness = sum(f['acousticness'] for f in features if f) / len(features)
            avg_tempo = sum(f['tempo'] for f in features if f) / len(features)
            
            # Determine personality type
            if avg_energy > 0.7 and avg_danceability > 0.7:
                personality = "🎉 Party Animal"
                description = "You love high-energy, danceable tracks that get you moving!"
            elif avg_valence < 0.4 and avg_energy < 0.5:
                personality = "😢 Melancholic Soul"
                description = "You vibe with emotional, introspective music that hits deep."
            elif avg_acousticness > 0.6:
                personality = "🎸 Acoustic Lover"
                description = "You prefer organic, unplugged sounds and intimate performances."
            elif avg_energy > 0.7 and avg_tempo > 130:
                personality = "💪 Workout Warrior"
                description = "Your playlist is a gym session waiting to happen!"
            elif avg_valence > 0.7 and avg_energy > 0.6:
                personality = "☀️ Happy Vibes"
                description = "You're all about feel-good, uplifting music that brightens the day."
            elif avg_danceability > 0.7:
                personality = "🕺 Dance Floor King/Queen"
                description = "If it makes you move, it's on your playlist!"
            else:
                personality = "🎭 Eclectic Explorer"
                description = "Your taste is diverse and you love discovering new sounds."
            
            return {
                'personality': personality,
                'description': description,
                'energy': avg_energy,
                'valence': avg_valence,
                'danceability': avg_danceability,
                'acousticness': avg_acousticness,
                'tempo': avg_tempo
            }
        except Exception as e:
            print(f"Error getting personality: {e}")
            return {
                'personality': "🎵 Music Lover",
                'description': "You have great taste in music!",
                'energy': 0.5,
                'valence': 0.5,
                'danceability': 0.5,
                'acousticness': 0.5,
                'tempo': 120
            }
    
    def get_hidden_gems(self, time_range='medium_term'):
        """Find hidden gems - songs you love but aren't popular"""
        try:
            tracks = self.client.get_top_tracks(time_range=time_range)
            gems = []
            
            for track in tracks['items']:
                popularity = track['popularity']
                # Hidden gems are tracks with low popularity that you still love
                if popularity < 50:
                    gems.append({
                        'name': track['name'],
                        'artist': track['artists'][0]['name'],
                        'popularity': popularity,
                        'album': track['album']['name'],
                        'image': track['album']['images'][0]['url'] if track['album']['images'] else None
                    })
            
            return pd.DataFrame(gems[:10])  # Top 10 hidden gems
        except Exception as e:
            print(f"Error finding hidden gems: {e}")
            return pd.DataFrame()
    
    def get_binge_listening(self):
        """Detect songs played on repeat"""
        try:
            recent = self.client.get_recently_played(limit=50)
            track_counts = Counter()
            track_info = {}
            
            for item in recent['items']:
                track_id = item['track']['id']
                track_counts[track_id] += 1
                if track_id not in track_info:
                    track_info[track_id] = {
                        'name': item['track']['name'],
                        'artist': item['track']['artists'][0]['name'],
                        'album': item['track']['album']['name']
                    }
            
            # Find tracks played more than once
            binge_tracks = []
            for track_id, count in track_counts.most_common(10):
                if count > 1:
                    info = track_info[track_id]
                    binge_tracks.append({
                        'name': info['name'],
                        'artist': info['artist'],
                        'plays': count,
                        'album': info['album']
                    })
            
            return pd.DataFrame(binge_tracks)
        except Exception as e:
            print(f"Error detecting binge listening: {e}")
            return pd.DataFrame()
    
    def get_diversity_score(self, time_range='medium_term'):
        """Calculate music diversity score (0-100)"""
        try:
            # Get top artists and tracks
            artists = self.client.get_top_artists(time_range=time_range)
            tracks = self.client.get_top_tracks(time_range=time_range)
            
            # Count unique genres
            all_genres = []
            for artist in artists['items']:
                all_genres.extend(artist['genres'])
            unique_genres = len(set(all_genres))
            
            # Count unique artists
            unique_artists = len(artists['items'])
            
            # Get audio feature variance
            track_ids = [track['id'] for track in tracks['items'][:50]]
            features = self.client.get_audio_features(track_ids)
            
            # Calculate variance in audio features
            energy_vals = [f['energy'] for f in features if f]
            valence_vals = [f['valence'] for f in features if f]
            tempo_vals = [f['tempo'] for f in features if f]
            
            import statistics
            energy_var = statistics.variance(energy_vals) if len(energy_vals) > 1 else 0
            valence_var = statistics.variance(valence_vals) if len(valence_vals) > 1 else 0
            tempo_var = statistics.variance(tempo_vals) if len(tempo_vals) > 1 else 0
            
            # Calculate diversity score (0-100)
            genre_score = min(unique_genres * 2, 40)  # Max 40 points
            artist_score = min(unique_artists, 30)  # Max 30 points
            variance_score = min((energy_var + valence_var + tempo_var/1000) * 30, 30)  # Max 30 points
            
            total_score = int(genre_score + artist_score + variance_score)
            
            # Determine diversity level
            if total_score >= 80:
                level = "🌈 Extremely Diverse"
                message = "You're a true music explorer with incredibly varied taste!"
            elif total_score >= 60:
                level = "🎨 Very Diverse"
                message = "You love exploring different genres and artists!"
            elif total_score >= 40:
                level = "🎵 Moderately Diverse"
                message = "You have a balanced mix of favorites and new discoveries."
            else:
                level = "🎯 Focused Taste"
                message = "You know what you like and stick to it!"
            
            return {
                'score': total_score,
                'level': level,
                'message': message,
                'unique_genres': unique_genres,
                'unique_artists': unique_artists,
                'genre_score': int(genre_score),
                'artist_score': int(artist_score),
                'variance_score': int(variance_score)
            }
        except Exception as e:
            print(f"Error calculating diversity: {e}")
            return {
                'score': 50,
                'level': "🎵 Music Lover",
                'message': "You have great taste!",
                'unique_genres': 0,
                'unique_artists': 0,
                'genre_score': 0,
                'artist_score': 0,
                'variance_score': 0
            }
