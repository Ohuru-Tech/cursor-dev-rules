# Cursor Dev Rules

A CLI tool to fetch and install Cursor dev rules into your project. This tool helps you quickly set up standardized development rules for various frameworks and technologies in your Cursor IDE workspace.

## Features

- 🚀 Quick installation of pre-configured Cursor dev rules
- 📦 Support for multiple frameworks (Django, FastAPI, Next.js, and more)
- 🎯 Category-based organization (backend/frontend)
- ✨ Automatic directory structure creation
- 🔄 Overwrites existing rules to keep them up-to-date

## Installation

### Using pip

```bash
pip install cursor-dev-rules
```

### Using uv

```bash
uv pip install cursor-dev-rules
```

### Development Installation

```bash
git clone https://github.com/yourusername/cursor-dev-rules.git
cd cursor-dev-rules
pip install -e ".[dev]"
```

## Quick Start

1. Navigate to your project directory:

   ```bash
   cd /path/to/your/project
   ```

2. Fetch rules for your framework:

   ```bash
   cursor-dev-rules fetch backend/django
   ```

3. The rules will be installed in `.cursor/rules/` directory:
   - General rules: `.cursor/rules/general/RULE.md`
   - Framework-specific rules: `.cursor/rules/code-patterns/RULE.md`

## Usage

### Basic Usage

```bash
cursor-dev-rules fetch <category>/<framework>
```

### Examples

**Backend Frameworks:**

```bash
# Django
cursor-dev-rules fetch backend/django

# FastAPI
cursor-dev-rules fetch backend/fastapi
```

**Frontend Frameworks:**

```bash
# Next.js
cursor-dev-rules fetch frontend/nextjs
```

### Command Options

- `--version`: Show the version number
- `--help`: Show help message

## Available Rules

### Backend Rules

- **backend/django** - Django REST Framework development standards and best practices
- **backend/fastapi** - FastAPI development standards and best practices
- **backend/general** - General backend development rules (automatically included)

### Frontend Rules

- **frontend/nextjs** - Next.js development standards and best practices
- **frontend/general** - General frontend development rules (automatically included)

## Project Structure

After running `fetch`, your project will have the following structure:

```text
your-project/
├── .cursor/
│   └── rules/
│       ├── general/
│       │   └── RULE.md          # General category rules
│       └── code-patterns/
│           └── RULE.md          # Framework-specific rules
└── ...
```

## How It Works

1. The tool locates the bundled rules from the installed package
2. It validates that both general and framework-specific rules exist
3. It creates the `.cursor/rules` directory structure if it doesn't exist
4. It copies the general rule to `.cursor/rules/general/RULE.md`
5. It copies the framework-specific rule to `.cursor/rules/code-patterns/RULE.md`

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=cursor_dev_rules --cov-report=html
```

### Repository Structure

```text
cursor-dev-rules/
├── cursor_dev_rules/
│   ├── __init__.py
│   ├── cli.py              # Main CLI implementation
│   └── rules/              # Bundled rules
│       ├── backend/
│       │   ├── django/
│       │   ├── fastapi/
│       │   └── general/
│       └── frontend/
│           ├── nextjs/
│           └── general/
├── tests/                  # Test suite
│   ├── test_cli.py
│   ├── test_utils.py
│   └── conftest.py
├── pyproject.toml
└── README.md
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Here are some ways you can contribute:

1. **Add new framework rules** - Create new rule files in the `cursor_dev_rules/rules/` directory
2. **Improve existing rules** - Update and enhance current rule files
3. **Bug fixes** - Report and fix bugs
4. **Documentation** - Improve documentation and examples
5. **Tests** - Add more test coverage

### Adding New Rules

1. Create a new directory under `cursor_dev_rules/rules/<category>/<framework>/`
2. Add a `RULE.md` file with your rules
3. Update this README to include the new framework
4. Add tests for the new rule path
5. Submit a Pull Request

## Requirements

- Python >= 3.11
- Click >= 8.1.0
- Rich >= 13.0.0

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed list of changes.
