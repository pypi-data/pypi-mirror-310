# img-characterize

A powerful Python tool for converting images into artistic character-based representations, supporting multiple character sets and output formats.

## Features

- **Multiple Character Sets**: Support for ASCII, Arabic, Braille, Emoji, Chinese, Roman, Latin, Hiragana, Katakana, Kanji, Cyrillic, and Hangul
- **Color Support**: Option to preserve original image colors
- **Multiple Output Formats**: PNG, JPG, and TXT output formats
- **Parallel Processing**: Efficient processing of multiple images
- **Large Image Support**: Automatic division of large images
- **Customizable**: Adjustable character resolution and complexity levels

## Installation

```bash
pip install img-characterize
```

## Quick Start

Basic usage:
```bash
characterize -i image.jpg -cr 1000 -cl 12 -f png txt
```

With color preservation:
```bash
characterize -i image.jpg -cr 1000 -cl 12 -f png -c
```

Process multiple images:
```bash
characterize -i image1.jpg image2.png -cr 1000 -cl 12 -f png txt
```

## Command Line Arguments

| Argument | Description | Values |
|----------|-------------|---------|
| `-i, --i` | Input file paths | One or more image paths |
| `-cr, --cr` | Character resolution | 1 to 4000 |
| `-cl, --cl` | Complexity level | 1 to 40 |
| `-l, --l` | Character set | ascii, arabic, braille, emoji, chinese, simple, numbers+, roman, numbers, latin, hiragana, katakana, kanji, cyrillic, hangul |
| `-d, --d` | Divide large images | true/false |
| `-c, --c` | Preserve colors | true/false |
| `-f, --f` | Output formats | png, jpg, txt |
| `-ec, --ec` | Include empty character | true/false |
| `-o, --o` | Optimize output files | true/false |
| `-tk, --tk` | Use GUI file selection | true/false |
| `-v, --v` | Enable verbose logging | true/false |

## Examples

1. Create ASCII art with color:
```bash
characterize -i photo.jpg -l ascii -c true -f png
```

2. Generate Kanji art in black and white:
```bash
characterize -i artwork.png -l kanji -cr 2000 -cl 20 -f png txt
```

3. Process multiple images with emoji characters:
```bash
characterize -i pic1.jpg pic2.jpg -l emoji -cr 1500 -cl 15 -f png
```

## Output

The program creates output files in your specified format(s):
- PNG/JPG: Character-based image representation
- TXT: Plain text representation using the selected characters

Output files are saved in the `output` directory with the same base name as the input file.

## Performance Tips

1. For large images:
   - Use the `-d` flag to enable automatic image division
   - Lower the character resolution (`-cr`) for faster processing

2. For batch processing:
   - The program automatically uses parallel processing
   - Consider using lower complexity levels for faster results

## Requirements

- Python 3.8 or higher
- Required packages are automatically installed with pip

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Augusto Rehfeldt

## Acknowledgments

Thanks to all contributors and users who help improve this tool.
