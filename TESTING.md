# Testing Guide

## Overview

This project includes comprehensive testing infrastructure with unit tests, integration tests, and mock data for development without API access.

## Test Structure

```
tests/
├── __init__.py
├── mock_data.py              # Mock Spotify data for testing
├── test_spotify_client.py    # Unit tests for Spotify client
├── test_data_processor.py    # Unit tests for data processing
├── test_visualizer.py        # Unit tests for visualizations
└── test_integration.py       # Integration tests
```

## Running Tests

### Run All Tests

Using unittest:
```bash
python run_tests.py
```

Using pytest (recommended):
```bash
pytest
```

### Run Specific Test Files

```bash
# Using unittest
python -m unittest tests.test_data_processor

# Using pytest
pytest tests/test_data_processor.py
```

### Run Specific Test Classes

```bash
# Using unittest
python -m unittest tests.test_data_processor.TestDataProcessor

# Using pytest
pytest tests/test_data_processor.py::TestDataProcessor
```

### Run Specific Test Methods

```bash
# Using unittest
python -m unittest tests.test_data_processor.TestDataProcessor.test_get_top_artists_data

# Using pytest
pytest tests/test_data_processor.py::TestDataProcessor::test_get_top_artists_data
```

## Test Coverage

### Generate Coverage Report

```bash
# Using pytest-cov
pytest --cov=. --cov-report=html --cov-report=term

# Using coverage.py
coverage run -m pytest
coverage report
coverage html
```

### View HTML Coverage Report

After generating the HTML report:
```bash
# Open htmlcov/index.html in your browser
start htmlcov/index.html  # Windows
open htmlcov/index.html   # macOS
xdg-open htmlcov/index.html  # Linux
```

## Development Mode (No API Required)

Run the application with mock data for development without Spotify API access:

```bash
streamlit run dev_mode.py
```

This mode:
- Uses realistic mock data
- Simulates all API responses
- Allows testing UI/UX without API credentials
- Perfect for development and testing

## Mock Data

The `tests/mock_data.py` module provides:

### MockSpotifyClient

A complete mock implementation of the Spotify client:

```python
from tests.mock_data import MockSpotifyClient

client = MockSpotifyClient()
top_artists = client.get_top_artists(limit=10)
top_tracks = client.get_top_tracks(limit=20)
```

### Sample Data

Quick access to sample data:

```python
from tests.mock_data import (
    SAMPLE_TOP_ARTISTS,
    SAMPLE_TOP_TRACKS,
    SAMPLE_AUDIO_FEATURES
)
```

## Test Categories

### Unit Tests

Test individual components in isolation:
- `test_spotify_client.py` - Spotify API client methods
- `test_data_processor.py` - Data processing logic
- `test_visualizer.py` - Visualization creation

### Integration Tests

Test complete workflows:
- `test_integration.py` - End-to-end workflows
- Data validation and quality checks
- Error handling and resilience

## Writing New Tests

### Unit Test Template

```python
import unittest
from unittest.mock import Mock, patch

class TestYourComponent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.component = YourComponent()
    
    def test_your_feature(self):
        """Test description"""
        # Arrange
        input_data = "test"
        
        # Act
        result = self.component.your_method(input_data)
        
        # Assert
        self.assertEqual(result, expected_value)
```

### Integration Test Template

```python
import unittest
from tests.mock_data import MockSpotifyClient

class TestYourWorkflow(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.client = MockSpotifyClient()
    
    def test_complete_workflow(self):
        """Test complete workflow"""
        # Test data flow from client to visualization
        data = self.client.get_data()
        processed = process_data(data)
        viz = create_visualization(processed)
        
        self.assertIsNotNone(viz)
```

## Best Practices

1. **Use Mock Data**: Always use `MockSpotifyClient` for tests
2. **Test Edge Cases**: Include tests for empty data, errors, etc.
3. **Descriptive Names**: Use clear, descriptive test names
4. **Arrange-Act-Assert**: Follow AAA pattern in tests
5. **Independent Tests**: Each test should be independent
6. **Fast Tests**: Keep tests fast by avoiding real API calls

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Troubleshooting

### Import Errors

If you get import errors, ensure you're running tests from the project root:
```bash
cd spotify-insights
python -m pytest
```

### Mock Data Issues

If mock data doesn't match expected format, update `tests/mock_data.py` to match the latest Spotify API response structure.

### Coverage Not Working

Ensure coverage is installed:
```bash
pip install coverage pytest-cov
```

## Test Metrics

Current test coverage goals:
- **Overall Coverage**: > 80%
- **Critical Paths**: > 95%
- **Data Processing**: > 90%
- **Visualizations**: > 85%

## Resources

- [pytest documentation](https://docs.pytest.org/)
- [unittest documentation](https://docs.python.org/3/library/unittest.html)
- [coverage.py documentation](https://coverage.readthedocs.io/)
- [Spotify API documentation](https://developer.spotify.com/documentation/web-api/)
