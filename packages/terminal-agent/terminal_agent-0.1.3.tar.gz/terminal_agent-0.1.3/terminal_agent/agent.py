import subprocess
import re
from transformers import pipeline


class TerminalAgent:
    def __init__(self, model_name="t5-small"):
        print("Initializing the terminal agent...")
        self.model = pipeline("text2text-generation", model=model_name)
        print("Model loaded successfully!")

    def parse_command(self, instruction):
        """Convert natural language instruction to a Linux command."""
        prompt = f"Convert the following instruction to a Linux command:\n{instruction}"
        response = self.model(prompt, max_length=50, num_return_sequences=1)
        command = response[0]['generated_text'].strip().split('\n')[0]
        return command

    def validate_command(self, command):
        """Check for potentially harmful commands."""
        dangerous_patterns = [
            r"rm\s+-rf\s+/",
            r"dd\s+if=",
            r":(){:|:&};:",
            r"shutdown",
            r"mkfs\..*",
            r"passwd\s+root",
            r"iptables\s+-F",
        ]
        for pattern in dangerous_patterns:
            if re.search(pattern, command):
                return False, f"Command '{command}' is potentially harmful!"
        if not command or len(command.split()) < 2:
            return False, "Generated command is invalid!"
        return True, "Command validated successfully."

    def execute_command(self, command):
        """Execute the command and return its output."""
        try:
            print(f"Executing: {command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
            if result.stdout:
                return f"Output:\n{result.stdout}"
            if result.stderr:
                return f"Error:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "Execution failed: Command timed out!"
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
            confirm = input(f"Generated Command: {command}\nDo you want to execute it? (y/n/r for regenerate): ")
            if confirm.lower() == 'r':
                continue
            if confirm.lower() == 'y':
                output = self.execute_command(command)
                print(output)
            else:
                print("Command not executed.")


def main():
    """Entry point for the terminal-agent command."""
    agent = TerminalAgent()
    agent.run()
