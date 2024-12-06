"""Image to character art conversion package."""

import logging
from pathlib import Path
from typing import List, Union

from .core import CharacterConverter, ConversionConfig
from .ranking import CharacterRanking
from .cli import main as cli_main

__version__ = "1.0.0"

# Configure package-level logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

def convert_image(
    image_path: Union[str, Path],
    output_path: Union[str, Path],
    character_set: str = "ascii",
    detail_level: int = 12,
    complexity: int = 12,
    color_mode: bool = False,
    subdivide: bool = False,
    optimize: bool = False,
    empty_char: bool = False,
    output_formats: List[str] = None,
    font_path: Union[str, Path] = None
) -> Path:
    """Convert an image to character art.
    
    This is the main entry point for programmatic use of the package.
    
    Args:
        image_path: Path to input image
        output_path: Path for output file(s)
        character_set: Type of characters to use ("ascii", "emoji", etc.)
        detail_level: Character size in pixels
        complexity: Number of different characters to use
        color_mode: Whether to preserve colors
        subdivide: Whether to subdivide large images
        optimize: Whether to optimize output files
        empty_char: Whether to include empty character
        output_formats: List of output formats ("png", "jpg", "txt")
        font_path: Optional custom font path
        
    Returns:
        Path to the output file
        
    Raises:
        ValueError: If parameters are invalid
        FileNotFoundError: If input file or font not found
        RuntimeError: If conversion fails
    """
    # Set default output format
    if output_formats is None:
        output_formats = ["png"]
        
    # Validate paths
    image_path = Path(image_path)
    output_path = Path(output_path)
    
    if not image_path.exists():
        raise FileNotFoundError(f"Input image not found: {image_path}")
        
    # Determine font path if not provided
    if font_path is None:
        font_mapping = {
            "ascii": "arial.ttf",
            "arabic": "arial.ttf",
            "braille": "seguisym.ttf",
            "emoji": "seguiemj.ttf",
            "chinese": "msyh.ttc",
            "simple": "arial.ttf",
            "numbers+": "arial.ttf",
            "roman": "times.ttf",
            "numbers": "arial.ttf",
            "latin": "arial.ttf",
            "hiragana": "msyh.ttc",
            "katakana": "msyh.ttc",
            "kanji": "msyh.ttc",
            "cyrillic": "arial.ttf",
            "hangul": "malgunbd.ttf",
        }
        
        font_name = font_mapping.get(character_set)
        if not font_name:
            raise ValueError(f"Invalid character set: {character_set}")
            
        # Search for font in system locations
        system_font_paths = [
            Path("C:/Windows/Fonts"),
            Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
            Path("/usr/share/fonts"),
            Path("/System/Library/Fonts"),
        ]
        
        for path in system_font_paths:
            if path.exists():
                potential_path = path / font_name
                if potential_path.exists():
                    font_path = potential_path
                    break
                    
        if not font_path:
            raise FileNotFoundError(f"Required font not found: {font_name}")
    else:
        font_path = Path(font_path)
        if not font_path.exists():
            raise FileNotFoundError(f"Font not found: {font_path}")
            
    # Create configuration
    config = ConversionConfig(
        detail_level=detail_level,
        font_path=font_path,
        character_set=character_set,
        color_mode=color_mode,
        subdivide=subdivide,
        optimize=optimize,
        empty_char=empty_char,
        output_formats=output_formats
    )
    
    # Initialize ranking system
    ranking = CharacterRanking(
        font_path=font_path,
        detail_level=detail_level,
        list_size=complexity
    )
    
    # Create converter
    converter = CharacterConverter(config)
    
    try:
        # Initialize character set
        char_ranking = ranking.create_ranking(include_empty=empty_char)
        converter._character_ranking = [char for char, _ in char_ranking]
        converter._char_images = ranking.create_char_images(
            converter._character_ranking,
            color_mode=color_mode
        )
        
        # Convert image
        result = converter.convert_image(image_path)
        
        # Save results
        output_files = []
        for fmt in output_formats:
            out_path = output_path.with_suffix(f".{fmt}")
            converter.save_result(result, out_path, fmt)
            output_files.append(out_path)
            
        # Return path to first output file
        return output_files[0]
        
    except Exception as e:
        raise RuntimeError(f"Failed to convert image: {e}") from e

# Expose main classes and functions
__all__ = [
    "convert_image",
    "CharacterConverter",
    "ConversionConfig",
    "CharacterRanking",
    "cli_main",
]