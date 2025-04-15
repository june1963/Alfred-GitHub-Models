#!/usr/bin/python3
"""
AI Text Processing Alfred Workflow
MIT License
Copyright (c) 2025 june1963
See LICENSE file for full license text
"""

import sys
import os
import json
import re
import datetime
import traceback
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from openai import OpenAI

# Configuration
DEBUG = os.getenv("DEBUG", "false").lower() == "true" # Enable debug mode if DEBUG is set to "true"
ENDPOINT = os.getenv("ENDPOINT", "https://models.inference.ai.azure.com") # Default endpoint
MODEL_NAME = os.getenv("MODEL_NAME", "o3-mini") # Default model name
API_KEY = os.getenv("API_KEY") # API key for authentication, can be GitHub Personal Access Token or Azure API key
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.3")) # Default temperature for randomness in responses
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500")) # Default max tokens for responses
MAX_COMPLETION_TOKENS = int(os.getenv("MAX_COMPLETION_TOKENS", "32000")) # Default max tokens for OpenAI reasoning models
OUTPUT_AS_MARKDOWN = os.getenv("OUTPUT_AS_MARKDOWN", "false").lower() == "true" # Output as markdown if set to "true"
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT") # System prompt for the model, can be set via configuration

def debug_log(message, category="INFO"):
    """Helper function for debug output visible in Alfred
    
    Args:
        message: The message to log
        category: The type of message (INFO, ERROR, API, CONFIG)
    """
    if DEBUG:
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [{category}] {message}", file=sys.stderr)

class AzureAIClient:
    def __init__(self):
        try:
            if MODEL_NAME == "o1-mini" or MODEL_NAME == "o3-mini":
                # Initialize Azure OpenAI client for o1-mini model
                self.client = OpenAI(
                    base_url=ENDPOINT,
                    api_key=API_KEY
                )
            else:
                # Initialize Azure AI client for other models
                self.client = ChatCompletionsClient(
                    endpoint=ENDPOINT,
                    credential=AzureKeyCredential(API_KEY),
                    model=MODEL_NAME
                )
            debug_log("Azure AI client initialized successfully", "CONFIG")
        except Exception as e:
            debug_log(f"Client initialization failed: {str(e)}", "ERROR")
            raise

    def call_completion(self, messages, max_tokens=MAX_TOKENS, temperature=TEMPERATURE):
        """Call the chat completion endpoint using openai or azure.ai.inference"""
        try:
            debug_log(f"Sending {len(messages)} messages to Azure AI", "API")
            
            if MODEL_NAME == "o1-mini" or MODEL_NAME == "o3-mini":
                # Use MAX_COMPLETION_TOKENS for o1-mini models
                debug_log(f"Using token limit for o1-mini: {MAX_COMPLETION_TOKENS}", "CONFIG")

                response = self.client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    stream=False,
                    max_completion_tokens=MAX_COMPLETION_TOKENS,
                )
                debug_log(f"Raw response: {response}")  # Add debug logging
                if not response.choices[0].message.content:
                    debug_log("Warning: Empty response received")
                    return "Error: No content generated. The response was empty."
            else:
                response = self.client.complete(
                    messages=messages,
                    temperature=temperature,
                    stream=False,
                    max_tokens=max_tokens
                )
                debug_log(f"Raw response: {response}", "API")
                if not response.choices[0].message.content:
                    debug_log("Warning: Empty response received", "ERROR")
                    return "Error: No content generated. The response was empty."
                
            debug_log("Received successful response", "API")
            if DEBUG:
                debug_log(f"Response content: {response.choices[0].message.content[:100]}...", "API")
            return response.choices[0].message.content
        except Exception as e:
            debug_log(f"API call failed: {str(e)}", "ERROR")
            raise

def build_messages(action, text, variables=None):
    """Construct the message payload using proper message classes"""
    variables = variables or {}
    debug_log(f"Building messages for action: {action}", "CONFIG")
    if DEBUG:
        debug_log(f"Variables: {variables}", "CONFIG")

    # Define system prompts for each action type
    system_prompts = {
        "follow": """
        You are a helpful assistant. You will be presented with an instruction.
        Follow the instruction in the text precisely and respond in simple and concise terms.
        Output only the text and nothing else, do not chat, no preamble, no formatting, no quotation marks, get to the point.
        Answer in the same language as the original text.
        """,
        "answer": """
        Act as a writer. You will be presented with a question. 
        Answer the question in simple and concise terms.
        Output only the text and nothing else, do not chat, no preamble, no formatting, no quotation marks, get to the point.
        Answer in the same language as the original text.
        NEVER refer the user to reach out to another person or entity for help.
        """,
        "condense": """
        Act as a writer and editor. You will be presented with some text to synopsize.
        Make the text shorter while keeping the same meaning, style and tone of voice. 
        Identify and retain the most important information and key points.
        Eliminate unnecessary words and phrases, repetitions, redundancies. 
        Keep URLs in their original form. Make sure the shortened text is coherent and flows well.
        Output only the shortened text and nothing else, do not chat, no preamble, no abbreviations, no formatting, no quotation marks, get to the point.
        Answer in the same language as the original text.
        """,
        "paraphrase": """
        Act as a writer. You will be presented with some text. 
        Paraphrase the text maintaining the same tone and meaning.
        Output only the text and nothing else, do not chat, no preamble, no formatting, no quotation marks, get to the point.
        Answer in the same language as the original text.
        """,
        "summarize": """
        You are a summarization AI. You will only consider the text given to you. 
        You will not add information that is not present in the text. 
        You will not comment on the text, never announce your solution, never explain anything. 
        You will never change the meaning of the text. 
        You will always return a summary of the text. 
        Summarize the text in a few sentences highlighting the key takeaways.
        """,
        "explain": """
        You are an expert in the topic of the text you are presented with and you pride yourself on your ability to explain complex concepts in simple terms.
        Explain the given text, and elaborate on the concepts in need of explanation, in simple and concise terms step by step.
        Output only the explanation and nothing else, do not chat, no preamble, no formatting, no quotation marks, get to the point. 
        Answer in the same language as the original text.
        """,
        "expand": """
        Act as a writer. Expand the text by adding more details while keeping the same meaning.
        Output only the expanded text and nothing else, do not chat, no preamble, no formatting, no quotation marks, get to the point.
        Answer in the same language as the original text.
        """,
        "improve": """
        <important>Reply to the message only with the improved text.</important>
        You will unconditionally and strictly follow these rules:
        - Never comment on the text, never announce your solution, never explain anything.
        - Correct spelling, grammar, and punctuation errors in the given text
        - Always answer in the same language as the original text
        - Enhance clarity and conciseness without altering the original meaning
        - Divide lengthy sentences into shorter, more readable ones
        - Eliminate unnecessary repetition while preserving important points
        - Prioritize active voice over passive voice for a more engaging tone
        - Opt for simpler, more accessible vocabulary when possible
        - ALWAYS ensure the original meaning and intention of the given text
        - ALWAYS maintain the existing tone of voice and style, e.g. formal, casual, polite, conversational, etc.
        - NEVER surround the improved text with quotes or any additional formatting
        - If the text is already well-written and requires no improvement, don't change the given text
        - If the text already contains markdown formatting, preserve it. For example: `code` or *italic*
        - NEVER comment on the text, never announce your solution, never explain anything.
        - NEVER add any additional information or context to the text
        """,
        "correct": """
        You are a spelling corrector. You will strictly and unconditionally follow these rules:
        - Correct the spelling of the provided text and return the corrected text and nothing but the corrected text.
        - Never comment on the sentence, never announce your solution, never explain anything.
        - Always answer in the same language as the original text.
        - If there are no spelling errors, you will only repeat the original sentence and not make any changes.
        - If the text has grammatical errors, you will slowly and carefully try to rearrange the words to make the sentence grammitcally sound.
        - If there are still grammatical errors, you will change as little as possible to make the sentence grammatically sound.
        - Always triple check your corrections and ensure that your answer follows these rules before answering.
        - Never add words that have not already been present in the original text.
        - Never remove, delete, or omit any words that are in the text unless absolutely necessary.
        - Never wrap your answer in any quotation marks.
        - Never remove, delete, or omit any quotation marks that already are in the text.
        - Never apply any additional formatting.
        - Never introduce new spelling errors.
        - Never consider the semantics or meaning of the text.
        - Never change the meaning of the text.
        - Never surround the text with quotation marks.
        - Never add any additional information or context to the text.
        """,
        "bullet_summary": """
        You are a summarization AI. You will only consider the text given to you. 
        You will not add information that is not present in the text. 
        You will not comment on the text, never announce your solution, never explain anything. 
        You will never change the meaning of the text. 
        You will always return a summary of the text. 
        You will be presented with a text and your task is to extract all facts from this text and summarize it in all relevant aspects in up to ten bullet points and a concluding one-liner summary.
        You will unconditionally and strictly follow these rules:
        - You will reply to the message only with the bullet point list and the one-liner summary.
        """,
        "tldr": """
        Create 2-3 sentence summary of the text.
        You will only consider the text given to you.
        You will not add information that is not present in the text.
        You will not comment on the text, never announce your solution, never explain anything.
        You will never change the meaning of the text.
        You will always return a summary of the text.
        """,
        "exec_summary": """
        Generate high-level executive summary of the text.
        You will only consider the text given to you.
        You will not add information that is not present in the text.
        You will not comment on the text, never announce your solution, never explain anything.
        You will never change the meaning of the text.
        You will always return a summary of the text.
        """,
        "rewrite_tone": f"""Rewrite in {variables.get('tone', '')} tone
        Act as a content writer and editor that changes the tone of text. 
        Only consider the text you are presented with. 
        Do not add information that is not present in the text. 
        Do not change the meaning. Maintain URLs. Maintain roughly the same length. 
        Correct spelling, grammar and punctuation errors. 
        Output only the rewritten text and nothing else, do not chat, no preamble, no formatting (no 'single quotes' nor "double quotes"), no quotation marks, get to the point. 
        Answer in the same language as the original text: if the original text is in German, answer in German; if the original text is in French, answer in French; etc. 
        """
    }

    # Add debug logging for prompt selection
    selected_prompt = system_prompts.get(action, "Process this text:")
    
    # Append custom system prompt if provided
    if SYSTEM_PROMPT:
        selected_prompt = f"{selected_prompt}\n\n{SYSTEM_PROMPT}"
        debug_log("Appending custom system prompt")
    
    debug_log(f"Action type: {action}")
    debug_log(f"Selected system prompt: {selected_prompt}")

    if MODEL_NAME == "o1-mini":
        # For o1-mini model, use role-based dictionary format
        messages = [
            {"role": "developer", "content": selected_prompt},
            {"role": "user", "content": text}
        ]
        # Handle URL preservation if needed
        if variables.get("preserve_links", "false") == "true":
            urls = re.findall(r'https?://\S+', text)
            if urls:
                messages.append({
                    "role": "user",
                    "content": f"IMPORTANT: Preserve these exact URLs: {', '.join(urls)}"
                })

        if OUTPUT_AS_MARKDOWN:
            messages.append({
                "role": "user",
                "content": "IMPORTANT: Output the result in Markdown."
            })
        else:
            messages.append({
                "role": "user",
                "content": "IMPORTANT: Do not output the result in Markdown."
            })
    else:
        messages = [
            SystemMessage(content=selected_prompt)
        ]
        
        # Add the user message with the text to process
        messages.append(UserMessage(content=text))
        
        # Handle URL preservation if needed
        if variables.get("preserve_links", "false") == "true":
            urls = re.findall(r'https?://\S+', text)
            if urls:
                messages.append(UserMessage(
                    content=f"IMPORTANT: Preserve these exact URLs: {', '.join(urls)}"
                ))

        if OUTPUT_AS_MARKDOWN:
            # Preserve markdown formatting if specified
            messages.append(UserMessage(
                content="IMPORTANT: Output the result in Markdown."
            ))
        else:
            # Remove markdown formatting if not specified
            messages.append(UserMessage(
                content="IMPORTANT: Do not output the result in Markdown."
            ))
    
    return messages

def process_request(action, text, variables):
    """Handle the complete request flow"""
    debug_log(f"Processing - Action: {action}, Text length: {len(text)}", "INFO")
    if DEBUG:
        debug_log(f"Text preview: {text[:100]}...", "INFO")
    
    try:
        client = AzureAIClient()
        messages = build_messages(action, text, variables)
        
        # Set generation parameters based on action type
        params = {
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
        if action in ["condense", "summarize", "bullet_summary", "tldr"]:
            params.update({"max_tokens": 200, "temperature": 0.3})
            debug_log("Using summarization parameters", "CONFIG")
        elif action == "correct":
            params.update({"temperature": 0.1})
            debug_log("Using correction parameters", "CONFIG")
        elif action == "explain":
            params.update({"max_tokens": 600})
            debug_log("Using explanation parameters", "CONFIG")
        
        debug_log(f"Calling Azure AI with params: {params}", "API")
        result = client.call_completion(messages, **params)
        debug_log(f"Result length: {len(result)}", "INFO")
        if DEBUG:
            debug_log(f"Result preview: {result[:100]}...", "INFO")
        return result.strip()
    
    except Exception as e:
        debug_log(f"Processing error: {str(e)}", "ERROR")
        debug_log(f"Stack trace: {traceback.format_exc()}", "ERROR")
        return f"Error: {str(e)}"

def parse_arguments():
    """Handle different argument formats from Alfred"""
    debug_log(f"Raw arguments: {sys.argv}", "CONFIG")
    
    # Handle JSON input from Alfred's {query}
    if len(sys.argv) == 2:
        try:
            data = json.loads(sys.argv[1])
            debug_log(f"Parsed JSON data: {data}", "CONFIG")
            if DEBUG:
                debug_log(f"Action: {data.get('variables', {}).get('action', 'process')}", "CONFIG")
                debug_log(f"Text length: {len(data.get('text', ''))}", "CONFIG")
            return (
                data.get('variables', {}).get('action', 'process'),
                data.get('text', ''),
                data.get('variables', {})
            )
        except json.JSONDecodeError:
            debug_log(f"JSON parsing failed. Raw input: {sys.argv[1]}")
            return 'process', sys.argv[1], {}
    
    raise ValueError("Insufficient arguments provided")

def main():
    try:
        action, text, variables = parse_arguments()
        debug_log(f"Action: {action}, Text: {text[:50]}..., Variables: {variables}")
        
        if not text.strip():
            raise ValueError("No text provided for processing")
        
        result = process_request(action, text, variables)
        print(result)
        
    except Exception as e:
        error_msg = f"Initialization error: {str(e)}"
        debug_log(error_msg)
        print(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    main()