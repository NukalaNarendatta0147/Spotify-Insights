"""
Development mode script for testing without Spotify API access
Uses mock data to simulate the full application experience
"""
import streamlit as st
from tests.mock_data import MockSpotifyClient
from data_processor import DataProcessor
from visualizer import Visualizer


def main():
    st.set_page_config(
        page_title="Spotify Insights - Dev Mode",
        page_icon="🎵",
        layout="wide"
    )
    
    # Dev mode banner
    st.warning("⚠️ DEVELOPMENT MODE - Using Mock Data (No Spotify API Required)")
    
    st.title("🎵 Your Spotify Insights - Dev Mode")
    st.markdown("---")
    
    # Initialize with mock client
    try:
        client = MockSpotifyClient()
        processor = DataProcessor(client)
        visualizer = Visualizer()
        
        st.success("✅ Mock data loaded successfully!")
        
        # Sidebar
        st.sidebar.title("⚙️ Settings")
        time_range_map = {
            "Last 4 Weeks": "short_term",
            "Last 6 Months": "medium_term",
            "All Time": "long_term"
        }
        time_range_display = st.sidebar.selectbox(
            "Time Range",
            list(time_range_map.keys()),
            index=1
        )
        time_range = time_range_map[time_range_display]
        
        # Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🎤 Top Artists",
            "🎧 Listening Patterns",
            "🎭 Music Personality",
            "💎 Hidden Gems",
            "📊 Diversity Score"
        ])
        
        # Tab 1: Top Artists
        with tab1:
            st.header("Your Top Artists")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                df_artists = processor.get_top_artists_data(time_range)
                fig_artists = visualizer.create_top_artists_chart(df_artists)
                st.plotly_chart(fig_artists, use_container_width=True)
            
            with col2:
                st.subheader("📊 Artist Stats")
                st.dataframe(df_artists[['name', 'popularity', 'genres']].head(10), 
                           use_container_width=True, hide_index=True)
            
            # Genre Distribution
            st.subheader("🎸 Genre Distribution")
            df_genres = processor.get_genre_distribution(time_range)
            fig_genres = visualizer.create_genre_chart(df_genres)
            st.plotly_chart(fig_genres, use_container_width=True)
        
        # Tab 2: Listening Patterns
        with tab2:
            st.header("Your Listening Patterns")
            
            # Listening Hours
            df_hours = processor.get_listening_hours_data()
            fig_hours = visualizer.create_listening_hours_chart(df_hours)
            st.plotly_chart(fig_hours, use_container_width=True)
            
            # Listening Heatmap
            st.subheader("🔥 When You Listen Most")
            df_heatmap = processor.get_listening_heatmap_data()
            fig_heatmap = visualizer.create_listening_heatmap(df_heatmap)
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Binge Listening
            st.subheader("🔁 Songs You Binged")
            df_binge = processor.get_binge_listening()
            if len(df_binge) > 0:
                fig_binge = visualizer.create_binge_chart(df_binge)
                st.plotly_chart(fig_binge, use_container_width=True)
            else:
                st.info("No repeat plays detected in recent history!")
        
        # Tab 3: Music Personality
        with tab3:
            st.header("Your Music Personality")
            
            personality = processor.get_music_personality(time_range)
            
            # Display personality
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"## {personality['personality']}")
                st.markdown(f"### {personality['description']}")
                
                st.markdown("---")
                st.metric("Energy", f"{personality['energy']:.2f}")
                st.metric("Happiness", f"{personality['valence']:.2f}")
                st.metric("Danceability", f"{personality['danceability']:.2f}")
            
            with col2:
                # Emotional patterns
                df_emotional = processor.get_emotional_patterns(time_range)
                fig_radar = visualizer.create_emotional_radar(df_emotional)
                st.plotly_chart(fig_radar, use_container_width=True)
            
            # Emotional scatter
            st.subheader("💫 Song Emotional Landscape")
            fig_scatter = visualizer.create_emotional_scatter(df_emotional)
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Tab 4: Hidden Gems
        with tab4:
            st.header("Your Hidden Gems")
            st.markdown("Songs you love that aren't mainstream hits")
            
            df_gems = processor.get_hidden_gems(time_range)
            
            if len(df_gems) > 0:
                fig_gems = visualizer.create_hidden_gems_chart(df_gems)
                st.plotly_chart(fig_gems, use_container_width=True)
                
                st.subheader("💎 Gem Details")
                st.dataframe(df_gems[['name', 'artist', 'popularity', 'album']], 
                           use_container_width=True, hide_index=True)
            else:
                st.info("All your favorites are popular hits! 🌟")
        
        # Tab 5: Diversity Score
        with tab5:
            st.header("Your Music Diversity Score")
            
            diversity = processor.get_diversity_score(time_range)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                fig_gauge = visualizer.create_diversity_gauge(diversity)
                st.plotly_chart(fig_gauge, use_container_width=True)
            
            with col2:
                st.markdown(f"## {diversity['level']}")
                st.markdown(f"### {diversity['message']}")
                
                st.markdown("---")
                st.metric("Unique Genres", diversity['unique_genres'])
                st.metric("Unique Artists", diversity['unique_artists'])
                
                st.markdown("#### Score Breakdown")
                st.progress(diversity['genre_score'] / 40, text=f"Genre Diversity: {diversity['genre_score']}/40")
                st.progress(diversity['artist_score'] / 30, text=f"Artist Diversity: {diversity['artist_score']}/30")
                st.progress(diversity['variance_score'] / 30, text=f"Feature Variance: {diversity['variance_score']}/30")
        
        # Footer
        st.markdown("---")
        st.info("💡 This is development mode using mock data. Connect to Spotify API for real insights!")
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()
