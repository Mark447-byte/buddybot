from input.text_input import get_text_input

class InputController:
    """Handles user input. Pass voice_input=None for text-only mode."""

    def __init__(self, voice_input=None):
        self.voice_input = voice_input

    def get_user_goal(self):
        if self.voice_input is None:
            return get_text_input("You: ")
        
        print("\nBuddyBot: Select input mode:")
        print("T - Text (Keyboard)")
        print("V - Voice (Push-to-Talk)")
        choice = input("Choice [T/V]: ").strip().upper()
        
        if choice == 'V':
            input("Press Enter to start recording...")
            text = self.voice_input.get_voice_input()
            if text:
                print(f"BuddyBot (Voice to Text): {text}")
                return text
            else:
                print("BuddyBot: Voice input failed. Falling back to text.")
                return get_text_input("You: ")
        else:
            return get_text_input("You: ")
