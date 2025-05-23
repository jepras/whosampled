import pytest
from unittest.mock import patch, Mock
from whosampled.api.genius_client import call_genius_api, BASE_URL

# Sample response data for testing
SAMPLE_SONG_RESPONSE = {
    "response": {
        "song": {
            "id": 123,
            "title": "Test Song",
            "artist_names": "Test Artist"
        }
    }
}

SAMPLE_SEARCH_RESPONSE = {
    "response": {
        "hits": [
            {
                "result": {
                    "id": 123,
                    "full_title": "Test Song",
                    "primary_artist": {"name": "Test Artist"}
                }
            }
        ]
    }
}

@pytest.fixture
def mock_response():
    """Fixture to create a mock response"""
    mock = Mock()
    mock.json.return_value = SAMPLE_SONG_RESPONSE
    return mock

def test_call_genius_api_success(mock_response):
    """Test successful API call"""
    with patch('requests.get', return_value=mock_response) as mock_get:
        result = call_genius_api("/songs/{song_id}", song_id=123)
        
        # Verify the result
        assert result == SAMPLE_SONG_RESPONSE
        assert result["response"]["song"]["id"] == 123
        
        # Verify the API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == f"{BASE_URL}/songs/123"
        assert "headers" in kwargs
        assert "params" in kwargs

def test_call_genius_api_without_song_id(mock_response):
    """Test API call without song_id parameter"""
    with patch('requests.get', return_value=mock_response) as mock_get:
        result = call_genius_api("/search", q="test song")
        
        # Verify the result
        assert result == SAMPLE_SONG_RESPONSE
        
        # Verify the API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert args[0] == f"{BASE_URL}/search"
        assert kwargs["params"]["q"] == "test song"

def test_call_genius_api_error():
    """Test API call error handling"""
    with patch('requests.get', side_effect=Exception("API Error")) as mock_get:
        with pytest.raises(Exception) as exc_info:
            call_genius_api("/songs/{song_id}", song_id=123)
        
        assert "API Error" in str(exc_info.value)
        mock_get.assert_called_once()

def test_call_genius_api_with_query_params(mock_response):
    """Test API call with query parameters"""
    with patch('requests.get', return_value=mock_response) as mock_get:
        params = {"q": "test", "per_page": 10, "page": 1}
        result = call_genius_api("/search", **params)
        
        # Verify the API call
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["params"] == params

def test_call_genius_api_url_formatting():
    """Test URL formatting with different endpoints"""
    with patch('requests.get') as mock_get:
        # Test with song_id
        call_genius_api("/songs/{song_id}", song_id=123)
        args, _ = mock_get.call_args
        assert args[0] == f"{BASE_URL}/songs/123"
        
        # Test without song_id
        call_genius_api("/search")
        args, _ = mock_get.call_args
        assert args[0] == f"{BASE_URL}/search"
        
        # Test with multiple format parameters
        call_genius_api("/artists/{artist_id}/songs/{song_id}", 
                       artist_id=456, song_id=123)
        args, _ = mock_get.call_args
        assert args[0] == f"{BASE_URL}/artists/456/songs/123" 