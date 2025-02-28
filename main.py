from groq import Groq
import requests

api_token = "7650006636:AAFFgk-DEGYQgsDjCKq42mdJYMNL9Pv-EKs"
chat_id = "7817879334"
send_message_url = f"https://api.telegram.org/bot{api_token}/sendMessage"
get_updates_url = f"https://api.telegram.org/bot{api_token}/getUpdates"


def send_message(chat_id, text):
    params = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(send_message_url, params=params)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print("Failed to send message.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
def get_updates(offset=None):
    params = {'timeout': 100, 'offset': offset}
    response = requests.get(get_updates_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to get updates.")
        print("Status Code:", response.status_code)
        print("Response:", response.text)
        return None
    
update_id = None

def get_message():
    global update_id
    print("Polling for new messages...")
    while True:
        updates = get_updates(update_id)
        if updates:
            for update in updates['result']:
                update_id = update['update_id'] + 1
                if 'message' in update:
                    message_text = update['message'].get('text', '')
                    if message_text:
                        return message_text


client = Groq(
    api_key="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",
)

user_input = ""

while True:
    user_input = get_message()
    print(user_input)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_input,
            }
        ],
        model="llama-3.3-70b-versatile",
        stream=False,
    )

    send_message(chat_id, chat_completion.choices[0].message.content)
