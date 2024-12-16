import json
from datetime import datetime


class ChatHistoryFile:
    def __init__(self, file_name="chat_history.json"):
        self.file_name = file_name

    def save_message(self, session_id, role, message):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        timestamp = datetime.utcnow().isoformat()
        if session_id not in data:
            data[session_id] = []
        data[session_id].append({
            "role": role,
            "message": message,
            "timestamp": timestamp
        })

        with open(self.file_name, "w") as file:
            json.dump(data, file, indent=4)

    def get_history(self, session_id):
        try:
            with open(self.file_name, "r") as file:
                data = json.load(file)
            return data.get(session_id, [])
        except FileNotFoundError:
            return []


# Sử dụng
# chat_file = ChatHistoryFile()
# chat_file.save_message("12345", "user", "Hello, chatbot!")
# chat_file.save_message("12345", "bot", "Hello! How can I assist you today?")
# print(chat_file.get_history("12345"))
