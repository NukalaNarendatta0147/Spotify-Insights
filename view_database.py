"""
View SQLite Database Contents
Simple script to view your Spotify database
"""

import sqlite3
import pandas as pd

def view_database(db_name="spotify_data.db"):
    """View database contents"""
    try:
        conn = sqlite3.connect(db_name)
        
        print("=" * 60)
        print("📊 SPOTIFY DATABASE VIEWER")
        print("=" * 60)
        print()
        
        # List all tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("Available tables:")
        for idx, table in enumerate(tables, 1):
            print(f"   {idx}. {table[0]}")
        
        print()
        print("=" * 60)
        
        # Show each table
        for table in tables:
            table_name = table[0]
            print(f"\n📋 TABLE: {table_name}")
            print("-" * 60)
            
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            print(f"Total records: {len(df)}")
            print()
            print(df.head(10).to_string())
            print()
        
        conn.close()
        
        print("=" * 60)
        print("✅ Database viewing completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("Make sure 'spotify_data.db' exists in the current directory.")

if __name__ == "__main__":
    view_database()
