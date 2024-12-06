"""Character ranking and selection system."""

from typing import List, Tuple, Dict, Optional
import logging
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

logger = logging.getLogger(__name__)

class CharacterRanking:
    """Handles character ranking and selection based on brightness levels."""
    
    def __init__(
        self,
        font_path: Path,
        detail_level: int,
        allowed_chars: Optional[str] = None,
        list_size: int = 12
    ):
        """Initialize character ranking system.
        
        Args:
            font_path: Path to the font file
            detail_level: Size of character images in pixels
            allowed_chars: String of allowed characters, or None for default set
            list_size: Number of characters to select
        """
        self.font_path = Path(font_path)
        self.detail_level = detail_level
        self.list_size = list_size
        
        if allowed_chars is None:
            allowed_chars = (
                "0123456789"
                "abcdefghijklmnñopqrstuvwxyz"
                "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
            )
        self.allowed_chars = allowed_chars
        
        # Load font
        try:
            self.font = ImageFont.truetype(str(font_path), detail_level)
        except OSError as e:
            logger.error(f"Failed to load font {font_path}: {e}")
            raise
            
        self._brightness_cache: Dict[str, float] = {}
        self._char_image_cache: Dict[str, Image.Image] = {}
        
    def create_ranking(self, include_empty: bool = False) -> List[Tuple[str, float]]:
        """Create a ranking of characters based on brightness.
        
        Args:
            include_empty: Whether to include space character
            
        Returns:
            List of (character, brightness) tuples sorted by brightness
        """
        try:
            # Calculate brightness for all characters
            char_values = []
            for char in self.allowed_chars:
                brightness = self._get_char_brightness(char)
                char_values.append((char, brightness))
                
            # Add empty character if requested
            if include_empty:
                char_values.append((" ", 0.0))
                
            # Sort by brightness
            char_values.sort(key=lambda x: x[1])
            
            # Select optimal subset
            selected = self._select_optimal_chars(char_values)
            
            # Log statistics
            self._log_ranking_stats(selected)
            
            return selected
            
        except Exception as e:
            logger.error(f"Failed to create character ranking: {e}")
            raise
            
    def create_char_images(
        self,
        characters: List[str],
        color_mode: bool = False
    ) -> Dict[str, Image.Image]:
        """Create character images for the given characters.
        
        Args:
            characters: List of characters to create images for
            color_mode: Whether to create images for color mode
            
        Returns:
            Dictionary mapping characters to their images
        """
        try:
            images = {}
            for char in characters:
                if char in self._char_image_cache:
                    images[char] = self._char_image_cache[char]
                else:
                    img = self._create_char_image(char, color_mode)
                    self._char_image_cache[char] = img
                    images[char] = img
            return images
            
        except Exception as e:
            logger.error(f"Failed to create character images: {e}")
            raise
            
    def _get_char_brightness(self, char: str) -> float:
        """Calculate brightness value for a character."""
        if char in self._brightness_cache:
            return self._brightness_cache[char]
            
        # Handle empty character
        if char.strip() == "":
            return 0.0
            
        try:
            # Create character image
            img = Image.new("L", (self.detail_level, self.detail_level), color=0)
            draw = ImageDraw.Draw(img)
            
            # Draw character
            draw.text(
                (self.detail_level/2, self.detail_level/2),
                char,
                font=self.font,
                fill=255,
                anchor="mm"
            )
            
            # Calculate brightness
            brightness = float(np.mean(img)) / 255
            self._brightness_cache[char] = brightness
            
            return brightness
            
        except Exception as e:
            logger.error(f"Failed to calculate brightness for '{char}': {e}")
            raise
            
    def _create_char_image(self, char: str, color_mode: bool) -> Image.Image:
        """Create image for a single character."""
        try:
            # Create base image
            mode = "RGBA" if color_mode else "L"
            img = Image.new(mode, (self.detail_level, self.detail_level), 0)
            draw = ImageDraw.Draw(img)
            
            # Set fill color
            fill = (0, 0, 0, 0) if color_mode else 255
            
            # Draw character
            draw.text(
                (self.detail_level/2, self.detail_level/2),
                char,
                font=self.font,
                fill=fill,
                anchor="mm"
            )
            
            return img
            
        except Exception as e:
            logger.error(f"Failed to create image for '{char}': {e}")
            raise
            
    def _select_optimal_chars(
        self,
        char_values: List[Tuple[str, float]]
    ) -> List[Tuple[str, float]]:
        """Select optimal subset of characters for even distribution."""
        if not char_values:
            raise ValueError("Empty character list")
            
        if len(char_values) <= self.list_size:
            return char_values
            
        # Handle empty character separately
        empty_char = None
        if (" ", 0.0) in char_values:
            empty_char = (" ", 0.0)
            char_values = [c for c in char_values if c != (" ", 0.0)]
            self.list_size -= 1
            
        # Calculate target brightness values
        min_val = char_values[0][1]
        max_val = char_values[-1][1]
        step = (max_val - min_val) / (self.list_size - 1)
        targets = [min_val + i * step for i in range(self.list_size)]
        
        # Select characters closest to targets
        selected = []
        remaining = char_values.copy()
        
        for target in targets:
            closest = min(remaining, key=lambda x: abs(x[1] - target))
            selected.append(closest)
            remaining.remove(closest)
            
        # Add empty character back if needed
        if empty_char:
            selected = [empty_char] + selected
            
        return sorted(selected, key=lambda x: x[1])
        
    def _log_ranking_stats(self, ranking: List[Tuple[str, float]]):
        """Log statistics about the character ranking."""
        try:
            brightness_range = ranking[-1][1] - ranking[0][1]
            steps = [b2[1] - b1[1] for b1, b2 in zip(ranking[:-1], ranking[1:])]
            dissimilarity = np.median(steps) / brightness_range if steps else 0
            
            logger.info(
                f"Character ranking stats: "
                f"range={brightness_range:.3f}, "
                f"dissimilarity={dissimilarity:.3f}, "
                f"chars={len(ranking)}"
            )
            
        except Exception as e:
            logger.error(f"Failed to log ranking stats: {e}")