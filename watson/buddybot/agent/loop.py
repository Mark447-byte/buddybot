from agent.planner import Planner
from agent.reflector import Reflector
from tools.file_tools import list_files, read_file, write_file
from tools.shell_tools import execute_shell

class AgentLoop:
    def __init__(self, llm_client, task_tools, long_term_memory, short_term_memory):
        self.planner = Planner(llm_client)
        self.reflector = Reflector(llm_client)
        self.task_tools = task_tools
        self.long_term_memory = long_term_memory
        self.short_term_memory = short_term_memory
        self.tools = {
            "list_files": list_files,
            "read_file": read_file,
            "write_file": write_file,
            "execute_shell": execute_shell,
            "add_task": self.task_tools.add_task,
            "list_tasks": self.task_tools.list_tasks,
            "complete_task": self.task_tools.complete_task
        }

    def run(self, user_goal):
        print(f"BuddyBot: Planning for goal: {user_goal}")
        
        # Retrieve context from short-term memory
        context = self.short_term_memory.get_formatted_history()
        
        plan = self.planner.plan(user_goal, context=context)
        
        execution_details = ""
        for step in plan:
            description = step.get('description', 'Unknown step')
            print(f"BuddyBot: Executing step: {description}")
            tool_name = step.get('tool')
            args = step.get('args', {}) or {}
            
            if tool_name and tool_name in self.tools:
                try:
                    result = self.tools[tool_name](**args)
                except Exception as e:
                    result = f"Error executing tool: {str(e)}"
            elif tool_name is None or tool_name == "":
                # No tool (e.g. Ollama error step) - use description as result
                result = description
            else:
                result = f"Unknown tool: {tool_name}. Available: list_files, read_file, write_file, add_task, list_tasks, complete_task, execute_shell"
            
            print(f"BuddyBot: Result: {result}")
            
            should_continue, reflection = self.reflector.reflect(step, result)
            execution_details += f"Step: {description}\nResult: {result}\nReflection: {reflection}\n\n"
            
            if not should_continue:
                print("BuddyBot: Stopping based on reflection.")
                break
        
        # Summarize the interaction for memory
        summary = f"Goal: {user_goal}\n{execution_details}"
        
        # Store in both memory layers
        self.short_term_memory.add_interaction(user_goal, execution_details)
        self.long_term_memory.store_interaction(user_goal, execution_details, summary=summary)
        
        return execution_details
