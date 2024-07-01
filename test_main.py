import pytest
from fastapi.testclient import TestClient
from main import app, preprocess_text, get_tags_api

# Créez un client de test pour l'application FastAPI
client = TestClient(app)

# Test de l'endpoint principal
def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test de la fonction de prétraitement
def test_preprocess_text():
    text = "This is a simple test sentence"
    processed_text = preprocess_text(text)
    assert processed_text == "simpl test sentenc"

# Test de l'endpoint get_tags_api avec une charge utile valide
def test_get_tags_api_endpoint():
    payload = {"title": "This is a test sentence about python and api.", "threshold": 0.2}
    response = client.post("/get_tags_api", json=payload)
    assert response.status_code == 200
    assert "tags" in response.json()

# Test de l'endpoint get_tags_api avec une charge utile invalide
def test_get_tags_api_endpoint_invalid():
    payload = {"title": "", "threshold": 0.2}
    response = client.post("/get_tags_api", json=payload)
    assert response.status_code == 422

# Test de la fonction get_tags_api
def test_get_tags_api_function():
    title = "This is a test sentence."
    tags = get_tags_api(title, 0.2)
    assert isinstance(tags, list)  # Vérifie que la sortie est une liste

# Test de l'endpoint `/get_tags_api` avec un seuil valide
def test_get_tags_api_endpoint_valid_threshold():
    payload = {"title": "Test", "threshold": 0.5}
    response = client.post("/get_tags_api", json=payload)
    assert response.status_code == 200
    assert "tags" in response.json()

# Test de l'endpoint `/get_tags_api` avec un seuil invalide (inférieur à 0)
def test_get_tags_api_endpoint_invalid_threshold_below():
    payload = {"title": "Test", "threshold": -0.1}
    response = client.post("/get_tags_api", json=payload)
    assert response.status_code == 422
    
# Test de l'endpoint `/get_tags_api` avec un seuil invalide (supérieur à 1)
def test_get_tags_api_endpoint_invalid_threshold_above():
    payload = {"title": "Test", "threshold": 1.1}
    response = client.post("/get_tags_api", json=payload)
    assert response.status_code == 422

# Test de l'endpoint /hello
def test_hello():
    response = client.get("/hello", params={"title": "test"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test de l'endpoint /get_tags avec un paramètre valide
def test_get_tags():
    response = client.get("/get_tags", params={"title": "test"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test de l'endpoint /get_tags avec un paramètre vide
def test_get_tags_empty_title():
    response = client.get("/get_tags", params={"title": ""})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]