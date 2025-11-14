import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

class Visualizer:
    def __init__(self):
        self.colors = px.colors.qualitative.Vivid
    
    def create_top_artists_chart(self, df):
        """Create colorful bar chart for top artists"""
        colors = ['#1DB954', '#1ed760', '#ff6b6b', '#4ecdc4', '#45b7d1', 
                  '#f093fb', '#f5576c', '#feca57', '#48dbfb', '#ff9ff3']
        
        fig = go.Figure(data=[
            go.Bar(
                x=df['name'][:10],
                y=df['popularity'],
                marker=dict(
                    color=colors[:len(df[:10])],
                    line=dict(width=0)
                ),
                text=df['popularity'][:10],
                textposition='auto',
                textfont=dict(size=14, color='white', family='Arial Black')
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🎵 Your Top 10 Artists',
                'font': {'size': 28, 'color': '#1DB954', 'family': 'Arial Black'}
            },
            xaxis_title='Artist',
            yaxis_title='Popularity Score',
            template='plotly_dark',
            height=550,
            font=dict(size=14),
            plot_bgcolor='rgba(0,0,0,0.3)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    def create_listening_hours_chart(self, df):
        """Create area chart for listening hours"""
        fig = go.Figure(data=[
            go.Scatter(
                x=df['hour'],
                y=df['plays'],
                mode='lines+markers',
                fill='tozeroy',
                line=dict(color='#1DB954', width=4),
                marker=dict(size=12, color='#1ed760', line=dict(width=0)),
                fillcolor='rgba(29, 185, 84, 0.3)'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '⏰ Listening Activity by Hour',
                'font': {'size': 24, 'color': '#1ed760', 'family': 'Arial Black'}
            },
            xaxis_title='Hour of Day',
            yaxis_title='Number of Plays',
            template='plotly_dark',
            height=500,
            plot_bgcolor='rgba(0,0,0,0.3)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig

    def create_genre_chart(self, df):
        """Create colorful pie chart for genres"""
        colors = ['#1DB954', '#1ed760', '#ff6b6b', '#4ecdc4', '#45b7d1', 
                  '#f093fb', '#f5576c', '#feca57', '#48dbfb', '#ff9ff3',
                  '#a29bfe', '#fd79a8', '#fdcb6e', '#6c5ce7', '#00b894']
        
        fig = go.Figure(data=[
            go.Pie(
                labels=df['genre'],
                values=df['count'],
                hole=0.45,
                marker=dict(
                    colors=colors[:len(df)],
                    line=dict(width=0)
                ),
                textinfo='percent',
                textposition='inside',
                textfont=dict(size=12, color='white', family='Arial Black'),
                hovertemplate='<b>%{label}</b><br>%{percent}<br><extra></extra>',
                pull=[0.02] * len(df)
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🎸 Your Genre Distribution',
                'font': {'size': 24, 'color': '#ff6b6b', 'family': 'Arial Black'}
            },
            template='plotly_dark',
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=11, color='white')
            )
        )
        return fig
    
    def create_emotional_radar(self, df):
        """Create radar chart for emotional patterns"""
        avg_features = {
            'Happiness': df['valence'].mean(),
            'Energy': df['energy'].mean(),
            'Danceability': df['danceability'].mean(),
            'Acousticness': df['acousticness'].mean()
        }
        
        categories = list(avg_features.keys())
        values = list(avg_features.values())
        
        fig = go.Figure(data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                line=dict(color='#1ed760', width=4),
                marker=dict(size=15, color='#ff6b6b', line=dict(width=0)),
                fillcolor='rgba(29, 185, 84, 0.4)'
            )
        ])
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, 
                    range=[0, 1],
                    gridcolor='rgba(255,255,255,0.2)'
                ),
                bgcolor='rgba(0,0,0,0.3)',
                angularaxis=dict(gridcolor='rgba(255,255,255,0.2)')
            ),
            title={
                'text': '🎭 Your Music Emotional Profile',
                'font': {'size': 24, 'color': '#4ecdc4', 'family': 'Arial Black'}
            },
            template='plotly_dark',
            height=500,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    def create_listening_heatmap(self, df):
        """Create heatmap for listening patterns"""
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Create pivot table
        pivot = df.pivot_table(values='plays', index='day', columns='hour', fill_value=0)
        pivot = pivot.reindex(days)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=list(range(24)),
            y=days,
            colorscale=[[0, '#191414'], [0.5, '#1DB954'], [1, '#1ed760']],
            text=pivot.values,
            texttemplate='%{text}',
            textfont={"size": 12, "color": "white"},
            colorbar=dict(title=dict(text="Plays", font=dict(size=14)))
        ))
        
        fig.update_layout(
            title={
                'text': '🔥 Listening Heatmap: When You Listen Most',
                'font': {'size': 28, 'color': '#feca57', 'family': 'Arial Black'}
            },
            xaxis_title='Hour of Day',
            yaxis_title='Day of Week',
            template='plotly_dark',
            height=450,
            plot_bgcolor='rgba(0,0,0,0.3)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=13)
        )
        return fig
    
    def create_emotional_scatter(self, df):
        """Create scatter plot for valence vs energy"""
        fig = px.scatter(
            df,
            x='valence',
            y='energy',
            size='danceability',
            color='energy',
            hover_data=['name', 'artist'],
            color_continuous_scale=[[0, '#191414'], [0.3, '#1DB954'], [0.6, '#1ed760'], [1, '#feca57']],
            title='💫 Song Emotional Landscape'
        )
        
        fig.update_layout(
            title={
                'text': '💫 Song Emotional Landscape',
                'font': {'size': 24, 'color': '#48dbfb', 'family': 'Arial Black'}
            },
            xaxis_title='Happiness (Valence)',
            yaxis_title='Energy',
            template='plotly_dark',
            height=500,
            plot_bgcolor='rgba(0,0,0,0.3)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(marker=dict(line=dict(width=0)))
        return fig

    def create_diversity_gauge(self, diversity_data):
        """Create gauge chart for diversity score"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=diversity_data['score'],
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{diversity_data['level']}", 'font': {'size': 24, 'color': '#1DB954'}},
            delta={'reference': 50, 'increasing': {'color': "#1ed760"}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 0, 'tickcolor': "#8696a0"},
                'bar': {'color': "#00a884", 'thickness': 0.75},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(255, 107, 107, 0.3)'},
                    {'range': [40, 60], 'color': 'rgba(255, 206, 87, 0.3)'},
                    {'range': [60, 80], 'color': 'rgba(72, 219, 251, 0.3)'},
                    {'range': [80, 100], 'color': 'rgba(0, 168, 132, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "#00a884", 'width': 4},
                    'thickness': 0.75,
                    'value': diversity_data['score']
                }
            }
        ))
        
        fig.update_layout(
            template='plotly_dark',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': "white", 'family': "Arial Black"}
        )
        return fig
    
    def create_hidden_gems_chart(self, gems_df):
        """Create chart for hidden gems"""
        if len(gems_df) == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="No hidden gems found!<br>All your favorites are popular hits! 🌟",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color='#1DB954')
            )
            fig.update_layout(
                template='plotly_dark',
                height=400,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        colors = ['#1DB954', '#1ed760', '#ff6b6b', '#4ecdc4', '#45b7d1', 
                  '#f093fb', '#f5576c', '#feca57', '#48dbfb', '#ff9ff3']
        
        fig = go.Figure(data=[
            go.Bar(
                y=[f"{row['name'][:30]}..." if len(row['name']) > 30 else row['name'] 
                   for _, row in gems_df.iterrows()],
                x=gems_df['popularity'],
                orientation='h',
                marker=dict(
                    color=colors[:len(gems_df)],
                    line=dict(width=0)
                ),
                text=gems_df['popularity'],
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Popularity: %{x}<br><extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '💎 Your Hidden Gems',
                'font': {'size': 24, 'color': '#f093fb', 'family': 'Arial Black'}
            },
            xaxis_title='Popularity Score',
            yaxis_title='',
            template='plotly_dark',
            height=400,
            plot_bgcolor='rgba(0,0,0,0.3)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
        return fig
    
    def create_binge_chart(self, binge_df):
        """Create chart for binge listening"""
        if len(binge_df) == 0:
            fig = go.Figure()
            fig.add_annotation(
                text="No repeat plays detected!<br>You're exploring new music! 🎵",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=20, color='#1DB954')
            )
            fig.update_layout(
                template='plotly_dark',
                height=400,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            return fig
        
        colors = ['#ff6b6b', '#f5576c', '#ff9ff3', '#fd79a8', '#feca57',
                  '#48dbfb', '#4ecdc4', '#45b7d1', '#1ed760', '#1DB954']
        
        fig = go.Figure(data=[
            go.Bar(
                x=binge_df['name'],
                y=binge_df['plays'],
                marker=dict(
                    color=colors[:len(binge_df)],
                    line=dict(width=0)
                ),
                text=binge_df['plays'],
                textposition='auto',
                textfont=dict(size=16, color='white', family='Arial Black'),
                hovertemplate='<b>%{x}</b><br>Played %{y} times<br><extra></extra>'
            )
        ])
        
        fig.update_layout(
            title={
                'text': '🔁 Songs You Binged',
                'font': {'size': 24, 'color': '#ff6b6b', 'family': 'Arial Black'}
            },
            xaxis_title='Song',
            yaxis_title='Times Played',
            template='plotly_dark',
            height=400,
            plot_bgcolor='rgba(0,0,0,0.3)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
        return fig
