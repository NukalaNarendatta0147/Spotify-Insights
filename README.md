# 🎵 Spotify Listening Insights

[![Tests](https://img.shields.io/badge/tests-46%20passed-brightgreen)](./TESTING.md)
[![Coverage](https://img.shields.io/badge/coverage-80%25+-brightgreen)](./TESTING.md)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)

A colorful, interactive dashboard to visualize your Spotify listening patterns, favorite artists, genres, and emotional music profile.

## 🚀 Setup Instructions

### 1. Get Spotify API Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Log in with your Spotify account
3. Click **"Create an App"**
4. Fill in:
   - App name: "Listening Insights"
   - App description: "Personal listening analytics"
   - Redirect URI: `http://localhost:8080`
5. Copy your **Client ID** and **Client Secret**

### 2. Install Dependencies

```bash
cd spotify-insights
pip install -r requirements.txt
```

### 3. Configure Environment

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   SPOTIPY_CLIENT_ID=your_client_id_here
   SPOTIPY_CLIENT_SECRET=your_client_secret_here
   SPOTIPY_REDIRECT_URI=http://localhost:8080
   ```

### 4. Run the Dashboard

```bash
streamlit run main.py
```

The dashboard will automatically open in your browser (usually at **http://localhost:8501**)

On first run, you'll be redirected to Spotify to authorize the app. After authorization, you'll see your insights!

## 📊 Features

- **🎵 Top Artists**: Your most played artists with popularity scores
- **🎸 Genre Distribution**: Colorful breakdown of your music genres
- **🎭 Emotional Profile**: Radar chart showing happiness, energy, danceability
- **🔥 Listening Heatmap**: When you listen most (day/hour)
- **⏰ Hourly Activity**: Your listening patterns throughout the day
- **💫 Emotional Landscape**: Scatter plot of song moods

## 🎨 Customization

Edit `visualizer.py` to change colors, chart types, or add new visualizations!

## 🧪 Testing

This project includes comprehensive testing infrastructure. See [TESTING.md](TESTING.md) for detailed information.

### Quick Start

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

### Development Mode (No API Required)

Test the application without Spotify API credentials:
```bash
streamlit run dev_mode.py
```

This uses mock data to simulate the full application experience.

## 📝 Notes

- Data is fetched in real-time from Spotify API
- Limited to last 50 recently played tracks for heatmap
- Top artists/tracks can show short_term (4 weeks), medium_term (6 months), or long_term (years)
- Comprehensive test suite with 80%+ coverage
- Mock data available for development without API access
