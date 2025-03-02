from flask import Flask
from flask_restful import Api
from routes.upload import UploadImage
from routes.metadata import ImageMetadata
from routes.slice import SliceImage
from routes.analyze import AnalyzeImage
from routes.statistics import ImageStatistics
from routes.segmentation import KMeansSegmentation
from flasgger import Swagger

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    'title': 'Image Processing API',
    'uiversion': 3
}
swagger = Swagger(app)

# API routes
api.add_resource(UploadImage, "/upload")
api.add_resource(ImageMetadata, "/metadata")
api.add_resource(SliceImage, "/slice")
api.add_resource(AnalyzeImage, "/analyze")
api.add_resource(ImageStatistics, "/statistics")
api.add_resource(KMeansSegmentation, "/segment/kmeans")

if __name__ == "__main__":
    app.run(debug=True)