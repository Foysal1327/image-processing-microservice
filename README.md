📸 Image Processing Microservice

A microservice for **high-dimensional image processing** (5D TIFF images) using **Flask, Dask, and SQLAlchemy**.  
It supports **PCA, segmentation (K-Means, Otsu), chunked processing, and REST API access**.

---

## **📦 Installation & Setup**
###  Clone the Repository**

git clone https://github.com/Foysal1327/image-processing-microservice.git
cd image-processing-microservice

Create a Virtual Environment

python -m venv myenv
source myenv/bin/activate  # macOS/Linux
myenv\Scripts\activate      # Windows

Install Dependencies
pip install -r requirements.txt


🚀 Running the API
1️⃣ Start the Flask server:
python app/main.py

2️⃣ Open Swagger UI in your browser to test endpoints interactively:
http://127.0.0.1:5000/apidocs/

🔗 API Endpoints
Here are the available REST API endpoints and how to use them.

1️⃣ Upload an Image
Uploads a multi-dimensional TIFF image.

cURL Request:
curl -X POST -F "file=@data/test_image.tif" http://127.0.0.1:5000/upload
Response:
{
  "message": "File uploaded successfully",
  "file_path": "data/test_image.tif"
}
2️⃣ Get Image Metadata
Retrieves metadata of the uploaded image, such as dimensions and channels.

cURL Request:
curl "http://127.0.0.1:5000/metadata?file_path=data/test_image.tif"
Response:
{
  "metadata": {
    "shape": [100, 100, 10, 5, 3],
    "dtype": "uint8"
  }
}
3️⃣ Extract a Specific Slice
Extracts a slice from the image based on user input (Z, Time, Channel).
curl "http://127.0.0.1:5000/slice?file_path=data/test_image.tif&z=5&time=2&channel=1"
Response:
Returns a TIFF file containing the requested slice.

4️⃣ Perform PCA (Dimensionality Reduction)
Applies Principal Component Analysis (PCA) to reduce the number of spectral bands.

cURL Request:
curl -X POST -H "Content-Type: application/json" -d '{"file_path": "data/test_image.tif", "components": 3}' http://127.0.0.1:5000/analyze
Response:
{
  "message": "PCA analysis completed",
  "file_path": "data/pca_output_3.tif"
}

5️⃣ Get Image Statistics
Returns mean, standard deviation, min, and max for each spectral band.

cURL Request:
curl "http://127.0.0.1:5000/statistics?file_path=data/test_image.tif"
Response:
{
  "statistics": {
    "Channel 0": {
      "mean": 125.6,
      "std": 20.1,
      "min": 0,
      "max": 255
    },
    "Channel 1": { ... },
    "Channel 2": { ... }
  }
}
🧪 Running Tests
Run unit tests and check test coverage:

pytest --cov=app --cov=image_processor --cov-report=html --disable-warnings
Check the coverage report in htmlcov/index.html.

🌟 Additional Features
✅ Chunked Processing with Dask for large images
✅ SQLite/PostgreSQL Storage for metadata & analysis results
✅ Swagger API Documentation for easy testing
