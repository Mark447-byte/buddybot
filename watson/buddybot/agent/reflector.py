class Reflector:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def reflect(self, step, result):
        prompt = f"""
Step executed: {step}
Result: {result}

Did the step succeed? Should the agent continue or stop?
Respond with ONE WORD: 'CONTINUE' or 'STOP'. 
Followed by a brief reason.
"""
        response = self.llm_client.generate(prompt)
        cleaned_response = response.strip().upper()
        
        if cleaned_response.startswith("STOP"):
            return False, response
        elif cleaned_response.startswith("CONTINUE"):
            return True, response
            
        # Fallback for unexpected LLM output
        if "CONTINUE" in cleaned_response:
            return True, response
        return False, response # Default to stop for safety
