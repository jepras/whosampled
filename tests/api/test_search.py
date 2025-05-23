import pytest
from unittest.mock import patch, Mock
from whosampled.api.search import get_search_results, search_song

# Sample response data for testing
SAMPLE_SEARCH_RESPONSE = {
    "response": {
        "hits": [
            {
                "result": {
                    "id": 123,
                    "full_title": "Test Song by Test Artist",
                    "primary_artist": {"name": "Test Artist"}
                }
            },
            {
                "result": {
                    "id": 456,
                    "full_title": "Another Song by Test Artist",
                    "primary_artist": {"name": "Test Artist"}
                }
            }
        ]
    }
}

@pytest.fixture
def mock_search_response():
    """Fixture to create a mock search response"""
    mock = Mock()
    mock.json.return_value = SAMPLE_SEARCH_RESPONSE
    return mock

def test_get_search_results_success(mock_search_response):
    """Test successful search results for dropdown menu"""
    with patch('requests.get', return_value=mock_search_response) as mock_get:
        results = get_search_results("test song")
        
        # Verify the results
        assert len(results) == 2
        assert results[0][0] == "Test Song by Test Artist"
        assert results[0][1] == 123
        assert results[1][0] == "Another Song by Test Artist"
        assert results[1][1] == 456
        
        # Verify the API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert "search" in args[0]
        assert kwargs["params"]["q"] == "test song"

def test_get_search_results_empty_query():
    """Test search with empty query"""
    results = get_search_results("")
    assert results == []

def test_get_search_results_no_results(mock_search_response):
    """Test search with no results"""
    mock_search_response.json.return_value = {"response": {"hits": []}}
    
    with patch('requests.get', return_value=mock_search_response):
        results = get_search_results("nonexistent song")
        assert results == []

def test_get_search_results_error():
    """Test search error handling"""
    with patch('requests.get', side_effect=Exception("API Error")):
        results = get_search_results("test song")
        assert results == []

def test_search_song_success(mock_search_response):
    """Test successful song search"""
    with patch('requests.get', return_value=mock_search_response) as mock_get:
        song_id = search_song("Test Song")
        assert song_id == 123
        assert mock_get.call_count == 1

def test_search_song_no_match(mock_search_response):
    """Test search with no matching results"""
    mock_search_response.json.return_value = {"response": {"hits": []}}
    
    with patch('requests.get', return_value=mock_search_response) as mock_get:
        song_id = search_song("nonexistent song")
        assert song_id is None
        assert mock_get.call_count == 1

def test_search_song_error():
    """Test search error handling"""
    with patch('requests.get', side_effect=Exception("API Error")) as mock_get:
        song_id = search_song("test song")
        assert song_id is None
        assert mock_get.call_count == 1 