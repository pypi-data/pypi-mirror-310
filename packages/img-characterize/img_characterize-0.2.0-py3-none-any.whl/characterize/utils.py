"""Utility functions for image processing and file operations."""

from typing import List, Union, Optional, Tuple
from pathlib import Path
import logging
from PIL import Image
import numpy as np
from multiprocessing import Pool, cpu_count
import subprocess
from tqdm import tqdm
import os

logger = logging.getLogger(__name__)

def divide_image(
    image: Image.Image,
    min_size: int = 1000000
) -> List[Tuple[Image.Image, Tuple[int, int]]]:
    """
    Divide a large image into smaller parts using NumPy for efficiency.
    
    Args:
        image: Input PIL Image
        min_size: Minimum size threshold for division
        
    Returns:
        List of tuples containing (Image, (x_offset, y_offset))
    """
    try:
        # Convert to numpy array for faster processing
        img_array = np.array(image)
        w, h = image.size
        current_size = w * h
        
        if current_size < min_size:
            return [(image, (0, 0))]
            
        # Calculate optimal division size
        div_factor = int(np.ceil(np.sqrt(current_size / min_size)))
        chunk_w = w // div_factor
        chunk_h = h // div_factor
        
        divided_images = []
        
        # Use numpy array slicing for faster division
        for i in range(div_factor):
            for j in range(div_factor):
                x_start = i * chunk_w
                y_start = j * chunk_h
                x_end = min((i + 1) * chunk_w, w)
                y_end = min((j + 1) * chunk_h, h)
                
                chunk = img_array[y_start:y_end, x_start:x_end]
                chunk_image = Image.fromarray(chunk)
                divided_images.append((chunk_image, (x_start, y_start)))
                
        return divided_images
        
    except Exception as e:
        logger.error(f"Error dividing image: {str(e)}")
        raise

def unite_image(
    char_images: List[List[Image.Image]],
    width: int,
    height: int,
    detail_level: int,
    max_chunk_size: int = 100
) -> Image.Image:
    """
    Combine character images into a single image using memory-efficient processing.
    
    Args:
        char_images: 2D list of character images
        width: Original image width
        height: Original image height
        detail_level: Size of each character image
        max_chunk_size: Maximum size for processing chunks
        
    Returns:
        Combined PIL Image
    """
    try:
        # Validate input dimensions
        if width <= 0 or height <= 0 or detail_level <= 0:
            raise ValueError(f"Invalid dimensions: width={width}, height={height}, detail_level={detail_level}")
            
        # Calculate final image dimensions
        final_width = width * detail_level
        final_height = height * detail_level
        
        # Validate final dimensions
        max_dimension = 65535  # PIL's maximum image dimension
        if final_width > max_dimension or final_height > max_dimension:
            raise ValueError(f"Final image dimensions too large: {final_width}x{final_height}")
        
        # Create empty PIL image for the result
        final_image = Image.new('RGBA', (final_width, final_height), (0, 0, 0, 0))
        
        # Process in chunks to manage memory usage
        chunk_size = min(max_chunk_size, min(width, height))
        
        for start_x in range(0, width, chunk_size):
            end_x = min(start_x + chunk_size, width)
            for start_y in range(0, height, chunk_size):
                end_y = min(start_y + chunk_size, height)
                
                # Process current chunk
                for i in range(start_x, end_x):
                    for j in range(start_y, end_y):
                        try:
                            char_img = char_images[i][j].convert("RGBA")
                            final_image.paste(
                                char_img,
                                (i * detail_level, j * detail_level),
                                char_img
                            )
                        except Exception as e:
                            logger.error(f"Error processing character at position ({i}, {j}): {str(e)}")
                            continue
        
        return final_image
        
    except Exception as e:
        logger.error(f"Error uniting images: {str(e)}")
        raise

def save_image(
    image: Image.Image,
    output_format: List[str],
    use_color: bool,
    filename: Union[str, Path],
    max_attempts: int = 3
) -> None:
    """
    Save image with optimized compression and parallel processing.
    
    Args:
        image: PIL Image to save
        output_format: List of desired output formats (png or jpg)
        use_color: Whether to preserve color
        filename: Output filename
        max_attempts: Maximum number of save attempts
    """
    save_options = {
        "png": {
            "format": "PNG",
            "compress_level": 6,  # Reduced from 9 for better performance
            "optimize": True
        },
        "jpg": {
            "format": "JPEG",
            "quality": 85,  # Reduced from 95 for better performance
            "optimize": True
        }
    }
    
    try:
        # Convert to Path object and create parent directories
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        # Validate image
        if not isinstance(image, Image.Image):
            raise ValueError("Invalid image input")
            
        # Convert image to appropriate format
        if use_color:
            if image.mode != "RGB":
                image = image.convert("RGB")
        else:
            if image.mode != "L":
                image = image.convert("L")
        
        # Save with format-specific optimizations
        for fmt in output_format:
            if fmt not in ["png", "jpg"]:
                logger.warning(f"Unsupported format: {fmt}")
                continue
                
            output_path = filename.with_suffix(f".{fmt}")
            
            # Try to save with multiple attempts
            for attempt in range(max_attempts):
                try:
                    image.save(output_path, **save_options[fmt])
                    logger.info(f"Successfully saved image as {output_path}")
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(f"Save attempt {attempt + 1} failed: {str(e)}")
                    
    except Exception as e:
        logger.error(f"Error saving image: {str(e)}", exc_info=True)
        raise

def save_text(
    characters: List[List[str]],
    filename: Union[str, Path]
) -> None:
    """
    Save character art as text file with efficient buffering.
    
    Args:
        characters: 2D list of characters
        filename: Output filename
    """
    try:
        filename = Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        
        # Validate input
        if not characters or not characters[0]:
            raise ValueError("Empty character list")
            
        # Use list comprehension for faster string joining
        text_content = "\n".join(" ".join(line) for line in characters)
        
        # Write with large buffer size for better performance
        with open(filename.with_suffix(".txt"), "w", encoding="utf-8", buffering=1048576) as f:
            f.write(text_content)
            
        logger.info(f"Successfully saved text file as {filename}")
        
    except Exception as e:
        logger.error(f"Error saving text file: {str(e)}", exc_info=True)
        raise

def optimize_file(filepath: Union[str, Path]) -> None:
    """
    Optimize file size using parallel compression.
    
    Args:
        filepath: Path to file to optimize
    """
    try:
        filepath = Path(filepath)
        if not filepath.exists():
            logger.error(f"File not found: {filepath}")
            return
            
        if filepath.suffix.lower() == ".png":
            # Use optipng for PNG optimization
            subprocess.run(
                ["optipng", "-o3", str(filepath)],  # Reduced from -o5 for better performance
                check=True,
                capture_output=True
            )
        elif filepath.suffix.lower() in {".jpg", ".jpeg"}:
            # Use jpegtran for JPEG optimization
            subprocess.run(
                ["jpegtran", "-optimize", "-progressive", "-outfile", str(filepath), str(filepath)],
                check=True,
                capture_output=True
            )
            
        logger.info(f"Successfully optimized {filepath}")
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Error optimizing file: {str(e)}")
        raise
    except FileNotFoundError:
        logger.warning("Optimization tools not found, skipping optimization")

def optimize_files(
    files: List[Union[str, Path]],
    num_processes: Optional[int] = None
) -> None:
    """
    Optimize multiple files using parallel processing.
    
    Args:
        files: List of file paths to optimize
        num_processes: Number of processes to use
    """
    if not num_processes:
        num_processes = min(cpu_count(), 4)  # Limit to 4 processes
        
    try:
        with Pool(processes=num_processes) as pool:
            list(tqdm(
                pool.imap_unordered(optimize_file, files),
                total=len(files),
                desc="Optimizing files"
            ))
            
    except Exception as e:
        logger.error(f"Error in parallel file optimization: {str(e)}")
        raise