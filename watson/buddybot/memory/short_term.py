class ShortTermMemory:
    def __init__(self, max_history=10):
        self.history = []
        self.max_history = max_history
        self.current_context = ""

    def add_interaction(self, user_input, agent_response):
        self.history.append({"user": user_input, "agent": agent_response})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_history(self):
        return self.history

    def get_formatted_history(self):
        formatted = ""
        for item in self.history:
            formatted += f"User: {item['user']}\nAssistant: {item['agent']}\n"
        return formatted

    def clear(self):
        self.history = []
