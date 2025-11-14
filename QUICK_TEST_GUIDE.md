# Quick Testing Guide

## ✅ All Tests Passing (46/46)

## Run Tests

### Option 1: Using run_tests.py (Recommended)
```bash
python run_tests.py
```

### Option 2: Using pytest (if installed)
```bash
pytest
pytest -v  # verbose
pytest --cov=. --cov-report=html  # with coverage
```

### Option 3: Using unittest directly
```bash
python -m unittest discover tests
```

## Test Development Mode

Run the app without Spotify API:
```bash
streamlit run dev_mode.py
```

## Test Coverage

Current coverage: **80%+**

### Generate Coverage Report
```bash
# Install coverage if needed
pip install coverage pytest-cov

# Run with coverage
pytest --cov=. --cov-report=html --cov-report=term

# View HTML report
start htmlcov/index.html  # Windows
```

## Test Structure

```
tests/
├── test_spotify_client.py     ✅ 8 tests  - API client
├── test_data_processor.py     ✅ 10 tests - Data processing
├── test_visualizer.py         ✅ 13 tests - Visualizations
├── test_integration.py        ✅ 15 tests - End-to-end workflows
└── mock_data.py               📦 Mock data provider
```

## Quick Commands

```bash
# Run all tests
python run_tests.py

# Run specific test file
python -m unittest tests.test_data_processor

# Run specific test class
python -m unittest tests.test_data_processor.TestDataProcessor

# Run specific test method
python -m unittest tests.test_data_processor.TestDataProcessor.test_get_top_artists_data

# Run with verbose output
python run_tests.py -v
```

## Mock Data Usage

```python
from tests.mock_data import MockSpotifyClient

# Use in your code
client = MockSpotifyClient()
artists = client.get_top_artists(limit=10)
tracks = client.get_top_tracks(limit=20)
```

## CI/CD

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Multiple OS (Ubuntu, Windows, macOS)
- Multiple Python versions (3.9, 3.10, 3.11)

See `.github/workflows/tests.yml` for configuration.

## Troubleshooting

### Import Errors
Run from project root:
```bash
cd spotify-insights
python run_tests.py
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Pytest Not Found
```bash
pip install pytest pytest-cov
```

## Test Categories

### ✅ Unit Tests (31 tests)
- Spotify client methods
- Data processing functions
- Visualization creation

### ✅ Integration Tests (15 tests)
- Complete workflows
- Data validation
- Error handling

## Next Steps

1. ✅ Run tests: `python run_tests.py`
2. ✅ Check coverage: `pytest --cov=.`
3. ✅ Try dev mode: `streamlit run dev_mode.py`
4. ✅ Read full guide: [TESTING.md](TESTING.md)
