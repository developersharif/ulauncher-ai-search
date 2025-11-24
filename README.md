# AI & Custom Search - Ulauncher Extension

A flexible Ulauncher extension that enables searching multiple AI services and custom web engines with dynamic syntax.

## Features

- **Default Search Mode**: Use `ai <query>` to search with your default engine
- **Specific Engine Mode**: Use `ai:<engine_id> <query>` (or `ai <engine_id>: <query>`) to search with a specific engine
- **Fully Configurable**: Add unlimited custom search engines via JSON configuration
- **Flexible Keyword**: Customize the trigger keyword to any word, phrase, or character (e.g., `ai`, `ask`, `?`)

## Installation

1. Clone this repository to your Ulauncher extensions directory:
   ```bash
   mkdir -p ~/.local/share/ulauncher/extensions
   cd ~/.local/share/ulauncher/extensions
   git clone https://github.com/yourusername/ulauncher-ai-search.git com.github.ulauncher.ai-search
   ```

2. Restart Ulauncher:
   ```bash
   pkill ulauncher && ulauncher &
   ```

3. Configure the extension in Ulauncher Preferences → Extensions

## Configuration

### Default Settings

- **Keyword**: `ai`
- **Default Engine**: `googleai` (Google AI Mode)
- **Engines Config**: JSON array of search engines

### Default Engines

The extension comes pre-configured with:
- **Google AI Mode** (`googleai`): Google Search with AI Overviews enabled
- **ChatGPT** (`chatgpt`): Opens ChatGPT with pre-filled prompt
- **Perplexity** (`perplexity`): AI-powered search engine
- **Google Search** (`google`): Standard Google Search
- **DuckDuckGo** (`duckduckgo`): Privacy-focused search

### Adding Custom Engines

Edit the `engines_config` preference with valid JSON.

```json
[
  {
    "id": "perplexity",
    "name": "Perplexity AI",
    "url_template": "https://www.perplexity.ai/search?q=%s",
    "icon": "fa-search"
  },
  {
    "id": "custom",
    "name": "My Custom Engine",
    "url_template": "https://example.com/search?q=%s",
    "icon": "fa-search"
  }
]
```

## Usage

### Default Search
```
ai What is quantum computing?
```
Opens the query in the default engine (Google AI Mode).

### Specific Engine Search
```
ai:chatgpt Write a python script
```
OR
```
ai chatgpt: Write a python script
```
Opens the query in ChatGPT.

### Engine Discovery
Type `ai:` or `ai` to see available engines and options.

## Requirements

- Ulauncher 5.x or later
- Python 3.6+

## License

MIT License

