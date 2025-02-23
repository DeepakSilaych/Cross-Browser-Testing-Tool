# Cross-Browser Testing Tool

A Docker-based automated tool for visual regression testing across different browsers using Playwright. The tool captures screenshots of web pages in multiple browsers, compares them for visual differences, and generates an HTML report.

## Features

- **Multi-Browser Support**: Test websites in Chromium and Firefox
- **Visual Comparison**: Automatically detect and highlight visual differences between browsers
- **HTML Reports**: Generate user-friendly reports with side-by-side comparisons
- **Docker Integration**: Run tests in an isolated, consistent environment
- **Headless Mode**: Fast, automated testing without opening browser windows

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd cross-browser-testing
   ```

2. Build the Docker image:
   ```bash
   sudo docker-compose build
   ```

## Usage

Run the testing tool using Docker Compose:

```bash
sudo docker-compose run cross-browser-test --url <website-url> --browsers <browser-list>
```

### Parameters

- `--url`: The website URL to test (required)
- `--browsers`: Comma-separated list of browsers to test (default: chromium,firefox)
- `--headless`: Run in headless mode (default: true)

### Example

```bash
sudo docker-compose run cross-browser-test --url https://example.com --browsers chromium,firefox
```

## Output

The tool generates the following files in the `results` directory:

- `{browser}.png`: Screenshots from each browser
- `diff_{browser1}_{browser2}.png`: Visual difference between browsers
- `report.html`: HTML report with side-by-side comparisons

## Project Structure

```
.
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── run_test.py            # Main testing script
├── template.html          # HTML report template
└── results/               # Test results directory
```

## Dependencies

- Python 3.11
- Playwright: Browser automation
- Pillow: Image processing and comparison
- Jinja2: HTML report generation
# Cross-Browser-Testing-Tool
