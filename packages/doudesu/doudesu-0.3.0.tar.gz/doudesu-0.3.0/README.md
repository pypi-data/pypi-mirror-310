# Dodesu

A powerful manga downloader and Python wrapper for doujindesu.tv with both CLI and GUI interfaces.

![Python Version](https://img.shields.io/pypi/pyversions/dodesu)
![License](https://img.shields.io/pypi/l/dodesu)
![PyPI Version](https://img.shields.io/pypi/v/dodesu)
![Downloads](https://img.shields.io/pypi/dm/dodesu)

## Features

- 🔍 Search manga by title
- 📱 Modern GUI interface using Flet
- 💻 Feature-rich CLI interface
- 📖 Download single or multiple chapters
- 📑 Automatic PDF conversion
- 🌙 Dark/Light theme support
- 🎨 Beautiful and intuitive interface

## Installation

### Basic Installation
```bash
pip install dodesu
# or using uv
uv pip install dodesu
```

### With GUI Support
> [!NOTE]
> GUI support requires `flet` to be installed.
> I just tested it on Windows, so idk if it works on Linux or MacOS. just let me know if it does.
```bash
pip install dodesu[gui]
# or using uv
uv pip install "dodesu[gui]"
```

## Command-Line Usage

### Available Commands
```bash
# Launch GUI interface
python -m dodesu --gui

# Launch interactive CLI interface
python -m dodesu --interactive

# Search manga by keyword
python -m dodesu --search "manga name"

# Download manga directly by URL
python -m dodesu --url "https://doujindesu.tv/manga/your-manga-url"

# Show help message
python -m dodesu --help
```

### Command Options
```
Options:
  --gui          Run in GUI mode (requires dodesu[gui] installation)
  --search TEXT  Search manga by keyword
  --url TEXT     Download manga by URL
  --interactive  Run in interactive CLI mode
```

### Examples
```bash
# Search for a manga
python -m dodesu --search "manga title"

# Download manga from URL
python -m dodesu --url "https://doujindesu.tv/manga/example"

# Launch GUI interface
python -m dodesu --gui

# Start interactive CLI mode
python -m dodesu --interactive
```

### GUI Mode
```bash
python -m dodesu --gui
```

### CLI Features

- 🎨 Colorful and intuitive interface
- 📄 Detailed manga information
- 📚 Chapter selection options:
  - Download all chapters
  - Download specific chapter
  - Download range of chapters
- 🔄 Pagination support for search results
- ✨ Progress indicators
- 🎯 Smart single-chapter handling

### GUI Features

- 🎨 Modern and responsive design
- 🌓 Dark/Light theme toggle
- 📱 Mobile-friendly layout
- 🖼️ Thumbnail previews
- 📊 Download progress tracking
- 🔍 Advanced search capabilities

## Python API Usage

```python
from dodesu import Doujindesu

# Search for manga
results = Doujindesu.search("manga name")
for manga in results.results:
    print(f"Title: {manga.name}")
    print(f"URL: {manga.url}")

# Download manga
manga = Doujindesu("manga_url")
details = manga.get_details()
chapters = manga.get_all_chapters()

# Get chapter images
manga.url = chapters[0]  # Set to specific chapter
images = manga.get_all_images()
```

## Configuration

Downloaded files are saved in the `result` directory by default.

## Dependencies

- beautifulsoup4 >= 4.9.3
- tls-client >= 0.2.1
- rich >= 10.0.0
- Pillow >= 8.0.0
- reportlab >= 4.0.0
- pydantic >= 2.0.0
- flet >= 0.7.0 (GUI only)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
