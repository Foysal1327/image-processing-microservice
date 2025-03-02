import os
from flask import request
from flask_restful import Resource
from werkzeug.utils import secure_filename
from flasgger import swag_from
import tifffile as tiff
from sqlalchemy.orm import sessionmaker
from database import get_db, ImageMetadata
import logging
from sqlalchemy.exc import IntegrityError

UPLOAD_FOLDER = "data/"
ALLOWED_EXTENSIONS = {"tif", "tiff"}

logging.basicConfig(level=logging.DEBUG)

class UploadImage(Resource):
    @swag_from({
        'summary': 'Upload an image',
        'description': 'Uploads a multi-dimensional TIFF image for processing.',
        'consumes': ['multipart/form-data'],
        'parameters': [
            {
                'name': 'file',
                'in': 'formData',
                'type': 'file',
                'required': True,
                'description': 'TIFF image file to upload'
            }
        ],
        'responses': {
            201: {'description': 'File uploaded successfully'},
            400: {'description': 'Invalid request or file type'}
        }
    })
    def post(self):
        logging.debug("Received upload request")

        if "file" not in request.files:
            logging.error("No file provided in request")
            return {"error": "No file provided"}, 400

        file = request.files["file"]
        if file.filename == "":
            logging.error("No selected file in request")
            return {"error": "No selected file"}, 400

        if not self.allowed_file(file.filename):
            logging.error(f"Invalid file type: {file.filename}")
            return {"error": "Invalid file format. Only .tif and .tiff allowed"}, 400

        try:
            
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            logging.debug(f"File saved at {file_path}")

            image = tiff.imread(file_path)

            if image.ndim != 5:
                logging.error(f"Invalid image dimensions: {image.shape}")
                return {"error": "Image must be 5D (X, Y, Z, Time, Channel)"}, 400

            height, width, depth, time_frames, channels = image.shape

            db = next(get_db())

            existing_entry = db.query(ImageMetadata).filter_by(file_path=file_path).first()
            if existing_entry:
                logging.info(f"Updating existing metadata for {file_path}")
                existing_entry.width = width
                existing_entry.height = height
                existing_entry.depth = depth
                existing_entry.time_frames = time_frames
                existing_entry.channels = channels
                existing_entry.dtype = str(image.dtype)
            else:
                logging.info(f"Inserting new metadata for {file_path}")
                metadata_entry = ImageMetadata(
                    file_path=file_path,
                    width=width,
                    height=height,
                    depth=depth,
                    time_frames=time_frames,
                    channels=channels,
                    dtype=str(image.dtype),
                )
                db.add(metadata_entry)

            db.commit()
            return {"message": "File uploaded successfully", "file_path": file_path}, 201

        except IntegrityError:
            db.rollback()
            logging.error(f"Duplicate entry detected for file: {file_path}")
            return {"error": "File already uploaded"}, 400
        except Exception as e:
            logging.error(f"Error processing file upload: {e}")
            return {"error": "Internal server error"}, 500
    
    @staticmethod
    def allowed_file(filename):
        return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS