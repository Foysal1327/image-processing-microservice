import os
import numpy as np
import tifffile as tiff
from flask import request
from flask_restful import Resource
from image_processor import ImageProcessor
from flasgger import swag_from
from sqlalchemy.orm import sessionmaker
from database import get_db, ImageAnalysis
import logging

logging.basicConfig(level=logging.DEBUG)

class AnalyzeImage(Resource):
    @swag_from({
        'summary': 'Perform PCA analysis',
        'description': 'Perform Principal Component Analysis (PCA) on the input image.',
        'parameters': [
            {
                'name': 'file_path',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Path to the image file'
            },
            {
                'name': 'components',
                'in': 'query',
                'type': 'integer',
                'required': False,
                'description': 'Number of principal components to retain (default=3)'
            }
        ],
        'responses': {
            200: {'description': 'PCA analysis completed'},
            400: {'description': 'Invalid request or file path'}   
        }
    })
    
    def post(self):
        data = request.get_json()
        file_path = data.get("file_path")
        components = data.get("components", 3)

        if not file_path or not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            return {"error": "File not found"}, 400

        try:
            processor = ImageProcessor(file_path)
            reduced_image = processor.apply_pca(components)

            if reduced_image is None or np.isnan(reduced_image).any():
                logging.error(f"PCA failed: Output contains NaN values.")
                return {"error": "PCA computation failed"}, 500

            output_path = f"data/pca_output_{components}.tif"
            tiff.imwrite(output_path, reduced_image.astype(np.uint8))

     
            db = next(get_db())
            analysis_entry = ImageAnalysis(
                file_path=file_path,
                pca_components=components
            )
            db.add(analysis_entry)
            db.commit()

            return {"message": "PCA analysis completed", "file_path": output_path}, 200

        except Exception as e:
            logging.error(f"Error during PCA processing: {e}")
            return {"error": "Internal server error"}, 500