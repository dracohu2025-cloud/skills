---
description: Headless browser automation for web scraping, testing, and interaction. Use when you need to browse websites, scrape dynamic content, fill forms, click buttons, take screenshots, or automate web interactions. Triggers include "browse website", "scrape page", "take screenshot", "automate browser", "extract DOM", "web scraping", "fill form", "click button".
---

# Agent Browser Skill

Headless browser automation CLI for AI agents using `agent-browser` (Vercel Labs).

## Overview

This skill provides browser automation capabilities through the `agent-browser` CLI. It uses Playwright under the hood with a Rust CLI for speed.

## Key Concepts

### Refs (Recommended for AI)

The `snapshot` command returns an accessibility tree with refs that can be used for precise element selection:

```bash
# 1. Get snapshot with refs
agent-browser snapshot -c
# Output:
# - heading "Example Domain" [ref=e1] [level=1]
# - button "Submit" [ref=e2]
# - textbox "Email" [ref=e3]

# 2. Use refs to interact
agent-browser click @e2                   # Click by ref
agent-browser fill @e3 "test@example.com" # Fill by ref
agent-browser get text @e1                # Get text by ref
```

## Common Workflows

### Basic Web Scraping

```bash
# Open page and get content
agent-browser open https://example.com
agent-browser snapshot -c              # Get accessibility tree (compact)
agent-browser get text "body"          # Get all text
agent-browser screenshot page.png      # Take screenshot
agent-browser close
```

### Form Filling

```bash
agent-browser open https://example.com/login
agent-browser snapshot -i              # Interactive elements only
agent-browser fill @e3 "user@email.com"
agent-browser fill @e4 "password123"
agent-browser click @e5                # Click submit button
agent-browser wait --url "**/dashboard"
agent-browser close
```

### Multi-Page Navigation

```bash
agent-browser open https://example.com
agent-browser click @e2                # Click a link
agent-browser wait 2000                # Wait 2 seconds
agent-browser snapshot -c
agent-browser back                     # Go back
agent-browser close
```

### Taking Screenshots

```bash
agent-browser open https://example.com
agent-browser screenshot page.png           # Viewport only
agent-browser screenshot full.png --full    # Full page
agent-browser close
```

## Command Reference

### Core Commands

| Command | Description |
|---------|-------------|
| `open <url>` | Navigate to URL |
| `click <sel>` | Click element |
| `fill <sel> <text>` | Clear and fill input |
| `type <sel> <text>` | Type into element |
| `press <key>` | Press key (Enter, Tab, etc.) |
| `hover <sel>` | Hover over element |
| `scroll <dir> [px]` | Scroll (up/down/left/right) |
| `screenshot [path]` | Take screenshot (--full for full page) |
| `snapshot` | Get accessibility tree with refs |
| `close` | Close browser |

### Snapshot Options

| Option | Description |
|--------|-------------|
| `-i, --interactive` | Only show interactive elements |
| `-c, --compact` | Remove empty structural elements |
| `-d, --depth <n>` | Limit tree depth |
| `-s, --selector <sel>` | Scope to CSS selector |

### Get Info

| Command | Description |
|---------|-------------|
| `get text <sel>` | Get text content |
| `get html <sel>` | Get innerHTML |
| `get value <sel>` | Get input value |
| `get title` | Get page title |
| `get url` | Get current URL |

### Wait Commands

| Command | Description |
|---------|-------------|
| `wait <selector>` | Wait for element visible |
| `wait <ms>` | Wait milliseconds |
| `wait --text "text"` | Wait for text to appear |
| `wait --url "pattern"` | Wait for URL pattern |

### Sessions (Multiple Browsers)

```bash
# Run isolated browser instances
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com

# List active sessions
agent-browser session list
```

## Selector Types

### Refs (Recommended)
```bash
agent-browser click @e2              # From snapshot
```

### CSS Selectors
```bash
agent-browser click "#id"
agent-browser click ".class"
agent-browser click "div > button"
```

### Text & XPath
```bash
agent-browser click "text=Submit"
agent-browser click "xpath=//button"
```

### Semantic Locators
```bash
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "test@test.com"
```

## Best Practices

1. **Always use `snapshot -c` first** to get refs before interacting
2. **Use refs (@e1, @e2)** instead of CSS selectors for reliability
3. **Add waits** after navigation or clicks that trigger page changes
4. **Use `--json` flag** for programmatic parsing of output
5. **Close browser** when done to free resources

## Troubleshooting

### Browser not starting
```bash
# Reinstall Chromium
agent-browser install
```

### Element not found
```bash
# Use snapshot to see available elements
agent-browser snapshot -c

# Wait for element to appear
agent-browser wait "#element"
```

### Timeout issues
```bash
# Increase wait time
agent-browser wait 5000
agent-browser wait --load networkidle
```
