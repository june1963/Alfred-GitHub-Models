# AI Text Processing Alfred Workflow

An Alfred workflow that provides powerful AI-powered text processing capabilities using Azure AI services via GitHub Models.

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
- GitHub PAT with `models:read` permissions

## Installation

1. Download the latest release
2. Double click to install in Alfred

## Configuration

Set up your preferred hotkey for the workflow, e.g., `⌘+Shift+1`. You can also configure the workflow to use a specific model by setting the `MODEL_NAME` configuration variable.

The workflow supports the following configuration variables:

- `API_KEY`: Your GitHub PAT with `models:read` permissions
- `ENDPOINT`: Your Azure AI endpoint (default: `https://models.inference.ai.azure.com`)
- `MODEL_NAME`: Azure AI model name (default: `o3-mini`)
- `MAX_TOKENS`: Maximum tokens for responses
- `MAX_COMPLETION_TOKENS`: Maximum tokens for o1-mini and o3 mini models
- `TEMPERATURE`: Control response randomness (0.01-1.0)
- `SYSTEM_PROMPT`: Optional custom system prompt
- `OUTPUT_AS_MARKDOWN`: Output responses in Markdown format (true/false)
- `DEBUG`: Enable debug logging (true/false)

## Usage

1. Select the text you want to process
2. Activate Alfred and type your hotkey (e.g., `⌘+Shift+1`)
3. Choose the desired action from the list
4. Wait for the AI to process the text, which may take a few seconds
5. The processed text will be displayed in the active window

## License

MIT License - see [LICENSE](LICENSE) for details

## Author

Copyright (c) 2025 [june1963](https://github.com/june1963)
