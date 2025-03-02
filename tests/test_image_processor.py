import pytest
import numpy as np
import tifffile as tiff
from image_processor import ImageProcessor

# Generate a dummy 5D image (X, Y, Z, Time, Channels)
dummy_image = np.random.randint(0, 256, (100, 100, 10, 5, 3), dtype=np.uint8)
tiff.imwrite("data/test_image.tif", dummy_image)

@pytest.fixture
def processor():
    return ImageProcessor("data/test_image.tif")

def test_metadata(processor):
    """Test retrieving image metadata."""
    metadata = processor.get_metadata()
    assert metadata["shape"] == (100, 100, 10, 5, 3)
    assert metadata["dtype"] == "uint8"

def test_extract_slice(processor):
    """Test extracting a single slice."""
    slice_img = processor.extract_slice(z=5, time=2, channel=1)
    assert slice_img.shape == (100, 100)

def test_pca(processor):
    """Test PCA transformation."""
    reduced = processor.apply_pca(2)
    assert reduced.shape[-1] == 2

def test_statistics(processor):
    """Test computing image statistics."""
    stats = processor.compute_statistics()
    assert "Channel 0" in stats
    assert isinstance(stats["Channel 0"]["mean"], float)


def test_kmeans_segmentation(processor):
    """Test K-Means segmentation."""
    segmented = processor.apply_kmeans_segmentation(channel=0, k=3)
    assert segmented.shape == (100, 100, 10)
