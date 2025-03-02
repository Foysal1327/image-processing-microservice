import os
import tifffile as tiff
from flask import request
from flask_restful import Resource
from image_processor import ImageProcessor
from flasgger import swag_from

class ImageMetadata(Resource):
    @swag_from({
        'summary': 'Get image metadata',
        'description': 'Retrieve metadata information for the input image.',
        'parameters': [
            {
                'name': 'file_path',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Path to the image file'
            }
        ],
        'responses': {
            200: {'description': 'Image metadata retrieved successfully'},
            400: {'description': 'Invalid request or file path'}
        }
    })
    def get(self):
        file_path = request.args.get("file_path")
        if not file_path or not os.path.exists(file_path):
            return {"error": "File not found"}, 400

        processor = ImageProcessor(file_path)
        metadata = processor.get_metadata()

        return {"metadata": metadata}, 200