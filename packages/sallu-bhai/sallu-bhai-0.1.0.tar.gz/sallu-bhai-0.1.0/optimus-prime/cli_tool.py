import sys
from .core import NL2CLI

def main():
    # Check for `-n` argument or custom model
    model_arg = "-n" if "-n" in sys.argv else None
    nl2cli = NL2CLI(model=model_arg)

    # Example input
    natural_language_input = "Find all Python files in the current directory."

    try:
        cli_command = nl2cli.get_cli_command(natural_language_input)
        print(f"CLI Command: {cli_command}")
    except RuntimeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
