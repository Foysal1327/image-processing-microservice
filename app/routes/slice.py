import os
import numpy as np
import tifffile as tiff
from flask import request, send_file
from flask_restful import Resource
from image_processor import ImageProcessor
from flasgger import swag_from

OUTPUT_FOLDER = os.path.abspath("data/") 
OUTPUT_FILE = os.path.join(OUTPUT_FOLDER, "slice_output.tif")

class SliceImage(Resource):
    @swag_from({
        'summary': 'Extract image slice',
        'description': 'Extract a 2D slice from a multi-dimensional TIFF image.',
        'parameters': [
            {
                'name': 'file_path',
                'in': 'query',
                'type': 'string',
                'required': True,
                'description': 'Path to the image file'
            },
            {
                'name': 'z',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'Z-dimension index of the slice'
            },
            {
                'name': 'time',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'Time index of the slice'
            },
            {
                'name': 'channel',
                'in': 'query',
                'type': 'integer',
                'required': True,
                'description': 'Channel index of the slice'
            }
        ],
        'responses': {
            200: {'description': 'Slice extracted successfully'},
            400: {'description': 'Invalid request or file path'}
        }
    })
    def get(self):
        file_path = request.args.get("file_path")
        z = request.args.get("z", type=int)
        time = request.args.get("time", type=int)
        channel = request.args.get("channel", type=int)

        if not file_path or not os.path.exists(file_path):
            return {"error": "File not found"}, 400

        
        if not os.path.exists(OUTPUT_FOLDER):
            os.makedirs(OUTPUT_FOLDER)

        processor = ImageProcessor(file_path)
        sliced_image = processor.extract_slice(z, time, channel)

        tiff.imwrite(OUTPUT_FILE, sliced_image.astype(np.uint8))

        return send_file(OUTPUT_FILE, as_attachment=True)