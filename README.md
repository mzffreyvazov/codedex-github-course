# Chat Analysis Tool

A Python script for analyzing chat message data and generating visualizations of chat patterns and user statistics.

## Features

- Parses chat log files with timestamps and user messages
- Filters out system messages and invalid entries
- Generates statistics about total messages and unique users
- Creates visualizations for:
  - Message activity by hour of day
  - Top contributors

## Requirements

- Python 3.x
- pandas
- matplotlib

## Setup

1. Install required dependencies:
```bash
pip install pandas matplotlib
```

2. Configure the input file path in `intellektual.py`:
```python
INPUT_FILE = "path/to/your/chat_file.txt"
```

## Usage

Run the script:
```bash
python intellektual.py
```

The script will generate:
- Basic statistics about the chat
- A bar chart showing message frequency by hour
- A horizontal bar chart showing top message contributors

## Input File Format

The chat log file should be in the following format:
```
[DD/MM/YYYY, HH:MM AM/PM] - Username: Message content
```

## License

MIT
