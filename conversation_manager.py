# Manages conversations per sender
class ConversationManager:
    def __init__(self):
        self.conversations = {}
    def get_or_create_conversation(self, sender):
        if sender not in self.conversations:
            self.conversations[sender] = []
        return self.conversations[sender]
    def add_message(self, sender, message):
        self.get_or_create_conversation(sender).append(message)
