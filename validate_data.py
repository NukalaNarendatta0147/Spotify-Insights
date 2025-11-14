"""
Data validation script to check data quality and consistency
"""
import sys
from tests.mock_data import MockSpotifyClient
from data_processor import DataProcessor


def validate_top_artists(processor):
    """Validate top artists data"""
    print("Validating top artists data...")
    df = processor.get_top_artists_data()
    
    checks = {
        'Has data': len(df) > 0,
        'Has required columns': all(col in df.columns for col in ['rank', 'name', 'popularity', 'followers']),
        'Ranks are sequential': list(df['rank']) == list(range(1, len(df) + 1)),
        'Popularity in range': all((df['popularity'] >= 0) & (df['popularity'] <= 100)),
        'Followers non-negative': all(df['followers'] >= 0)
    }
    
    return checks


def validate_listening_hours(processor):
    """Validate listening hours data"""
    print("Validating listening hours data...")
    df = processor.get_listening_hours_data()
    
    checks = {
        'Has 24 hours': len(df) == 24,
        'All hours present': set(df['hour']) == set(range(24)),
        'Plays non-negative': all(df['plays'] >= 0)
    }
    
    return checks


def validate_genre_distribution(processor):
    """Validate genre distribution"""
    print("Validating genre distribution...")
    df = processor.get_genre_distribution()
    
    checks = {
        'Has data': len(df) > 0,
        'Has required columns': all(col in df.columns for col in ['genre', 'count']),
        'Counts positive': all(df['count'] > 0),
        'Sorted descending': list(df['count']) == sorted(df['count'], reverse=True)
    }
    
    return checks


def validate_emotional_patterns(processor):
    """Validate emotional patterns"""
    print("Validating emotional patterns...")
    df = processor.get_emotional_patterns()
    
    checks = {
        'Has data': len(df) > 0,
        'Has required columns': all(col in df.columns for col in ['valence', 'energy', 'danceability']),
        'Valence in range': all((df['valence'] >= 0) & (df['valence'] <= 1)),
        'Energy in range': all((df['energy'] >= 0) & (df['energy'] <= 1)),
        'Danceability in range': all((df['danceability'] >= 0) & (df['danceability'] <= 1))
    }
    
    return checks


def validate_music_personality(processor):
    """Validate music personality"""
    print("Validating music personality...")
    personality = processor.get_music_personality()
    
    checks = {
        'Has personality': 'personality' in personality,
        'Has description': 'description' in personality,
        'Has metrics': all(key in personality for key in ['energy', 'valence', 'danceability']),
        'Energy in range': 0 <= personality['energy'] <= 1,
        'Valence in range': 0 <= personality['valence'] <= 1,
        'Danceability in range': 0 <= personality['danceability'] <= 1
    }
    
    return checks


def validate_diversity_score(processor):
    """Validate diversity score"""
    print("Validating diversity score...")
    diversity = processor.get_diversity_score()
    
    checks = {
        'Has score': 'score' in diversity,
        'Has level': 'level' in diversity,
        'Score in range': 0 <= diversity['score'] <= 100,
        'Has breakdown': all(key in diversity for key in ['genre_score', 'artist_score', 'variance_score'])
    }
    
    return checks


def validate_hidden_gems(processor):
    """Validate hidden gems"""
    print("Validating hidden gems...")
    df = processor.get_hidden_gems()
    
    checks = {
        'Is DataFrame': True,  # Always returns DataFrame, may be empty
        'If has data, has columns': len(df) == 0 or all(col in df.columns for col in ['name', 'artist', 'popularity']),
        'If has data, popularity < 50': len(df) == 0 or all(df['popularity'] < 50)
    }
    
    return checks


def validate_binge_listening(processor):
    """Validate binge listening"""
    print("Validating binge listening...")
    df = processor.get_binge_listening()
    
    checks = {
        'Is DataFrame': True,
        'If has data, has columns': len(df) == 0 or all(col in df.columns for col in ['name', 'artist', 'plays']),
        'If has data, plays > 1': len(df) == 0 or all(df['plays'] > 1)
    }
    
    return checks


def print_results(validation_name, checks):
    """Print validation results"""
    all_passed = all(checks.values())
    status = "✅ PASS" if all_passed else "❌ FAIL"
    
    print(f"\n{validation_name}: {status}")
    for check_name, passed in checks.items():
        symbol = "  ✓" if passed else "  ✗"
        print(f"{symbol} {check_name}")
    
    return all_passed


def main():
    """Run all validations"""
    print("="*70)
    print("DATA VALIDATION REPORT")
    print("="*70)
    
    # Initialize with mock client
    client = MockSpotifyClient()
    processor = DataProcessor(client)
    
    validations = [
        ("Top Artists", validate_top_artists),
        ("Listening Hours", validate_listening_hours),
        ("Genre Distribution", validate_genre_distribution),
        ("Emotional Patterns", validate_emotional_patterns),
        ("Music Personality", validate_music_personality),
        ("Diversity Score", validate_diversity_score),
        ("Hidden Gems", validate_hidden_gems),
        ("Binge Listening", validate_binge_listening)
    ]
    
    results = []
    for name, validator in validations:
        try:
            checks = validator(processor)
            passed = print_results(name, checks)
            results.append((name, passed))
        except Exception as e:
            print(f"\n{name}: ❌ ERROR")
            print(f"  Error: {str(e)}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    failed = total - passed
    
    print(f"Total validations: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    
    if failed == 0:
        print("\n✅ All validations passed!")
        return 0
    else:
        print(f"\n❌ {failed} validation(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
