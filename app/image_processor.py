import numpy as np
import tifffile as tiff
import cv2
from sklearn.decomposition import PCA
from skimage.filters import threshold_otsu
from scipy import stats
import dask.array as da
from sklearn.decomposition import IncrementalPCA


class ImageProcessor:
    def __init__(self, image_path):
        # self.image_path = image_path
        # self.image = tiff.imread(image_path)
        # if self.image.ndim != 5:
        #     raise ValueError("Input image should have 5 dimensions (t, z, c, x, y).")
        self.file_path = image_path
        self.image = self.load_large_image(image_path)
    
    def get_metadata(self):
         return {
            "shape": self.image.shape,
            "dtype": str(self.image.dtype),
            "min": float(self.image.min()),
            "max": float(self.image.max()),
        }
    
    def load_large_image(self, file_path):
        """Loads a large TIFF image in chunks using Dask."""
        return da.from_array(tiff.imread(file_path), chunks="auto") 
    
    
    def extract_slice(self, z=None, time=None, channel=None):
        """Extracts a specific slice without loading the entire image into memory."""
        indices = [slice(None)] * 5  

        if z is not None:
            indices[2] = z  
        if time is not None:
            indices[3] = time  
        if channel is not None:
            indices[4] = channel  

        return self.image[tuple(indices)].compute()  
    
    def apply_pca(self, num_components=3):
        """Applies PCA using Dask's incremental processing to handle large images."""
        X, Y, Z, T, C = self.image.shape
        reshaped = self.image.reshape(-1, C)  

      
        reshaped = da.nan_to_num(reshaped)

       
        pca = IncrementalPCA(n_components=num_components)

        def pca_fit(chunk):
            """Function to apply Incremental PCA to each chunk."""
            pca.partial_fit(chunk)
            return chunk

        
        reshaped = reshaped.map_blocks(pca_fit, dtype=reshaped.dtype)

        reduced = pca.transform(reshaped.compute())  
        return reduced.reshape(X, Y, Z, T, num_components)
    
    def compute_statistics(self):
        """Computes mean, standard deviation, min, and max per band using Dask's lazy computation."""
        if self.image is None:
            raise ValueError("Loaded image is None!")

        stats_per_channel = {}
        for c in range(self.image.shape[-1]):
            channel_data = self.image[:, :, :, :, c]  

            stats_per_channel[f"Channel {c}"] = {
                "mean": float(channel_data.mean().compute()),  
                "std": float(channel_data.std().compute()),
                "min": float(channel_data.min().compute()),
                "max": float(channel_data.max().compute()),
            }

        return stats_per_channel

    
    def apply_kmeans_segmentation(self, channel=0, k=3):
        """Applies K-Means clustering for segmentation on a single channel."""
        channel_img = self.image[:, :, :, :, channel] 

        flattened = channel_img.reshape(-1, 1)

        _, labels, _ = cv2.kmeans(
            np.float32(flattened),
            k,
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2),
            10,
            cv2.KMEANS_RANDOM_CENTERS,
        )

        segmented = labels.reshape(channel_img.shape)

        return segmented[..., 0] 



