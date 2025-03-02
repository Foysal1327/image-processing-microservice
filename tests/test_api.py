import os
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_upload():
    """Test uploading an image."""
    file_path = "data/test_image.tif"
    if not os.path.exists(file_path):
        assert False, "Test image file does not exist."

    with open(file_path, "rb") as file:
        response = requests.post(f"{BASE_URL}/upload", files={"file": file})

    assert response.status_code == 201
    assert "File uploaded successfully" in response.json()["message"]

def test_metadata():
    """Test fetching image metadata."""
    response = requests.get(f"{BASE_URL}/metadata?file_path=data/test_image.tif")
    assert response.status_code == 200
    assert "metadata" in response.json()

def test_slice():
    """Test extracting a slice from the image."""
    response = requests.get(f"{BASE_URL}/slice?file_path=data/test_image.tif&z=5&time=2&channel=1")
    assert response.status_code == 200

def test_pca():
    """Test performing PCA analysis."""
    payload = {"file_path": "data/test_image.tif", "components": 3}
    response = requests.post(f"{BASE_URL}/analyze", json=payload)
    assert response.status_code == 200
    assert "PCA analysis completed" in response.json()["message"]

def test_statistics():
    """Test retrieving image statistics."""
    response = requests.get(f"{BASE_URL}/statistics?file_path=data/test_image.tif")
    assert response.status_code == 200
    assert "statistics" in response.json()

def test_kmeans_segmentation():
    """Test performing K-Means segmentation."""
    params = {
        "file_path": "data/test_image.tif",
        "channel": 0,
        "k": 3
    }
    response = requests.get(f"{BASE_URL}/segment/kmeans", params=params)

    assert response.status_code == 200
    result = response.json()

    assert "file_path" in result  
    assert os.path.exists(result["file_path"])  

if __name__ == "__main__":
    print("Running API tests...")
    test_upload()
    test_metadata()
    test_slice()
    test_pca()
    test_statistics()
    print("✅ All API tests passed!")
