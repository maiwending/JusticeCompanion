import requests
import re

url = "http://localhost:1234/v1/chat/completions"  # LM Studio API endpoint
payload = {
    "model": "meta-llama-3-8b-instruct",  # your loaded model name
    "messages": [
        {"role": "system", "content": "You are a helpful assistant. Do not output 'Thinking', '...', or any filler text. Only provide direct, helpful, and complete answers to the user's question."},
        {"role": "user", "content": "What is asylum protection bases?"}
    ],
    "max_tokens": 20480,  # No practical limit
    "temperature": 0.2,
    "stream": False
}

try:
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    # Extract only the AI's reply content and remove 'Thinking' or <think> tags
    ai_reply = None
    if "choices" in data and data["choices"]:
        ai_reply = data["choices"][0]["message"]["content"]
    elif "message" in data and "content" in data["message"]:
        ai_reply = data["message"]["content"]
    elif "messages" in data and data["messages"]:
        ai_reply = data["messages"][-1]["content"]
    if ai_reply:
        # Remove <think>...</think> blocks and <think> tags
        ai_reply = re.sub(r'<think>.*?</think>', '', ai_reply, flags=re.DOTALL|re.IGNORECASE)
        ai_reply = re.sub(r'</?think>', '', ai_reply, flags=re.IGNORECASE)
        # Remove lines that are just 'Thinking', '...', or similar
        ai_reply = '\n'.join([line for line in ai_reply.split('\n') if line.strip().lower() not in ['thinking', '...', '…']])
        # Remove if the whole reply is just 'Thinking' or '...'
        if ai_reply.strip().lower() in ['thinking', '...', '…']:
            ai_reply = ''
        print(ai_reply.strip())
    else:
        print("No valid AI response found.")
except Exception as e:
    print(f"Error: {e}")