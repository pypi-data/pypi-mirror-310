# Characterize

Convert images to character art with support for multiple character sets and formats.

## Features

- Multiple character sets (ASCII, Emoji, Chinese, etc.)
- Color and black/white modes
- Multiple output formats (PNG, JPG, TXT)
- Batch processing support
- Automatic character selection based on brightness
- GUI interface for easy use
- Command-line interface for automation
- Image optimization capabilities
- Large image subdivision support

## Installation

```bash
pip install characterize
```

## Quick Start

### Command Line

Convert a single image:
```bash
characterize -i image.jpg -s ascii
```

Convert multiple images:
```bash
characterize -i image1.jpg image2.png -s emoji --color
```

Convert all images in a directory:
```bash
characterize -i ./images/ -s chinese --color --optimize
```

### Python API

```python
from characterize import convert_image

# Simple conversion
output_path = convert_image(
    "input.jpg",
    "output",
    character_set="ascii"
)

# Advanced options
output_path = convert_image(
    "input.jpg",
    "output",
    character_set="emoji",
    detail_level=15,
    complexity=20,
    color_mode=True,
    subdivide=True,
    optimize=True,
    empty_char=True,
    output_formats=["png", "txt"]
)
```

## Command Line Options

- `-i, --input`: Input image files or directories
- `-s, --character-set`: Character set to use (default: ascii)
  - Available sets: ascii, arabic, braille, chinese, cyrillic, emoji, hangul, hiragana, katakana, kanji, latin, numbers, numbers+, roman, simple
- `-d, --detail-level`: Detail level (character size in pixels, default: 12)
- `-c, --complexity`: Number of different characters to use (default: 12)
- `--color`: Enable color output
- `--subdivide`: Subdivide large images
- `--optimize`: Optimize output files
- `--empty-char`: Include empty character for darker areas
- `-f, --formats`: Output formats (png, jpg, txt)

## Character Sets

Each character set has different characteristics suitable for different types of images:

- `ascii`: Good for general use, wide brightness range (2-81)
- `emoji`: Best for color images, largest brightness range (31-173)
- `chinese`: Excellent detail, wide range (0-107)
- `braille`: Compact representation, small range (3-18)
- `numbers`: Clean look, moderate range (21-43)
- `roman`: Serif style, good contrast (27-81)

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/kodu-ai/characterize.git
cd characterize
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/
```

### Building Documentation

```bash
cd docs
make html
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- PIL/Pillow for image processing
- NumPy for numerical operations
- The open-source community for font resources

## Troubleshooting

### Common Issues

1. **Font Not Found**
   - Ensure required system fonts are installed
   - Use custom fonts by specifying font_path

2. **Memory Issues**
   - Use --subdivide for large images
   - Reduce detail_level for faster processing

3. **Quality Issues**
   - Adjust complexity for more/fewer characters
   - Try different character sets
   - Enable color mode for color-rich images

### Error Messages

- "Font not found": Install required system fonts
- "Image too large": Use --subdivide option
- "Invalid character set": Check available sets

## Support

- GitHub Issues: Bug reports and feature requests
- Documentation: Full API reference and examples
- Email: support@kodu.ai

## Roadmap

- Additional character sets
- Custom character set support
- Animation support
- Web interface
- Cloud processing support