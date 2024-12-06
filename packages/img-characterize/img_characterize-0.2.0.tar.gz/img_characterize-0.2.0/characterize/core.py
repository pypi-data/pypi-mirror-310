"""Core functionality for image to character art conversion."""

from typing import Dict, List, Tuple, Union, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Pool, cpu_count
import logging
from pathlib import Path
from functools import lru_cache

logger = logging.getLogger(__name__)

# LRU cache for character images
@lru_cache(maxsize=1024)
def _get_cached_char_image(
    char: str,
    size: int,
    font_path: str,
    use_color: bool
) -> Image.Image:
    """Create and cache character image."""
    try:
        font = ImageFont.truetype(font_path, size)
        return _create_char_image(char, size, font, use_color)
    except Exception as e:
        logger.error(f"Error creating cached char image: {str(e)}")
        raise

def process_image(
    image: Image.Image,
    char_list: List[str],
    char_images: Dict[str, Image.Image],
    detail_level: int,
    divide_image_flag: bool = False,
    output_format: str = "png",
    resize: Optional[Tuple[int, int]] = None,
    color: bool = False,
    output_folder: Union[str, Path] = "output",
    use_tkinter: bool = False,
) -> Tuple[List[List[Image.Image]], List[List[str]]]:
    """
    Process an image to convert it into character art.
    """
    try:
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image input")
            
        if not char_images:
            raise ValueError("Character images dictionary is empty")
            
        # Resize image if requested
        if resize:
            image = image.resize(resize, Image.Resampling.LANCZOS)
            
        # Convert image to numpy array for faster processing
        img_array = np.array(image.convert("L"))
        width, height = img_array.shape
        
        # Calculate color levels using vectorized operations
        color_levels = _calculate_color_levels_vectorized(img_array, len(char_list), color)
        
        # Create character mappings in parallel
        with Pool(processes=cpu_count()) as pool:
            # Prepare data for parallel processing
            coords = [(i, j) for i in range(width) for j in range(height)]
            levels = color_levels.flatten()
            chars = [char_list[level] for level in levels]
            
            # Process character images in parallel
            char_images_flat = pool.starmap(
                _process_char_image,
                zip(chars, [char_images] * len(chars))
            )
            
            # Reshape results back to 2D
            char_images_list = [
                [char_images_flat[i * height + j] for j in range(height)]
                for i in range(width)
            ]
            char_text_list = [
                [chars[i * height + j] for j in range(height)]
                for i in range(width)
            ]
            
        return char_images_list, char_text_list
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise

def _process_char_image(char: str, char_images: Dict[str, Image.Image]) -> Image.Image:
    """Process a single character image (for parallel processing)."""
    try:
        if char not in char_images:
            raise KeyError(f"Character '{char}' not found in character images dictionary")
        return char_images[char]
    except Exception as e:
        logger.error(f"Error processing char image: {str(e)}")
        raise

def _create_char_image_worker(args: Tuple[str, int, str, bool]) -> Tuple[str, Optional[Image.Image]]:
    """Worker function for creating character images."""
    try:
        char, detail, font_path, color = args
        img = _get_cached_char_image(char, detail, font_path, color)
        return char, img
    except Exception as e:
        logger.error(f"Error in char image worker for char '{args[0]}': {str(e)}")
        return args[0], None

def create_char_image_dict(
    characters: List[str],
    detail: int,
    font_path: Union[str, Path],
    color: bool = False
) -> Dict[str, Image.Image]:
    """
    Create a dictionary mapping characters to their image representations.
    """
    try:
        if not characters:
            raise ValueError("Empty character list")
            
        if not isinstance(font_path, (str, Path)):
            raise ValueError("Invalid font path")
            
        # Verify font file exists
        font_path = Path(font_path)
        if not font_path.exists():
            raise FileNotFoundError(f"Font file not found: {font_path}")
            
        # Prepare arguments for the worker function
        args = [(char, detail, str(font_path), color) for char in characters]
        
        # Use multiprocessing for parallel character image creation
        with Pool(processes=cpu_count()) as pool:
            results = pool.map(_create_char_image_worker, args)
            
        # Filter out failed results and convert to dictionary
        char_images = {char: img for char, img in results if img is not None}
        
        if not char_images:
            raise ValueError("Failed to create any character images")
            
        failed_chars = set(characters) - set(char_images.keys())
        if failed_chars:
            logger.warning(f"Failed to create images for characters: {failed_chars}")
            
        return char_images
        
    except Exception as e:
        logger.error(f"Error creating character images: {str(e)}")
        raise

def _calculate_color_levels_vectorized(
    img_array: np.ndarray,
    num_chars: int,
    use_color: bool
) -> np.ndarray:
    """Calculate color levels using vectorized operations."""
    try:
        # Normalize to [0, 1]
        color_levels = img_array / 255.0
        
        if not use_color:
            # Calculate threshold using vectorized operations
            threshold = np.percentile(color_levels, 90)
            
            # Vectorized amplification
            deviations = np.abs(color_levels - threshold)
            amplification = np.where(
                color_levels >= threshold,
                1 + deviations,
                1 - deviations
            )
            color_levels = np.clip(color_levels * amplification, 0, 1)
        
        # Convert to character indices
        return (color_levels * (num_chars - 1)).astype(int)
    except Exception as e:
        logger.error(f"Error calculating color levels: {str(e)}")
        raise

def _create_char_image(
    char: str,
    size: int,
    font: ImageFont.FreeTypeFont,
    use_color: bool
) -> Image.Image:
    """Create an image representation of a character."""
    try:
        mode = "RGBA" if use_color else "L"
        color = (0, 0, 0, 0) if use_color else 0
        fill = (255, 255, 255, 255) if use_color else 255
        
        img = Image.new(mode, (size, size), color=color)
        draw = ImageDraw.Draw(img)
        
        # Get text size for centering
        bbox = draw.textbbox((0, 0), char, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        # Calculate position to center text
        x = (size - text_width) / 2
        y = (size - text_height) / 2
        
        draw.text(
            (x, y),
            char,
            font=font,
            fill=fill
        )
        return img
    except Exception as e:
        logger.error(f"Error creating char image: {str(e)}")
        raise

def _amplify_differences(values: List[float], threshold: float) -> List[float]:
    """Amplify differences in color values for better contrast."""
    try:
        values = np.array(values)
        deviations = np.abs(values - threshold)
        
        # Apply different amplification based on threshold
        amplification = np.where(
            values >= threshold,
            1 + deviations,  # Amplify bright areas
            1 - deviations   # Reduce dark areas
        )
        
        # Apply amplification and clip to valid range
        return np.clip(values * amplification, 0, 1)
    except Exception as e:
        logger.error(f"Error amplifying differences: {str(e)}")
        raise