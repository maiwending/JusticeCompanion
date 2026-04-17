import requests
import os
import time
import re

def redact_pii(text):
    if not text:
        return text
    # Redact 9-digit inmate IDs (e.g. 100009990)
    text = re.sub(r'\b\d{9,}\b', '[ID]', text)
    # Redact ALL-CAPS name patterns (two or more all-caps words)
    text = re.sub(r'\b[A-Z]{2,}(?:\s+[A-Z]{2,})+\b', '[NAME]', text)
    return text

# Handles AI chat integration (OpenAI or local LLM)
class AIChat:
    def __init__(self):
        pass  # TODO: Setup OpenAI or local LLM
    def get_response(self, conversation_id, message):
        pass  # TODO: Implement chat logic

class LMStudioChat:
    def __init__(self, model="meta-llama-3-8b-instruct", base_url="http://localhost:1234/v1/chat/completions", log_dir="logs"):
        self.model = model
        self.base_url = base_url
        self.conversations = {}  # sender_name -> list of messages
        self.log_dir = log_dir
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def log_interaction(self, sender, user_message, ai_reply):
        log_file = os.path.join(self.log_dir, f"{sender.replace(' ', '_')}.log")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"=== {time.strftime('%Y-%m-%d %H:%M:%S')} ===\n")
            f.write(f"User: {user_message}\n")
            f.write(f"AI: {ai_reply}\n\n")

    def get_or_create_conversation(self, sender):
        if sender not in self.conversations:
            self.conversations[sender] = []
        return self.conversations[sender]

    def get_response(self, sender, message):
        conversation = self.get_or_create_conversation(sender)
        conversation.append({"role": "user", "content": redact_pii(message)})
        # Add a system prompt to instruct the AI not to output 'Thinking' or similar filler
        system_prompt = {
            "role": "system",
            "content": "You are an expert legal and religious assistant. Do not output 'Thinking', '...', or any filler text. Only provide direct, helpful, and complete answers to the user's question."
        }
        # Insert system prompt only once at the start of the conversation
        if not any(msg["role"] == "system" for msg in conversation):
            conversation.insert(0, system_prompt)
        payload = {
            "model": self.model,
            "messages": conversation,
            "max_tokens": 20480,
            "temperature": 0.2,
            "stream": False
        }
        response = requests.post(self.base_url, json=payload)
        response.raise_for_status()
        data = response.json()
        # Robustly extract the AI reply from possible response formats
        ai_reply = None
        if "choices" in data and data["choices"]:
            ai_reply = data["choices"][0]["message"]["content"]
        elif "message" in data and "content" in data["message"]:
            ai_reply = data["message"]["content"]
        elif "messages" in data and data["messages"]:
            ai_reply = data["messages"][-1]["content"]
        else:
            raise ValueError(f"Unexpected response format from LM Studio: {data}")
        if ai_reply:
            # Remove all content between <think> and </think>, including the tags
            ai_reply = re.sub(r'<think>.*?</think>', '', ai_reply, flags=re.DOTALL|re.IGNORECASE)
            # Remove any standalone <think> or </think> tags
            ai_reply = re.sub(r'</?think>', '', ai_reply, flags=re.IGNORECASE)
            ai_reply = ai_reply.strip()
            # Remove lines that are just 'Thinking', '...', or similar
            ai_reply = '\n'.join([line for line in ai_reply.split('\n') if line.strip().lower() not in ['thinking', '...', '…']])
            # Remove if the whole reply is just 'Thinking' or '...'
            if ai_reply.strip().lower() in ['thinking', '...', '…']:
                ai_reply = ''
        conversation.append({"role": "assistant", "content": ai_reply})
        self.log_interaction(sender, message, ai_reply)
        return ai_reply
