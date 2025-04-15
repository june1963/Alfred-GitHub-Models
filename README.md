# AI Text Processing Alfred Workflow

An Alfred workflow that provides powerful AI-powered text processing capabilities using Azure AI services.

## Features

- Process text with various AI-powered actions
- Multiple processing modes:
  - Follow Instructions
  - Answer Questions
  - Condense Text
  - Paraphrase
  - Summarize
  - Explain
  - Expand
  - Improve
  - Correct Spelling
- Summary Formats:
  - Bullet Points
  - TL;DR
  - Executive Summary
- Tone Modifications:
  - Professional
  - Casual
  - Friendly
  - Diplomatic
  - Confident
  - Simple

## Requirements

- Alfred 5 with Powerpack
- Python 3.9+
  - Install `openai`, `azure-ai`, `azure-ai-inference`, and `azure-core` packages:
    ```bash
    pip install openai azure-ai azure-ai-inference azure-core
    ```
    or use the `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
- Azure AI API key or GitHub PAT with `models:read` permissions

## Installation

1. Download the latest release
2. Double click to install in Alfred

## Configuration

Set up your preferred hotkey for the workflow, e.g., `⌘+Shift+1`. You can also configure the workflow to use a specific Azure AI model by setting the `MODEL_NAME` environment variable.

The workflow supports the following environment variables:

   - `API_KEY`: Your Azure AI API key or GitHub PAT with `models:read` permissions
   - `ENDPOINT`: Your Azure AI endpoint URL
   - `MODEL_NAME`: Azure AI model name (default: "o3-mini")
   - `REQUIREMENTS`: Optional, use `requirements.txt` for package installation
   - `DEBUG`: Enable debug logging (true/false)
   - `TEMPERATURE`: Control response randomness (0.0-1.0)
   - `MAX_TOKENS`: Maximum tokens for responses
   - `OUTPUT_AS_MARKDOWN`: Output responses in markdown format (true/false)
   - `SYSTEM_PROMPT`: Optional custom system prompt

## Usage

1. Select the text you want to process
2. Activate Alfred and type your hotkey (e.g., `⌘+Shift+1`)
3. Choose the desired action from the list
4. Wait for the AI to process the text, which may take a few seconds
5. The processed text will be displayed in the active window

## License

MIT License - see [LICENSE](LICENSE) for details

## Author

Copyright (c) 2025 june1963
