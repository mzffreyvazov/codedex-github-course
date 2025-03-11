import pandas as pd
import matplotlib.pyplot as plt
import re
from datetime import datetime

# ------ Configuration ------
INPUT_FILE = r"C:\Users\muzaf\python scripts\chat_analyss\intellektual_chat.txt"
DATE_FORMAT = "%d/%m/%Y, %I:%M %p"  # Note the narrow no-break space (U+202F)
SYSTEM_INDICATOR = "~ "

# ------ Custom Parser ------
def parse_chat(file_path):
    messages = []
    current_message = None
    pattern = re.compile(r'^\[(\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2} [ap]m)\] - (.*)')

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            match = pattern.match(line)
            if match:
                if current_message:
                    messages.append(current_message)
                
                timestamp_str, remainder = match.groups()
                
                # Parse timestamp
                try:
                    timestamp = datetime.strptime(timestamp_str, DATE_FORMAT)
                except ValueError as e:
                    print(f"Failed to parse timestamp: {timestamp_str}")
                    continue

                # Split user and message
                if SYSTEM_INDICATOR in remainder:
                    user, message = remainder.split(SYSTEM_INDICATOR, 1)
                    is_system = True
                elif ": " in remainder:
                    user, message = remainder.split(": ", 1)
                    is_system = False
                else:
                    # Handle messages without user (system notifications)
                    messages.append({
                        'timestamp': timestamp,
                        'user': 'System',
                        'message': remainder,
                        'is_system': True,
                        'hour': timestamp.hour,
                        'day_of_week': timestamp.strftime('%A')
                    })
                    continue

                current_message = {
                    'timestamp': timestamp,
                    'user': user.strip(),
                    'message': message.strip(),
                    'is_system': is_system,
                    'hour': timestamp.hour,
                    'day_of_week': timestamp.strftime('%A')
                }
            else:
                if current_message:
                    current_message['message'] += '\n' + line
                else:
                    messages.append({
                        'timestamp': None,
                        'user': 'System',
                        'message': line,
                        'is_system': True,
                        'hour': None,
                        'day_of_week': None
                    })

    if current_message:
        messages.append(current_message)
    
    return pd.DataFrame(messages)

# ------ Data Processing ------
df = parse_chat(INPUT_FILE)

# Filter out system messages and invalid entries
valid_messages = df[
    (df['is_system'] == False) &
    (df['user'].notna()) &
    (df['message'].notna())
]

# ------ Basic Statistics ------
print(f"Total messages: {len(valid_messages)}")
print(f"Unique users: {valid_messages['user'].nunique()}")
print(f"Time range: {valid_messages['timestamp'].min()} - {valid_messages['timestamp'].max()}")

# ------ Visualization ------
if not valid_messages.empty:
    # Hourly activity
    plt.figure(figsize=(12, 6))
    valid_messages['hour'].value_counts().sort_index().plot(kind='bar')
    plt.title('Messages by Hour of Day')
    plt.xlabel('Hour (24h format)')
    plt.ylabel('Message Count')
    plt.show()

    # Top Contributors
    top_users = valid_messages['user'].value_counts().head(10)
    plt.figure(figsize=(12, 6))
    top_users.plot(kind='barh')
    plt.title('Top Contributors')
    plt.xlabel('Message Count')
    plt.ylabel('User')
    plt.show()
else:
    print("No valid messages found for analysis")

# ------ Debug Output ------
print("\nFirst 5 parsed messages:")
print(valid_messages[['timestamp', 'user', 'message']].head())