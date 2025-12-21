# preprocessing/steps.py

import cv2
import numpy as np

def ensure_png_compatible(img: np.ndarray) -> np.ndarray:
    """
    Ensures the image is PNG-compatible:
    - uint8 dtype
    - 1-channel (grayscale) or 3-channel (RGB)
    """

    if img is None:
        raise ValueError("Invalid image input")

    # Ensure uint8
    if img.dtype != np.uint8:
        img = np.clip(img, 0, 255).astype(np.uint8)

    # Convert RGBA → RGB
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    return img

# preprocessing/steps.py

import cv2
import numpy as np

def resize_image(img: np.ndarray, target_width: int = 1800) -> np.ndarray:
    """
    Resize a single image to a target width while maintaining aspect ratio.
    DPI change is not needed in memory, only pixel size matters.

    Parameters:
    - img: np.ndarray, input image (BGR)
    - target_width: int, desired width in pixels

    Returns:
    - img: np.ndarray, resized image
    """
    if img is None:
        raise ValueError("Input image is None")

    h, w = img.shape[:2]

    # Resize only if width < target_width
    if w < target_width:
        scale = target_width / w
        new_w = target_width
        new_h = int(h * scale)
        img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

    return img


def apply_clahe_only(img: np.ndarray, clip_limit: float = 2.0, tile_grid_size: tuple = (8, 8)) -> np.ndarray:
    """
    Convert an image to 8-bit grayscale and apply CLAHE (illumination normalization only).
    Does not apply brightness standardization.
    
    Parameters:
    - img: np.ndarray, input image (BGR or RGB)
    - clip_limit: float, CLAHE clip limit
    - tile_grid_size: tuple, CLAHE tile grid size
    
    Returns:
    - gray_clahe: np.ndarray, grayscale image with CLAHE applied
    """
    if img is None:
        raise ValueError("Input image is None")

    # 1. Convert to grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()  # already grayscale

    # 2. Apply CLAHE
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    gray_clahe = clahe.apply(gray)

    return gray_clahe

# preprocessing/steps.py



def denoise_image(img: np.ndarray, h: float = 8, template_window_size: int = 7, search_window_size: int = 21) -> np.ndarray:
    """
    Apply Non-Local Means Denoising to a grayscale image.

    Parameters:
    - img: np.ndarray, input grayscale image
    - h: float, filter strength. Higher h = more denoising
    - template_window_size: int, size of template patch
    - search_window_size: int, size of search window

    Returns:
    - denoised: np.ndarray, denoised image
    """
    if img is None:
        raise ValueError("Input image is None")

    # Ensure image is single-channel
    if len(img.shape) != 2:
        raise ValueError("Denoising expects a grayscale image")

    denoised = cv2.fastNlMeansDenoising(
        img,
        None,
        h=h,
        templateWindowSize=template_window_size,
        searchWindowSize=search_window_size
    )

    return denoised


def clahe_contrast_enhancement(img: np.ndarray, clip_limit: float = 2.5, tile_grid_size: tuple = (12, 12)) -> np.ndarray:
    """
    Apply CLAHE for contrast enhancement on a grayscale image.
    
    Parameters:
    - img: np.ndarray, input grayscale image
    - clip_limit: float, CLAHE clip limit
    - tile_grid_size: tuple, CLAHE tile grid size
    
    Returns:
    - enhanced: np.ndarray, contrast-enhanced image
    """
    if img is None:
        raise ValueError("Input image is None")

    # Ensure grayscale
    if len(img.shape) != 2:
        raise ValueError("CLAHE contrast enhancement expects a grayscale image")

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_grid_size)
    enhanced = clahe.apply(img)

    return enhanced


