import streamlit as st
from spotify_client import SpotifyClient
from data_processor import DataProcessor
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

# Initialize session state for caching
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False

try:
    with st.spinner('🎵 Loading your Spotify data...'):
        # Initialize clients
        spotify = SpotifyClient()
        processor = DataProcessor(spotify)
        viz = Visualizer()
        
        # Get all data
        top_artists_df = processor.get_top_artists_data()
        genre_df = processor.get_genre_distribution()
        listening_hours_df = processor.get_listening_hours_data()
        heatmap_df = processor.get_listening_heatmap_data()
        emotional_df = processor.get_emotional_patterns()
        
        # Get new smart features
        personality = processor.get_music_personality()
        diversity = processor.get_diversity_score()
        hidden_gems_df = processor.get_hidden_gems()
        binge_df = processor.get_binge_listening()
        
        st.session_state.data_loaded = True
    
    # === PAGE ROUTING ===
    if page == "📊 Overview":
        st.markdown("## �  Quick Overview")
        
        # Personality and Diversity in one row
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, rgba(29, 185, 84, 0.3), rgba(30, 215, 96, 0.3)); 
                        padding: 30px; border-radius: 15px; border: 2px solid #1DB954;'>
                <h2 style='text-align: center; color: #1ed760; margin-bottom: 20px;'>{personality['personality']}</h2>
                <p style='text-align: center; font-size: 1.2em; color: white;'>{personality['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.plotly_chart(viz.create_diversity_gauge(diversity), use_container_width=True)
        
        st.markdown("---")
        
        # Quick stats
        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(viz.create_top_artists_chart(top_artists_df), use_container_width=True)
        with col4:
            st.plotly_chart(viz.create_genre_chart(genre_df), use_container_width=True)
    
    elif page == "🎯 Music Personality":
        st.markdown("## 🎯 Your Music Personality")
        
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
        
        if len(emotional_df) > 0 and 'valence' in emotional_df.columns:
            st.markdown("---")
            col3, col4 = st.columns(2)
            with col3:
                st.plotly_chart(viz.create_emotional_radar(emotional_df), use_container_width=True)
            with col4:
                st.plotly_chart(viz.create_emotional_scatter(emotional_df), use_container_width=True)
    
    elif page == "💎 Hidden Gems & Binge":
        st.markdown("## 💎 Hidden Gems & Binge Listening")
        
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(viz.create_hidden_gems_chart(hidden_gems_df), use_container_width=True)
            if len(hidden_gems_df) > 0:
                st.markdown("### 📋 All Your Hidden Gems")
                for idx, gem in hidden_gems_df.iterrows():
                    st.markdown(f"""
                    <div style='background: rgba(29, 185, 84, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: white; font-size: 1.1em; margin: 0;'><b>{gem['name']}</b></p>
                        <p style='color: #1ed760; margin: 5px 0;'>by {gem['artist']}</p>
                        <p style='color: #ff6b6b; margin: 0;'>Popularity: {gem['popularity']}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.plotly_chart(viz.create_binge_chart(binge_df), use_container_width=True)
            if len(binge_df) > 0:
                st.markdown("### 📋 Your Most Binged Songs")
                for idx, song in binge_df.iterrows():
                    st.markdown(f"""
                    <div style='background: rgba(255, 107, 107, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: white; font-size: 1.1em; margin: 0;'><b>{song['name']}</b></p>
                        <p style='color: #1ed760; margin: 5px 0;'>by {song['artist']}</p>
                        <p style='color: #feca57; margin: 0;'>🔁 Played {song['plays']} times</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    elif page == "🎤 Top Artists & Genres":
        st.markdown("## 🎤 Your Top Artists & Genres")
        
        st.plotly_chart(viz.create_top_artists_chart(top_artists_df), use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.plotly_chart(viz.create_genre_chart(genre_df), use_container_width=True)
        
        with col2:
            st.markdown("### 🎸 Top Artists Details")
            for idx, artist in top_artists_df.head(10).iterrows():
                st.markdown(f"""
                <div style='background: rgba(29, 185, 84, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                    <p style='color: white; font-size: 1.1em; margin: 0;'><b>#{artist['rank']} {artist['name']}</b></p>
                    <p style='color: #1ed760; margin: 5px 0;'>Popularity: {artist['popularity']}/100</p>
                    <p style='color: #48dbfb; margin: 0;'>Genres: {artist['genres']}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif page == "⏰ Listening Patterns":
        st.markdown("## ⏰ Your Listening Patterns")
        
        st.plotly_chart(viz.create_listening_heatmap(heatmap_df), use_container_width=True)
        
        st.markdown("---")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.plotly_chart(viz.create_listening_hours_chart(listening_hours_df), use_container_width=True)
        
        with col2:
            # Calculate peak listening time
            peak_hour = listening_hours_df.loc[listening_hours_df['plays'].idxmax(), 'hour']
            total_plays = listening_hours_df['plays'].sum()
            
            st.markdown(f"""
            <div style='background: rgba(29, 185, 84, 0.3); padding: 30px; border-radius: 15px; 
                        border: 2px solid #1DB954; margin-top: 50px;'>
                <h3 style='text-align: center; color: #1ed760;'>📊 Quick Stats</h3>
                <p style='text-align: center; font-size: 1.2em; color: white;'>
                    Peak Hour: <b>{peak_hour}:00</b>
                </p>
                <p style='text-align: center; font-size: 1.2em; color: white;'>
                    Total Plays: <b>{total_plays}</b>
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    elif page == "📈 Emotional Analysis":
        st.markdown("## 📈 Emotional Music Analysis")
        
        if len(emotional_df) > 0 and 'valence' in emotional_df.columns:
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(viz.create_emotional_radar(emotional_df), use_container_width=True)
            with col2:
                st.plotly_chart(viz.create_emotional_scatter(emotional_df), use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 🎵 Your Top Tracks Emotional Breakdown")
            
            for idx, track in emotional_df.head(10).iterrows():
                col_a, col_b = st.columns([2, 1])
                with col_a:
                    st.markdown(f"""
                    <div style='background: rgba(29, 185, 84, 0.2); padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <p style='color: white; font-size: 1.1em; margin: 0;'><b>{track['name']}</b></p>
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
            st.warning("⚠️ Emotional data not available for your tracks")

except Exception as e:
    st.error("❌ Error loading Spotify data")
    st.error(f"**Error details:** {str(e)}")
    st.info("""
    **Troubleshooting steps:**
    1. Make sure you've set up your `.env` file with Spotify credentials
    2. Ensure you've authorized the app with Spotify
    3. Check that your Spotify API credentials are valid
    4. Try restarting the Streamlit app
    """)
    
    with st.expander("Show technical details"):
        import traceback
        st.code(traceback.format_exc())
