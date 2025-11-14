import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

class SpotifyClient:
    def __init__(self):
        self.scope = "user-read-recently-played user-top-read user-library-read"
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv('SPOTIPY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
            redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
            scope=self.scope
        ))
    
    def get_top_artists(self, time_range='medium_term', limit=50):
        """Get user's top artists. time_range: short_term, medium_term, long_term"""
        return self.sp.current_user_top_artists(time_range=time_range, limit=limit)
    
    def get_top_tracks(self, time_range='medium_term', limit=50):
        """Get user's top tracks"""
        return self.sp.current_user_top_tracks(time_range=time_range, limit=limit)
    
    def get_recently_played(self, limit=50):
        """Get recently played tracks"""
        return self.sp.current_user_recently_played(limit=limit)
    
    def get_audio_features(self, track_ids):
        """Get audio features for tracks (energy, valence, danceability, etc.)"""
        # Split into smaller batches to avoid rate limits
        batch_size = 20
        all_features = []
        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            try:
                features = self.sp.audio_features(batch)
                all_features.extend(features)
            except Exception as e:
                print(f"Warning: Could not fetch audio features: {e}")
                all_features.extend([None] * len(batch))
        return all_features
    
    def get_artist_genres(self, artist_id):
        """Get genres for an artist"""
        artist = self.sp.artist(artist_id)
        return artist.get('genres', [])
