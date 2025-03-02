from flask import request, send_file
from flask_restful import Resource
import os
import tifffile as tiff
from image_processor import ImageProcessor

class KMeansSegmentation(Resource):
    def get(self):
        file_path = request.args.get("file_path")
        channel = int(request.args.get("channel", 0))
        k = int(request.args.get("k", 3))

        if not os.path.exists(file_path):
            return {"error": "File not found"}, 400

        processor = ImageProcessor(file_path)
        segmented_image = processor.apply_kmeans_segmentation(channel=channel, k=k)

        # output_path = f"data/kmeans_segmented_{channel}_k{k}.tif"
        output_filename = f"kmeans_segmented_{channel}_k{k}.tif"
        output_path = os.path.join(os.getcwd(), "data", output_filename)
        
        tiff.imwrite(output_path, segmented_image.astype("uint8"))

        return {"file_path": output_path}, 200
