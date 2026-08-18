from backend.app.database.crud import save_message, load_history


class MemoryManager:

    def add_user_message(self, message):
        save_message("user", message)

    def add_ai_message(self, message):
        save_message("assistant", message)

    def get_history(self):
        return load_history()