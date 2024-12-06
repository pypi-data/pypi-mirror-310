"""Command line interface for image characterization."""

import argparse
import logging
import sys
from pathlib import Path
from typing import List, Optional
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from .core import CharacterConverter, ConversionConfig
from .ranking import CharacterRanking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class CLIConfig:
    """Configuration for CLI operation."""
    input_paths: List[Path]
    character_set: str
    detail_level: int
    complexity: int
    color_mode: bool
    subdivide: bool
    optimize: bool
    empty_char: bool
    output_formats: List[str]
    output_dir: Path
    font_path: Path
    use_gui: bool = False

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> 'CLIConfig':
        """Create configuration from parsed arguments."""
        # Validate and process input paths
        input_paths = []
        for path_str in args.input:
            path = Path(path_str)
            if path.is_dir():
                input_paths.extend(
                    p for p in path.rglob("*")
                    if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
                )
            elif path.is_file() and path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
                input_paths.append(path)
                
        if not input_paths:
            raise ValueError("No valid input images found")
            
        # Determine font path based on character set
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
        
        font_name = font_mapping.get(args.character_set)
        if not font_name:
            raise ValueError(f"Invalid character set: {args.character_set}")
            
        # Try to find font in system locations
        system_font_paths = [
            Path("C:/Windows/Fonts"),
            Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
            Path("/usr/share/fonts"),
            Path("/System/Library/Fonts"),
        ]
        
        font_path = None
        for path in system_font_paths:
            if path.exists():
                potential_path = path / font_name
                if potential_path.exists():
                    font_path = potential_path
                    break
                    
        if not font_path:
            raise FileNotFoundError(f"Required font not found: {font_name}")
            
        # Create output directory
        output_dir = Path("output") / args.character_set
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if "txt" in args.formats:
            (output_dir / "text").mkdir(exist_ok=True)
            
        return cls(
            input_paths=input_paths,
            character_set=args.character_set,
            detail_level=args.detail_level,
            complexity=args.complexity,
            color_mode=args.color,
            subdivide=args.subdivide,
            optimize=args.optimize,
            empty_char=args.empty_char,
            output_formats=args.formats,
            output_dir=output_dir,
            font_path=font_path,
            use_gui=args.gui
        )

def process_image(
    image_path: Path,
    config: CLIConfig,
    converter: Optional[CharacterConverter] = None
) -> tuple[Path, float, Optional[Path]]:
    """Process a single image."""
    start_time = time.time()
    
    try:
        # Create converter if not provided
        if converter is None:
            conv_config = ConversionConfig(
                detail_level=config.detail_level,
                font_path=config.font_path,
                character_set=config.character_set,
                color_mode=config.color_mode,
                subdivide=config.subdivide,
                optimize=config.optimize,
                empty_char=config.empty_char,
                output_formats=config.output_formats
            )
            
            # Initialize ranking system
            ranking = CharacterRanking(
                font_path=config.font_path,
                detail_level=config.detail_level,
                list_size=config.complexity
            )
            
            # Create converter
            converter = CharacterConverter(conv_config)
            
            # Initialize character set
            char_ranking = ranking.create_ranking(include_empty=config.empty_char)
            converter._character_ranking = [char for char, _ in char_ranking]
            converter._char_images = ranking.create_char_images(
                converter._character_ranking,
                color_mode=config.color_mode
            )
            
        # Convert image
        result = converter.convert_image(image_path)
        
        # Save results
        output_path = None
        for fmt in config.output_formats:
            out_path = config.output_dir
            if fmt == "txt":
                out_path = out_path / "text"
            out_path = out_path / image_path.stem
            converter.save_result(result, out_path, fmt)
            output_path = out_path.with_suffix(f".{fmt}")
            
        elapsed = time.time() - start_time
        return image_path, elapsed, output_path
        
    except Exception as e:
        logger.error(f"Failed to process {image_path}: {e}")
        return image_path, time.time() - start_time, None

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description="Convert images to character art")
    
    parser.add_argument(
        "-i", "--input",
        nargs="+",
        required=True,
        help="Input image files or directories"
    )
    
    parser.add_argument(
        "-s", "--character-set",
        default="ascii",
        choices=[
            "ascii", "arabic", "braille", "chinese", "cyrillic",
            "emoji", "hangul", "hiragana", "katakana", "kanji",
            "latin", "numbers", "numbers+", "roman", "simple"
        ],
        help="Character set to use"
    )
    
    parser.add_argument(
        "-d", "--detail-level",
        type=int,
        default=12,
        help="Detail level (character size in pixels)"
    )
    
    parser.add_argument(
        "-c", "--complexity",
        type=int,
        default=12,
        help="Number of different characters to use"
    )
    
    parser.add_argument(
        "--color",
        action="store_true",
        help="Enable color output"
    )
    
    parser.add_argument(
        "--subdivide",
        action="store_true",
        help="Subdivide large images"
    )
    
    parser.add_argument(
        "--optimize",
        action="store_true",
        help="Optimize output files"
    )
    
    parser.add_argument(
        "--empty-char",
        action="store_true",
        help="Include empty character"
    )
    
    parser.add_argument(
        "-f", "--formats",
        nargs="+",
        default=["png"],
        choices=["png", "jpg", "txt"],
        help="Output formats"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Enable GUI progress reporting"
    )
    
    args = parser.parse_args()
    
    try:
        # Create configuration
        config = CLIConfig.from_args(args)
        
        # Process images
        start_time = time.time()
        total_images = len(config.input_paths)
        
        logger.info(f"Processing {total_images} images...")
        
        # Use ProcessPoolExecutor for parallel processing
        with ProcessPoolExecutor() as executor:
            futures = [
                executor.submit(process_image, path, config)
                for path in config.input_paths
            ]
            
            # Track progress
            completed = 0
            for future in futures:
                try:
                    path, elapsed, output = future.result()
                    completed += 1
                    
                    if config.use_gui:
                        # GUI progress format
                        print(f"<<{path}<<{elapsed:.2f}>>{output or ''}>>\n", flush=True)
                    else:
                        # CLI progress format
                        status = "Success" if output else "Failed"
                        logger.info(
                            f"[{completed}/{total_images}] {path.name}: {status} "
                            f"({elapsed:.2f}s)"
                        )
                        
                except Exception as e:
                    logger.error(f"Failed to get result: {e}")
                    
        total_time = time.time() - start_time
        logger.info(f"Completed in {total_time:.2f} seconds")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()