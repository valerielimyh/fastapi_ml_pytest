import json
from src.app import crud

def test_get_genre(test_app, monkeypatch):
  test_data = [
  {
    "predictions": "metal"
  },
  {
    "predictions": "folk"
  },
  {
    "predictions": "soul and reggae"
  },
  {
    "predictions": "pop"
  },
  {
    "predictions": "classic pop and rock"
  },
  {
    "predictions": "dance and electronica"
  },
  {
    "predictions": "punk"
  },
  {
    "predictions": "jazz and blues"
  }
]
  async def mock_get_genre():
        return test_data
  monkeypatch.setattr(crud, "get_genre", mock_get_genre)
  response = test_app.get("/get_genre/")
  assert response.status_code == 200
  assert response.json() == test_data
  