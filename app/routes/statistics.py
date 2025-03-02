import os
from flask import request
from flask_restful import Resource
from image_processor import ImageProcessor
from flasgger import swag_from
import logging
from sqlalchemy.orm import sessionmaker
from database import get_db, ImageAnalysis

class ImageStatistics(Resource):
    @swag_from({
        'summary': 'Get image statistics',
        'description': 'Compute and return statistics for the input image.',
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
            200: {'description': 'Image statistics computed successfully'},
            400: {'description': 'Invalid request or file path'}
        }
    })
    def get(self):
        file_path = request.args.get("file_path")

        if not file_path or not os.path.exists(file_path):
            return {"error": "File not found"}, 400

        try:
            processor = ImageProcessor(file_path)
            stats = processor.compute_statistics()

            # save statistics to database
            db = next(get_db())
            analysis_entry = ImageAnalysis(
                file_path=file_path,
                statistics=stats
            )
            db.add(analysis_entry)
            db.commit()

            return {"statistics": stats}, 200
        except Exception as e:
            logging.error(f"Error processing image statistics: {e}")
            return {"error": "Internal server error"}, 500
