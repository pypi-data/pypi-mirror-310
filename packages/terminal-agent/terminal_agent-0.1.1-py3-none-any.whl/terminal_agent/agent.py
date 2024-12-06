import subprocess
import re
from transformers import pipeline


class TerminalAgent:
    def __init__(self, model_name="tiiuae/falcon-7b-instruct"):
        print("Initializing the terminal agent...")
        self.model = pipeline("text2text-generation", model=model_name)
        print("Model loaded successfully!")

    def parse_command(self, instruction):
        """Convert natural language instruction to a Linux command."""
        prompt = f"Convert the following instruction to a Linux command:\n{instruction}"
        response = self.model(prompt, max_length=50, num_return_sequences=1)
        command = response[0]['generated_text']
        return command.strip()

    def validate_command(self, command):
        """Check for potentially harmful commands."""
        dangerous_patterns = [
            r"rm\s+-rf\s+/",    # Prevent root directory deletion
            r"dd\s+if=",        # Prevent destructive disk operations
            r":(){:|:&};:"      # Prevent fork bomb
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, command):
                return False, f"Command '{command}' is potentially harmful!"
        return True, "Command validated successfully."

    def execute_command(self, command):
        """Execute the command and return its output."""
        try:
            print(f"Executing: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.stdout:
                return f"Output:\n{result.stdout}"
            if result.stderr:
                return f"Error:\n{result.stderr}"
        except Exception as e:
            return f"Execution failed: {e}"

    def run(self):
        """Main loop to interact with the user."""
        print("Welcome to the Terminal Agent! Type 'exit' to quit.")
        while True:
            instruction = input("\nEnter your instruction: ")
            if instruction.lower() == "exit":
                print("Goodbye!")
                break

            # Step 1: Parse the command
            command = self.parse_command(instruction)

            # Step 2: Validate the command
            is_valid, message = self.validate_command(command)
            if not is_valid:
                print(message)
                continue

            # Step 3: Confirm execution
            confirm = input(f"Generated Command: {command}\nDo you want to execute it? (y/n): ")
            if confirm.lower() == 'y':
                output = self.execute_command(command)
                print(output)
            else:
                print("Command not executed.")


def main():
    """Entry point for the terminal-agent command."""
    agent = TerminalAgent()
    agent.run()
