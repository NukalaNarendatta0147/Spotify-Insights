import streamlit as st
import sqlite3
import pandas as pd
from visualizer import Visualizer

# Page configuration
st.set_page_config(
    page_title="Spotify Listening Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for WhatsApp-inspired dark theme
st.markdown("""
    <style>
    .main {
        background: #0b141a;
    }
    .stApp {
        background: #0b141a;
    }
    h1 {
        text-align: center;
        color: #00a884;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2em;
        color: #8696a0;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choose a view:",
    [
        "📊 Overview",
        "🎯 Music Personality",
        "💎 Hidden Gems & Binge",
        "🎤 Top Artists & Genres",
        "⏰ Listening Patterns",
        "📈 Emotional Analysis"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("ℹ️ **Tip:** Navigate between different views to explore your music insights!")

# Title and subtitle
st.title("📊 Spotify Listening Insights")
st.markdown('<p class="subtitle">Discover your music personality through data analytics</p>', unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_database_connection():
    """Create database connection"""
    return sqlite3.connect('spotify_data.db', check_same_thread=False)

def load_data_from_db():
    """Load all data from database"""
    conn = get_database_connection()
    
    data = {}
    data['top_artists'] = pd.read_sql_query("SELECT * FROM top_artists ORDER BY rank", conn)
    data['top_tracks'] = pd.read_sql_query("SELECT * FROM top_tracks ORDER BY rank", conn)
    data['genres'] = pd.read_sql_query("SELECT * FROM genres ORDER BY count DESC", conn)
    data['recently_played'] = pd.read_sql_query("SELECT * FROM recently_played ORDER BY played_at DESC", conn)
    data['listening_hours'] = pd.read_sql_query("SELECT * FROM listening_patterns ORDER BY hour", conn)
    data['listening_heatmap'] = pd.read_sql_query("SELECT * FROM listening_heatmap", conn)
    data['personality'] = pd.read_sql_query("SELECT * FROM music_personality ORDER BY id DESC LIMIT 1", conn).to_dict('records')[0]
    data['diversity'] = pd.read_sql_query("SELECT * FROM diversity_score ORDER BY id DESC LIMIT 1", conn).to_dict('records')[0]
    data['hidden_gems'] = pd.read_sql_query("SELECT * FROM hidden_gems", conn)
    data['binge_listening'] = pd.read_sql_query("SELECT * FROM binge_listening ORDER BY plays DESC", conn)
    
    # Check if audio_features has data
    audio_features = pd.read_sql_query("SELECT * FROM audio_features", conn)
    data['audio_features'] = audio_features if len(audio_features) > 0 else pd.DataFrame()
    
    return data

try:
    with st.spinner('📊 Loading data from database...'):
        # Load data
        data = load_data_from_db()
        viz = Visualizer()
    
    # === PAGE ROUTING ===
    if page == "📊 Overview":
        st.markdown("## 📊 Quick Overview")
        
        # Personality and Diversity in one row
        col1, col2 = st.columns(2)
        with col1:
            personality = data['personality']
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(29, 185, 84, 0.3), rgba(30, 215, 96, 0.3)); 
                        padding: 30px; border-radius: 15px; border: 2px solid #1DB954;'>
                <h2 style='text-align: center; color: #1ed760; margin-bottom: 20px;'>{personality['personality']}</h2>
                <p style='text-align: center; font-size: 1.2em; color: white;'>{personality['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.plotly_chart(viz.create_diversity_gauge(data['diversity']), use_container_width=True)
        
        st.markdown("---")
        
        # Quick stats
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(viz.create_top_artists_chart(data['top_artists']), use_container_width=True)
        with col4:
            st.plotly_chart(viz.create_genre_chart(data['genres']), use_container_width=True)
    
    elif page == "🎯 Music Personality":
        st.markdown("## 🎯 Your Music Personality")
        
        personality = data['personality']
        diversity = data['diversity']
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(29, 185, 84, 0.3), rgba(30, 215, 96, 0.3)); 
                        padding: 40px; border-radius: 15px; border: 2px solid #1DB954;'>
                <h1 style='text-align: center; color: #1ed760; margin-bottom: 20px;'>{personality['personality']}</h1>
                <p style='text-align: center; font-size: 1.3em; color: white; margin-bottom: 30px;'>{personality['description']}</p>
                <div style='margin-top: 30px;'>
                    <p style='color: #1ed760; font-size: 1.2em;'>⚡ Energy: {personality['energy']:.0%}</p>
                    <p style='color: #ff6b6b; font-size: 1.2em;'>😊 Happiness: {personality['valence']:.0%}</p>
                    <p style='color: #48dbfb; font-size: 1.2em;'>💃 Danceability: {personality['danceability']:.0%}</p>
                    <p style='color: #f093fb; font-size: 1.2em;'>🎸 Acousticness: {personality['acousticness']:.0%}</p>
                    <p style='color: #feca57; font-size: 1.2em;'>🎵 Tempo: {personality['tempo']:.0f} BPM</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.plotly_chart(viz.create_diversity_gauge(diversity), use_container_width=True)
            st.markdown(f"""
            <div style='text-align: center; color: white; margin-top: 20px; padding: 20px; 
                        background: rgba(0,0,0,0.3); border-radius: 10px;'>
                <h3 style='color: #1ed760;'>Diversity Breakdown</h3>
                <p style='font-size: 1.1em;'>{diversity['message']}</p>
                <p style='color: #1ed760; font-size: 1.1em;'>🎸 {diversity['unique_genres']} unique genres</p>
                <p style='color: #48dbfb; font-size: 1.1em;'>🎤 {diversity['unique_artists']} unique artists</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Show audio features if available
        if len(data['audio_features']) > 0:
            st.markdown("---")
            st.markdown("### 🎵 Audio Features Analysis")
            
            # Create emotional radar from audio features
            avg_features = {
                'Happiness': data['audio_features']['valence'].mean(),
                'Energy': data['audio_features']['energy'].mean(),
                'Danceability': data['audio_features']['danceability'].mean(),
                'Acousticness': data['audio_features']['acousticness'].mean()
            }
            
            col3, col4 = st.columns(2)
            with col3:
                # Create a simple dataframe for radar chart
                emotional_df = pd.DataFrame([avg_features])
                emotional_df.columns = ['valence', 'energy', 'danceability', 'acousticness']
                st.plotly_chart(viz.create_emotional_radar(emotional_df), use_container_width=True)
            
            with col4:
                # Scatter plot
                scatter_df = data['audio_features'][['valence', 'energy', 'danceability', 'track_name', 'artist']].copy()
                scatter_df.columns = ['valence', 'energy', 'danceability', 'name', 'artist']
                st.plotly_chart(viz.create_emotional_scatter(scatter_df), use_container_width=True)
    
    elif page == "💎 Hidden Gems & Binge":
        st.markdown("## 💎 Hidden Gems & Binge Listening")
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(viz.create_hidden_gems_chart(data['hidden_gems']), use_container_width=True)
            if len(data['hidden_gems']) > 0:
                st.markdown("### 📋 All Your Hidden Gems")
                for idx, gem in data['hidden_gems'].iterrows():
                    st.markdown(f"""
                    <div style='background: rgba(29, 185, 84, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: white; font-size: 1.1em; margin: 0;'><b>{gem['name']}</b></p>
                        <p style='color: #1ed760; margin: 5px 0;'>by {gem['artist']}</p>
                        <p style='color: #ff6b6b; margin: 0;'>Popularity: {gem['popularity']}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.plotly_chart(viz.create_binge_chart(data['binge_listening']), use_container_width=True)
            if len(data['binge_listening']) > 0:
                st.markdown("### 📋 Your Most Binged Songs")
                for idx, song in data['binge_listening'].iterrows():
                    st.markdown(f"""
                    <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: white; font-size: 1.1em; margin: 0;'><b>{song['name']}</b></p>
                        <p style='color: #1ed760; margin: 5px 0;'>by {song['artist']}</p>
                        <p style='color: #feca57; margin: 0;'>🔁 Played {song['plays']} times</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif page == "🎤 Top Artists & Genres":
        st.markdown("## 🎤 Your Top Artists & Genres")
        
        st.plotly_chart(viz.create_top_artists_chart(data['top_artists']), use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(viz.create_genre_chart(data['genres']), use_container_width=True)
        
        with col2:
            st.markdown("### 🎸 Top Artists Details")
            for idx, artist in data['top_artists'].head(10).iterrows():
                st.markdown(f"""
                <div style='background: rgba(29, 185, 84, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                    <p style='color: white; font-size: 1.1em; margin: 0;'><b>#{artist['rank']} {artist['name']}</b></p>
                    <p style='color: #1ed760; margin: 5px 0;'>Popularity: {artist['popularity']}/100</p>
                    <p style='color: #48dbfb; margin: 0;'>Genres: {artist['genres']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif page == "⏰ Listening Patterns":
        st.markdown("## ⏰ Your Listening Patterns")
        
        st.plotly_chart(viz.create_listening_heatmap(data['listening_heatmap']), use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(viz.create_listening_hours_chart(data['listening_hours']), use_container_width=True)
        
        with col2:
            # Calculate peak listening time
            peak_hour = data['listening_hours'].loc[data['listening_hours']['plays'].idxmax(), 'hour']
            total_plays = data['listening_hours']['plays'].sum()
            
            st.markdown(f"""
            <div style='background: rgba(29, 185, 84, 0.3); padding: 30px; border-radius: 15px; 
                        border: 2px solid #1DB954; margin-top: 50px;'>
                <h3 style='text-align: center; color: #1ed760;'>📊 Quick Stats</h3>
                <p style='text-align: center; font-size: 1.2em; color: white;'>
                    Peak Hour: <b>{int(peak_hour)}:00</b>
                </p>
                <p style='text-align: center; font-size: 1.2em; color: white;'>
                    Total Plays: <b>{int(total_plays)}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📈 Emotional Analysis":
        st.markdown("## 📈 Emotional Music Analysis")
        
        if len(data['audio_features']) > 0:
            col1, col2 = st.columns(2)
            
            # Prepare data for visualizations
            avg_features = {
                'valence': data['audio_features']['valence'].mean(),
                'energy': data['audio_features']['energy'].mean(),
                'danceability': data['audio_features']['danceability'].mean(),
                'acousticness': data['audio_features']['acousticness'].mean()
            }
            emotional_df = pd.DataFrame([avg_features])
            
            with col1:
                st.plotly_chart(viz.create_emotional_radar(emotional_df), use_container_width=True)
            
            with col2:
                scatter_df = data['audio_features'][['valence', 'energy', 'danceability', 'track_name', 'artist']].copy()
                scatter_df.columns = ['valence', 'energy', 'danceability', 'name', 'artist']
                st.plotly_chart(viz.create_emotional_scatter(scatter_df), use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🎵 Your Top Tracks Emotional Breakdown")
            
            for idx, track in data['audio_features'].head(10).iterrows():
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"""
                    <div style='background: rgba(29, 185, 84, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: white; font-size: 1.1em; margin: 0;'><b>{track['track_name']}</b></p>
                        <p style='color: #1ed760; margin: 5px 0;'>by {track['artist']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                with col_b:
                    st.markdown(f"""
                    <div style='background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: #ff6b6b; margin: 0;'>😊 {track['valence']:.0%}</p>
                        <p style='color: #48dbfb; margin: 0;'>⚡ {track['energy']:.0%}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Audio features data not available in database")
            st.info("💡 Audio features require additional API permissions. The dashboard shows all other available data.")

except FileNotFoundError:
    st.error("❌ Database file not found!")
    st.info("""
    **Please create the database first:**
    
    Run this command in your terminal:
    ```
    python export_to_database.py
    ```
    
    This will create the `spotify_data.db` file with all your Spotify data.
    """)

except Exception as e:
    st.error("❌ Error loading data from database")
    st.error(f"**Error details:** {str(e)}")
    st.info("""
    **Troubleshooting steps:**
    1. Make sure `spotify_data.db` exists in the current directory
    2. Try running `python export_to_database.py` again
    3. Check that the database has data using `python view_database.py`
    """)
    
    with st.expander("Show technical details"):
        import traceback
        st.code(traceback.format_exc())
