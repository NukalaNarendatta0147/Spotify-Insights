"""
Export Spotify Data to SQLite Database
This script fetches your Spotify data and stores it in a SQLite database
"""

import sqlite3
import pandas as pd
from datetime import datetime
from spotify_client import SpotifyClient
from data_processor import DataProcessor
import os

def create_database(db_name="spotify_data.db"):
    """Create SQLite database and return connection"""
    conn = sqlite3.connect(db_name)
    print(f"📊 Database created: {db_name}")
    return conn

def create_tables(conn):
    """Create all necessary tables in the database"""
    cursor = conn.cursor()
    
    # Top Artists Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank INTEGER,
        name TEXT,
        genres TEXT,
        popularity INTEGER,
        followers INTEGER,
        time_range TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Top Tracks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS top_tracks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rank INTEGER,
        name TEXT,
        artist TEXT,
        album TEXT,
        popularity INTEGER,
        duration_ms INTEGER,
        duration_min REAL,
        release_date TEXT,
        spotify_url TEXT,
        time_range TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Genres Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre TEXT,
        count INTEGER,
        time_range TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Recently Played Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recently_played (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        played_at TIMESTAMP,
        track_name TEXT,
        artist TEXT,
        album TEXT,
        duration_min REAL,
        day_of_week TEXT,
        hour INTEGER,
        spotify_url TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Audio Features Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audio_features (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        track_name TEXT,
        artist TEXT,
        popularity INTEGER,
        danceability REAL,
        energy REAL,
        key INTEGER,
        loudness REAL,
        mode INTEGER,
        speechiness REAL,
        acousticness REAL,
        instrumentalness REAL,
        liveness REAL,
        valence REAL,
        tempo REAL,
        duration_min REAL,
        time_signature INTEGER,
        time_range TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Listening Patterns Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listening_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hour INTEGER,
        plays INTEGER,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Listening Heatmap Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS listening_heatmap (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day_num INTEGER,
        day TEXT,
        hour INTEGER,
        plays INTEGER,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Music Personality Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS music_personality (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        personality TEXT,
        description TEXT,
        energy REAL,
        valence REAL,
        danceability REAL,
        acousticness REAL,
        tempo REAL,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Diversity Score Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diversity_score (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER,
        level TEXT,
        message TEXT,
        unique_genres INTEGER,
        unique_artists INTEGER,
        genre_score INTEGER,
        artist_score INTEGER,
        variance_score INTEGER,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Hidden Gems Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS hidden_gems (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        artist TEXT,
        popularity INTEGER,
        album TEXT,
        image TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Binge Listening Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS binge_listening (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        artist TEXT,
        plays INTEGER,
        album TEXT,
        export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    print("✅ All tables created successfully!")

def insert_top_artists(conn, processor, time_range='medium_term'):
    """Insert top artists data"""
    print("📊 Inserting top artists...")
    df = processor.get_top_artists_data(time_range=time_range)
    df['time_range'] = time_range
    df.to_sql('top_artists', conn, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} artists")

def insert_top_tracks(conn, client, time_range='medium_term'):
    """Insert top tracks data"""
    print("📊 Inserting top tracks...")
    tracks = client.get_top_tracks(time_range=time_range)
    
    data = []
    for idx, track in enumerate(tracks['items']):
        data.append({
            'rank': idx + 1,
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'duration_min': round(track['duration_ms'] / 60000, 2),
            'release_date': track['album']['release_date'],
            'spotify_url': track['external_urls']['spotify'],
            'time_range': time_range
        })
    
    df = pd.DataFrame(data)
    df.to_sql('top_tracks', conn, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} tracks")

def insert_genres(conn, processor, time_range='medium_term'):
    """Insert genre distribution"""
    print("📊 Inserting genres...")
    df = processor.get_genre_distribution(time_range=time_range)
    df['time_range'] = time_range
    df.to_sql('genres', conn, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} genres")

def insert_recently_played(conn, client):
    """Insert recently played tracks"""
    print("📊 Inserting recently played...")
    recent = client.get_recently_played(limit=50)
    
    data = []
    for item in recent['items']:
        played_at = datetime.fromisoformat(item['played_at'].replace('Z', '+00:00'))
        data.append({
            'played_at': played_at.strftime('%Y-%m-%d %H:%M:%S'),
            'track_name': item['track']['name'],
            'artist': item['track']['artists'][0]['name'],
            'album': item['track']['album']['name'],
            'duration_min': round(item['track']['duration_ms'] / 60000, 2),
            'day_of_week': played_at.strftime('%A'),
            'hour': played_at.hour,
            'spotify_url': item['track']['external_urls']['spotify']
        })
    
    df = pd.DataFrame(data)
    df.to_sql('recently_played', conn, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} recent plays")

def insert_audio_features(conn, client, time_range='medium_term'):
    """Insert audio features"""
    print("📊 Inserting audio features...")
    tracks = client.get_top_tracks(time_range=time_range)
    track_ids = [track['id'] for track in tracks['items'][:50]]
    features = client.get_audio_features(track_ids)
    
    data = []
    for track, feature in zip(tracks['items'][:50], features):
        if feature:
            data.append({
                'track_name': track['name'],
                'artist': track['artists'][0]['name'],
                'popularity': track['popularity'],
                'danceability': feature['danceability'],
                'energy': feature['energy'],
                'key': feature['key'],
                'loudness': feature['loudness'],
                'mode': feature['mode'],
                'speechiness': feature['speechiness'],
                'acousticness': feature['acousticness'],
                'instrumentalness': feature['instrumentalness'],
                'liveness': feature['liveness'],
                'valence': feature['valence'],
                'tempo': feature['tempo'],
                'duration_min': round(feature['duration_ms'] / 60000, 2),
                'time_signature': feature['time_signature'],
                'time_range': time_range
            })
    
    df = pd.DataFrame(data)
    df.to_sql('audio_features', conn, if_exists='append', index=False)
    print(f"✅ Inserted {len(df)} audio features")

def insert_listening_patterns(conn, processor):
    """Insert listening patterns"""
    print("📊 Inserting listening patterns...")
    
    # Hourly patterns
    hours_df = processor.get_listening_hours_data()
    hours_df.to_sql('listening_patterns', conn, if_exists='append', index=False)
    print(f"✅ Inserted hourly patterns")
    
    # Heatmap data
    heatmap_df = processor.get_listening_heatmap_data()
    heatmap_df.to_sql('listening_heatmap', conn, if_exists='append', index=False)
    print(f"✅ Inserted heatmap data")

def insert_music_personality(conn, processor):
    """Insert music personality"""
    print("📊 Inserting music personality...")
    personality = processor.get_music_personality()
    df = pd.DataFrame([personality])
    df.to_sql('music_personality', conn, if_exists='append', index=False)
    print("✅ Inserted music personality")

def insert_diversity_score(conn, processor):
    """Insert diversity score"""
    print("📊 Inserting diversity score...")
    diversity = processor.get_diversity_score()
    df = pd.DataFrame([diversity])
    df.to_sql('diversity_score', conn, if_exists='append', index=False)
    print("✅ Inserted diversity score")

def insert_hidden_gems(conn, processor):
    """Insert hidden gems"""
    print("📊 Inserting hidden gems...")
    df = processor.get_hidden_gems()
    if len(df) > 0:
        df.to_sql('hidden_gems', conn, if_exists='append', index=False)
        print(f"✅ Inserted {len(df)} hidden gems")
    else:
        print("ℹ️  No hidden gems to insert")

def insert_binge_listening(conn, processor):
    """Insert binge listening"""
    print("📊 Inserting binge listening...")
    df = processor.get_binge_listening()
    if len(df) > 0:
        df.to_sql('binge_listening', conn, if_exists='append', index=False)
        print(f"✅ Inserted {len(df)} binge tracks")
    else:
        print("ℹ️  No binge listening to insert")

def print_database_summary(conn):
    """Print summary of database contents"""
    cursor = conn.cursor()
    
    print("\n" + "=" * 60)
    print("📊 DATABASE SUMMARY")
    print("=" * 60)
    
    tables = [
        'top_artists', 'top_tracks', 'genres', 'recently_played',
        'audio_features', 'listening_patterns', 'listening_heatmap',
        'music_personality', 'diversity_score', 'hidden_gems', 'binge_listening'
    ]
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   • {table}: {count} records")
    
    print("=" * 60)

def main():
    """Main function to export all data to database"""
    print("=" * 60)
    print("🎵 SPOTIFY DATA EXPORT TO SQLITE DATABASE")
    print("=" * 60)
    print()
    
    try:
        # Initialize clients
        print("🔐 Connecting to Spotify...")
        spotify = SpotifyClient()
        processor = DataProcessor(spotify)
        print("✅ Connected successfully!")
        print()
        
        # Create database
        db_name = "spotify_data.db"
        conn = create_database(db_name)
        print()
        
        # Create tables
        create_tables(conn)
        print()
        
        # Insert all data
        insert_top_artists(conn, processor)
        insert_top_tracks(conn, spotify)
        insert_genres(conn, processor)
        insert_recently_played(conn, spotify)
        insert_audio_features(conn, spotify)
        insert_listening_patterns(conn, processor)
        insert_music_personality(conn, processor)
        insert_diversity_score(conn, processor)
        insert_hidden_gems(conn, processor)
        insert_binge_listening(conn, processor)
        
        # Print summary
        print_database_summary(conn)
        
        # Close connection
        conn.close()
        
        print()
        print("=" * 60)
        print("✅ DATABASE EXPORT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📂 Database file: {db_name}")
        print("\n💡 You can now:")
        print("   1. Open the database with any SQLite viewer")
        print("   2. Query the data using SQL")
        print("   3. Share the database file with your faculty")
        print("\n📝 Example SQL queries:")
        print("   SELECT * FROM top_artists;")
        print("   SELECT * FROM audio_features WHERE energy > 0.7;")
        print("   SELECT * FROM recently_played ORDER BY played_at DESC;")
        
    except Exception as e:
        print()
        print("=" * 60)
        print("❌ ERROR OCCURRED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print("\nPlease make sure:")
        print("1. Your .env file is configured correctly")
        print("2. You've authorized the Spotify app")
        print("3. Your internet connection is stable")
        import traceback
        print("\nTechnical details:")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
