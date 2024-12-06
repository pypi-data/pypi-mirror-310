"""Core functionality for image to character art conversion."""

from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional, Union
import logging
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageEnhance

logger = logging.getLogger(__name__)

@dataclass
class ConversionConfig:
    """Configuration for character conversion."""
    detail_level: int
    font_path: Union[str, Path]
    character_set: str
    color_mode: bool = False
    subdivide: bool = False
    optimize: bool = False
    empty_char: bool = False
    output_formats: List[str] = None

    def __post_init__(self):
        """Validate and process configuration."""
        self.font_path = Path(self.font_path)
        if not self.font_path.exists():
            raise ValueError(f"Font file not found: {self.font_path}")
            
        if self.output_formats is None:
            self.output_formats = ["png"]
        
        valid_formats = {"png", "jpg", "txt"}
        invalid_formats = set(self.output_formats) - valid_formats
        if invalid_formats:
            raise ValueError(f"Invalid output formats: {invalid_formats}")

class CharacterConverter:
    """Converts images to character art."""
    
    def __init__(self, config: ConversionConfig):
        """Initialize converter with configuration."""
        self.config = config
        self._char_images = {}
        self._character_ranking = []
        
    def convert_image(self, image_path: Union[str, Path]) -> Image.Image:
        """Convert an image to character art."""
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
            
        # Load and preprocess image
        image = self._load_image(image_path)
        if self.config.subdivide:
            image_parts = self._subdivide_image(image)
        else:
            image_parts = [image]
            
        # Convert each part
        results = []
        for part in image_parts:
            enhanced = self._enhance_image(part)
            char_map = self._create_character_map(enhanced)
            result = self._compose_result(char_map, part.size)
            results.append(result)
            
        # Combine results if needed
        if len(results) > 1:
            return self._combine_results(results)
        return results[0]
        
    def _load_image(self, path: Path) -> Image.Image:
        """Load and prepare image for conversion."""
        try:
            image = Image.open(path).convert("RGB")
            return image
        except Exception as e:
            logger.error(f"Error loading image {path}: {e}")
            raise
            
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Enhance image for better conversion results."""
        if self.config.color_mode:
            return ImageEnhance.Color(image).enhance(2)
        return image
        
    def _subdivide_image(self, image: Image.Image, max_size: int = 408960) -> List[Image.Image]:
        """Divide large images into manageable parts."""
        if image.size[0] * image.size[1] < max_size:
            return [image]
            
        parts = []
        width, height = image.size
        
        # Divide into quarters
        regions = [
            (0, 0, width//2, height//2),
            (width//2, 0, width, height//2),
            (0, height//2, width//2, height),
            (width//2, height//2, width, height)
        ]
        
        for region in regions:
            part = image.crop(region)
            if part.size[0] * part.size[1] >= max_size:
                parts.extend(self._subdivide_image(part, max_size))
            else:
                parts.append(part)
                
        return parts
        
    def _create_character_map(self, image: Image.Image) -> List[List[str]]:
        """Create a map of characters representing the image."""
        # Convert to grayscale for intensity mapping
        gray = image.convert("L")
        pixels = np.array(gray)
        
        # Normalize and map to characters
        normalized = pixels / 255.0
        char_indices = (normalized * (len(self._character_ranking) - 1)).astype(int)
        
        return [[self._character_ranking[idx] for idx in row] for row in char_indices]
        
    def _compose_result(self, char_map: List[List[str]], size: Tuple[int, int]) -> Image.Image:
        """Compose the final image from character map."""
        width, height = size
        detail = self.config.detail_level
        
        # Create base image
        result = Image.new("RGBA", (width * detail, height * detail), (0, 0, 0, 0))
        
        # Place characters
        for y, row in enumerate(char_map):
            for x, char in enumerate(row):
                if char in self._char_images:
                    char_img = self._char_images[char]
                    result.paste(
                        char_img,
                        (x * detail, y * detail),
                        char_img
                    )
                    
        return result
        
    def _combine_results(self, results: List[Image.Image]) -> Image.Image:
        """Combine multiple results into a single image."""
        # Calculate total size
        total_width = max(img.size[0] for img in results)
        total_height = sum(img.size[1] for img in results)
        
        # Create combined image
        combined = Image.new("RGBA", (total_width, total_height), (0, 0, 0, 0))
        
        # Paste results
        y_offset = 0
        for img in results:
            combined.paste(img, (0, y_offset))
            y_offset += img.size[1]
            
        return combined
        
    def save_result(self, image: Image.Image, output_path: Union[str, Path], format: str):
        """Save the result in the specified format."""
        output_path = Path(output_path)
        
        try:
            if format in ("png", "jpg"):
                # Prepare image for saving
                if image.mode != "RGB":
                    image = image.convert("RGB")
                    
                # Apply optimization if needed
                if self.config.optimize and format == "png":
                    image = image.quantize(colors=256)
                    
                # Save with format-specific options
                save_opts = {
                    "png": {"format": "PNG", "compress_level": 9},
                    "jpg": {"format": "JPEG", "quality": 95}
                }
                
                image.save(output_path.with_suffix(f".{format}"), **save_opts[format])
                
            elif format == "txt":
                # Save as text file
                char_map = self._create_character_map(image)
                with open(output_path.with_suffix(".txt"), "w") as f:
                    f.write("\n".join(" ".join(row) for row in char_map))
                    
        except Exception as e:
            logger.error(f"Error saving result as {format}: {e}")
            raise