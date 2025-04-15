#!/usr/bin/python3
"""
AI Text Processing Alfred Workflow
MIT License
Copyright (c) 2025 june1963
See LICENSE file for full license text
"""

import json
import sys
import re

def generate_alfred_items(selected_text):
    items = []
    
    # Detect if text contains URLs
    contains_links = bool(re.search(r'https?://\S+', selected_text))
    
    # Header if links detected
    if contains_links:
        items.append({
            "title": "🔗 Links Detected",
            "subtitle": "URLs will be preserved in output",
            "valid": False
        })
    
    # Core Processing Actions
    core_actions = [
        ("Follow Instruction", "Execute the selected instruction", "follow"),
        ("Answer Question", "Provide detailed answer to the question", "answer"),
        ("Condense", "Reduce length while rewriting for conciseness", "condense"),
        ("Paraphrase", "Rewrite in different words keeping same meaning", "paraphrase"),
        ("Summarize", "Create concise overview of main points", "summarize"),
        ("Explain", "Provide detailed explanation of content", "explain"),
        ("Expand", "Elaborate with more details and examples", "expand"),
        ("Improve", "Enhance clarity and flow of text", "improve"),
        ("Correct Spelling", "Fix spelling and grammar errors", "correct")
    ]
    
    # Summary Formats
    summary_formats = [
        ("Bullet Points", "Convert to concise bullet list", "bullet_summary"),
        ("TL;DR", "Very brief summary (2-3 sentences)", "tldr"),
        ("Executive Summary", "High-level overview for busy readers", "exec_summary")
    ]
    
    # Tone Modifications
    tone_modifications = [
        ("Professional Tone", "Formal business/academic style, concise and factual", "professional"),
        ("Casual Tone", "Conversational everyday language with active voice", "casual"),
        ("Friendly Tone", "Warm and approachable style, optimistic, and somewhat enthusiastic", "friendly"),
        ("Diplomatic Tone", "Tactful and politically sensitive, respectful, and considerate", "diplomatic"),
        ("Confident Tone", "Assertive, straightforward, and authoritative, avoiding apologies", "confident"),
        ("Simple Tone", "Easy-to-understand language, clear and concise", "simple")
    ]
    
    # Add core actions
    for title, subtitle, action in core_actions:
        items.append({
            "title": f"{title}",
            "subtitle": subtitle,
            "arg": json.dumps({
                "text": selected_text,
                "variables": {
                    "action": action,
                    "preserve_links": str(contains_links).lower()
                }
            })
        })
    
    # Add summary formats
    items.append({
        "title": "📋 Summary Formats",
        "subtitle": "Different ways to summarize the content",
        "valid": False
    })
    for title, subtitle, action in summary_formats:
        items.append({
            "title": f"  {title}",
            "subtitle": subtitle,
            "arg": json.dumps({
                "text": selected_text,
                "variables": {
                    "action": action,
                    "preserve_links": str(contains_links).lower()
                }
            })
        })
    
    # Add tone modifications
    items.append({
        "title": "🎭 Change Tone",
        "subtitle": "Rewrite in different styles",
        "valid": False
    })
    for title, subtitle, action in tone_modifications:
        items.append({
            "title": f"  {title}",
            "subtitle": subtitle,
            "arg": json.dumps({
                "text": selected_text,
                "variables": {
                    "action": "rewrite_tone",
                    "tone": action,
                    "preserve_links": str(contains_links).lower()
                }
            })
        })
    
    return {"items": items}

if __name__ == "__main__":
    selected_text = sys.argv[1] if len(sys.argv) > 1 else ""
    print(json.dumps(generate_alfred_items(selected_text)))