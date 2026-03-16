from memory.long_term import LongTermMemory

class TaskTools:
    def __init__(self, memory: LongTermMemory):
        self.memory = memory

    def add_task(self, content):
        task_id = self.memory.add_task(content)
        return f"Task added with ID: {task_id}"

    def list_tasks(self, status=None):
        tasks = self.memory.get_tasks(status)
        if not tasks:
            return "No tasks found."
        
        result = "Tasks:\n"
        for t in tasks:
            result += f"[{t[0]}] {t[1]} - {t[2]}\n"
        return result

    def complete_task(self, task_id):
        try:
            self.memory.update_task_status(int(task_id), "completed")
            return f"Task {task_id} marked as completed."
        except Exception as e:
            return str(e)
