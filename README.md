<p align="center">
  <img src="icon.png" alt="Advanced Layer Renamer" width="128" height="128">
</p>

<h1 align="center">Advanced Layer Renamer</h1>

<p align="center">
  <strong>Professional QGIS plugin for batch renaming map layers with advanced features</strong>
</p>

<p align="center">
  <a href="https://github.com/raymukesh/advanced_layer_renamer/releases"><img src="https://img.shields.io/github/v/release/raymukesh/advanced_layer_renamer?style=flat-square" alt="Release"></a>
  <a href="https://github.com/raymukesh/advanced_layer_renamer/blob/main/LICENSE"><img src="https://img.shields.io/github/license/raymukesh/advanced_layer_renamer?style=flat-square" alt="License"></a>
  <a href="https://qgis.org"><img src="https://img.shields.io/badge/QGIS-3.0%2B-brightgreen?style=flat-square" alt="QGIS Version"></a>
  <a href="https://github.com/raymukesh/advanced_layer_renamer/issues"><img src="https://img.shields.io/github/issues/raymukesh/advanced_layer_renamer?style=flat-square" alt="Issues"></a>
</p>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#contributing">Contributing</a>
</p>

---

## Overview

**Advanced Layer Renamer** is a powerful QGIS plugin that streamlines the process of renaming multiple map layers simultaneously. Whether you're managing large GIS projects, standardizing naming conventions, or simply cleaning up layer names, this plugin provides a comprehensive set of tools to get the job done efficiently.

### Why Use Advanced Layer Renamer?

- **Save Time**: Rename hundreds of layers in seconds instead of manually editing each one
- **Maintain Consistency**: Apply standardized naming conventions across your entire project
- **Reduce Errors**: Preview all changes before applying them
- **Stay Organized**: Use templates to maintain consistent naming standards across projects

---

## Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **Batch Selection** | Select all, none, or invert selection with one click. Refresh layer list anytime |
| **Real-time Preview** | See exactly how names will change before applying |
| **Resizable Interface** | Drag to resize panels and columns for comfortable viewing |

### Numbering Options

- **Sequential Numbering**: Add simple sequential numbers (1, 2, 3...)
- **Leading Zeros**: Configurable zero-padding (01, 001, 0001, etc.) for proper sorting
- **Up to 5 Digits**: Support from 1 to 5 leading zeros (up to 999,999 layers)

### Basic Transformations

- **Prefix**: Add text to the beginning of layer names
- **Suffix**: Add text to the end of layer names
- **Find & Replace**: Simple text replacement or powerful regex pattern matching
- **Regex Support**: Full Python regex support with built-in pattern tester

### Case Conversion

| Option | Example |
|--------|---------|
| UPPERCASE | `my layer` → `MY LAYER` |
| lowercase | `My Layer` → `my layer` |
| Title Case | `my layer name` → `My Layer Name` |
| Capitalized | `my layer name` → `My layer name` |

### Advanced Options

- **Date Stamping**: Automatically add current date in multiple formats
  - `YYYYMMDD` (20240115)
  - `YYYY-MM-DD` (2024-01-15)
  - `DD-MM-YYYY` (15-01-2024)
- **Remove Special Characters**: Clean up problematic characters while preserving letters, numbers, spaces, underscores, dashes, and dots
- **Clean Whitespace**: Remove leading/trailing spaces and collapse multiple spaces

### Templates System

- **Save Templates**: Store your favorite naming configurations for reuse
- **Quick Templates**: Built-in templates for common tasks (Date Prefix, Clean Names, Project Standard)
- **Portable**: Export and share templates with colleagues via JSON file

### Validation Tools

- Check for naming issues before applying changes
- Identify potential conflicts and problems
- Preview validation results in a dedicated tab

---

## Installation

### Method 1: QGIS Plugin Manager (Recommended)

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins...**
3. Click on the **All** tab
4. Search for `Advanced Layer Renamer`
5. Click **Install Plugin**

### Method 2: Manual Installation

1. Download the latest release from the [Releases page](https://github.com/raymukesh/advanced_layer_renamer/releases)
2. In QGIS, go to **Plugins** → **Manage and Install Plugins...**
3. Click **Install from ZIP**
4. Browse to the downloaded ZIP file and click **Install Plugin**

### Method 3: From Source (Development)

```bash
# Clone the repository
git clone https://github.com/raymukesh/advanced_layer_renamer.git

# Copy or symlink to your QGIS plugins directory
# Windows: %APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\
# macOS: ~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/
# Linux: ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/
```

---

## Quick Start

### Basic Workflow

1. **Open the Plugin**
   - Go to **Plugins** → **Advanced Layer Renamer**, or
   - Click the plugin icon in the toolbar

2. **Select Layers**
   - Your project layers appear in the left panel
   - Use **Select All**, **Select None**, or **Invert** buttons
   - Or manually select with `Ctrl+Click` / `Shift+Click`

3. **Configure Renaming Options**
   - Choose numbering style
   - Add prefix/suffix
   - Set up find/replace patterns
   - Select case conversion
   - Enable advanced options as needed

4. **Preview Changes**
   - The preview table updates automatically
   - Green rows = names will change
   - Gray rows = no change

5. **Apply Changes**
   - Click **Rename Layers**
   - Review the summary dialog

### Example Transformations

| Before | After | Settings Used |
|--------|-------|---------------|
| `my layer (copy)` | `01_Project_my_layer` | Numbering + Prefix + Find/Replace |
| `DATA_2023_final` | `data_2023_final` | Lowercase |
| `untitled   layer` | `Untitled Layer` | Clean Whitespace + Title Case |
| `layer@v1#test` | `layer_v1_test` | Remove Special Characters |

---

## Transformation Order

When multiple options are enabled, transformations are applied in this order:

1. Find/Replace (with or without regex)
2. Remove Special Characters
3. Clean Whitespace
4. Add Numbering
5. Add Date Stamp
6. Add Prefix
7. Add Suffix
8. Apply Case Conversion

---

## Requirements

- **QGIS Version**: 3.0 or higher
- **Platform**: Windows, macOS, Linux
- **Dependencies**: None (uses standard QGIS/Qt libraries)

---

## Documentation

Full documentation is available in the `docs/` folder:

- [Installation Guide](docs/installation.md)
- [Getting Started](docs/getting-started.md)
- [Complete Feature Guide](docs/features.md)
- [Templates System](docs/templates.md)
- [Validation Tools](docs/validation.md)
- [FAQ](docs/faq.md)
- [Changelog](docs/changelog.md)

---

## Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs

1. Check [existing issues](https://github.com/raymukesh/advanced_layer_renamer/issues) to avoid duplicates
2. [Open a new issue](https://github.com/raymukesh/advanced_layer_renamer/issues/new) with:
   - Clear description of the problem
   - Steps to reproduce
   - QGIS version and operating system
   - Screenshots if applicable

### Suggesting Features

1. Check if the feature is already in the [roadmap](docs/changelog.md#roadmap)
2. [Open an issue](https://github.com/raymukesh/advanced_layer_renamer/issues/new) with the "enhancement" label
3. Describe your use case and desired functionality

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Roadmap

Planned features for future releases:

- [ ] Undo/redo support
- [ ] Batch rename history
- [ ] Export/import templates
- [ ] Custom numbering start value
- [ ] Numbering suffix option
- [ ] Layer type filtering (vector/raster)
- [ ] Group-aware renaming
- [ ] Regular expression builder wizard

---

## License

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

---

## Author

**Mukesh Ray**

- Email: dr.raymukesh@gmail.com
- GitHub: [@raymukesh](https://github.com/raymukesh)

---

## Acknowledgments

- Built for the QGIS community
- Icons from the Material Design icon set
- Thanks to all contributors and users who provide feedback

---

<p align="center">
  <sub>Made with care for the QGIS community</sub>
</p>

<p align="center">
  <a href="https://github.com/raymukesh/advanced_layer_renamer/issues">Report Bug</a> •
  <a href="https://github.com/raymukesh/advanced_layer_renamer/issues">Request Feature</a>
</p>
