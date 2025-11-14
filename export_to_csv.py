"""
Export Spotify Data to CSV Files
This script fetches your Spotify data and exports it to CSV files for analysis
"""

import pandas as pd
from datetime import datetime
from spotify_client import SpotifyClient
from data_processor import DataProcessor
import os

def create_export_folder():
    """Create exports folder if it doesn't exist"""
    export_folder = "spotify_exports"
    if not os.path.exists(export_folder):
        os.makedirs(export_folder)
    return export_folder

def export_top_artists(processor, folder, time_range='medium_term'):
    """Export top artists to CSV"""
    print("📊 Exporting top artists...")
    df = processor.get_top_artists_data(time_range=time_range)
    filename = f"{folder}/top_artists_{time_range}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_top_tracks(client, folder, time_range='medium_term'):
    """Export top tracks to CSV"""
    print("📊 Exporting top tracks...")
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
            'spotify_url': track['external_urls']['spotify']
        })
    
    df = pd.DataFrame(data)
    filename = f"{folder}/top_tracks_{time_range}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_genres(processor, folder, time_range='medium_term'):
    """Export genre distribution to CSV"""
    print("📊 Exporting genre distribution...")
    df = processor.get_genre_distribution(time_range=time_range)
    filename = f"{folder}/genre_distribution_{time_range}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_recently_played(client, folder):
    """Export recently played tracks to CSV"""
    print("📊 Exporting recently played tracks...")
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
    filename = f"{folder}/recently_played.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_audio_features(client, folder, time_range='medium_term'):
    """Export audio features of top tracks to CSV"""
    print("📊 Exporting audio features...")
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
                'time_signature': feature['time_signature']
            })
    
    df = pd.DataFrame(data)
    filename = f"{folder}/audio_features_{time_range}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_listening_patterns(processor, folder):
    """Export listening patterns to CSV"""
    print("📊 Exporting listening patterns...")
    
    # Hourly patterns
    hours_df = processor.get_listening_hours_data()
    filename = f"{folder}/listening_by_hour.csv"
    hours_df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    
    # Heatmap data
    heatmap_df = processor.get_listening_heatmap_data()
    filename = f"{folder}/listening_heatmap.csv"
    heatmap_df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    
    return hours_df, heatmap_df

def export_music_personality(processor, folder):
    """Export music personality analysis to CSV"""
    print("📊 Exporting music personality...")
    personality = processor.get_music_personality()
    
    df = pd.DataFrame([personality])
    filename = f"{folder}/music_personality.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_diversity_score(processor, folder):
    """Export diversity score to CSV"""
    print("📊 Exporting diversity score...")
    diversity = processor.get_diversity_score()
    
    df = pd.DataFrame([diversity])
    filename = f"{folder}/diversity_score.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    return df

def export_hidden_gems(processor, folder):
    """Export hidden gems to CSV"""
    print("📊 Exporting hidden gems...")
    df = processor.get_hidden_gems()
    
    if len(df) > 0:
        filename = f"{folder}/hidden_gems.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved: {filename}")
    else:
        print("ℹ️  No hidden gems found")
    return df

def export_binge_listening(processor, folder):
    """Export binge listening data to CSV"""
    print("📊 Exporting binge listening...")
    df = processor.get_binge_listening()
    
    if len(df) > 0:
        filename = f"{folder}/binge_listening.csv"
        df.to_csv(filename, index=False)
        print(f"✅ Saved: {filename}")
    else:
        print("ℹ️  No binge listening detected")
    return df

def create_summary_report(folder, all_data):
    """Create a summary report with key statistics"""
    print("📊 Creating summary report...")
    
    summary = {
        'export_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_top_artists': len(all_data['top_artists']),
        'total_top_tracks': len(all_data['top_tracks']),
        'total_genres': len(all_data['genres']),
        'total_recent_plays': len(all_data['recently_played']),
        'music_personality': all_data['personality']['personality'],
        'diversity_score': all_data['diversity']['score'],
        'diversity_level': all_data['diversity']['level'],
        'unique_genres': all_data['diversity']['unique_genres'],
        'unique_artists': all_data['diversity']['unique_artists'],
        'hidden_gems_count': len(all_data['hidden_gems']),
        'binge_tracks_count': len(all_data['binge_listening'])
    }
    
    df = pd.DataFrame([summary])
    filename = f"{folder}/summary_report.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Saved: {filename}")
    
    return df

def main():
    """Main function to export all Spotify data"""
    print("=" * 60)
    print("🎵 SPOTIFY DATA EXPORT TO CSV")
    print("=" * 60)
    print()
    
    try:
        # Initialize clients
        print("🔐 Connecting to Spotify...")
        spotify = SpotifyClient()
        processor = DataProcessor(spotify)
        print("✅ Connected successfully!")
        print()
        
        # Create export folder
        folder = create_export_folder()
        print(f"📁 Export folder: {folder}/")
        print()
        
        # Store all data for summary
        all_data = {}
        
        # Export all data
        all_data['top_artists'] = export_top_artists(processor, folder)
        all_data['top_tracks'] = export_top_tracks(spotify, folder)
        all_data['genres'] = export_genres(processor, folder)
        all_data['recently_played'] = export_recently_played(spotify, folder)
        all_data['audio_features'] = export_audio_features(spotify, folder)
        
        hours_df, heatmap_df = export_listening_patterns(processor, folder)
        all_data['listening_hours'] = hours_df
        all_data['listening_heatmap'] = heatmap_df
        
        all_data['personality'] = processor.get_music_personality()
        export_music_personality(processor, folder)
        
        all_data['diversity'] = processor.get_diversity_score()
        export_diversity_score(processor, folder)
        
        all_data['hidden_gems'] = export_hidden_gems(processor, folder)
        all_data['binge_listening'] = export_binge_listening(processor, folder)
        
        # Create summary report
        print()
        create_summary_report(folder, all_data)
        
        print()
        print("=" * 60)
        print("✅ EXPORT COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📂 All files saved in: {folder}/")
        print("\n📊 Exported files:")
        print("   • top_artists_medium_term.csv")
        print("   • top_tracks_medium_term.csv")
        print("   • genre_distribution_medium_term.csv")
        print("   • recently_played.csv")
        print("   • audio_features_medium_term.csv")
        print("   • listening_by_hour.csv")
        print("   • listening_heatmap.csv")
        print("   • music_personality.csv")
        print("   • diversity_score.csv")
        print("   • hidden_gems.csv (if available)")
        print("   • binge_listening.csv (if available)")
        print("   • summary_report.csv")
        print("\n💡 You can now share these CSV files with your faculty!")
        
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
