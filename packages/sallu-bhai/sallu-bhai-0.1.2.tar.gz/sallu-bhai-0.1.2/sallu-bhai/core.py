import subprocess
from ollama import chat

class NL2CLI:
    """
    A library for converting natural language to CLI commands using Ollama's chat functionality.
    """

    def __init__(self, model=None):
        """
        Initialize the library with a model.
        If `-n` is passed, it selects an available model dynamically.
        
        :param model: The name of the LLM model hosted on Ollama.
                      If None, defaults to the first available model.
        """
        if model == "-n":
            self.model = self.get_available_model()
        else:
            self.model = model or "qwen2.5-coder:0.5b-instruct-q4_0"

    @staticmethod
    def get_available_model() -> str:
        """
        Fetches available models using `ollama list` and returns the first available one.

        :return: The name of the first available model.
        :raises: RuntimeError if no models are available.
        """
        try:
            # Run the `ollama list` command to get available models
            result = subprocess.run(
                ["ollama", "list"], capture_output=True, text=True, check=True
            )
            models = result.stdout.strip().split("\n")
            
            # Extract model names and pick the first one
            if models:
                return models[0]  # Select the first model
            else:
                raise RuntimeError("No models available on Ollama server.")
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to fetch models: {e.stderr.strip()}") from e

    def set_model(self, model_name: str):
        """
        Update the model used by the library.
        
        :param model_name: The new model name to use.
        """
        self.model = model_name

    def get_cli_command(self, natural_language: str) -> str:
        """
        Sends the natural language description to the LLM and retrieves the corresponding CLI command.

        :param natural_language: The natural language input.
        :return: The cleaned CLI command as a string.
        :raises: RuntimeError if the API call fails or the response format is unexpected.
        """
        messages = [
            {
                "role": "user",
                "content": (
                    f"You are an assistant that converts natural language into CLI commands.\n"
                    f"Translate the following description into an exact CLI command:\n\n"
                    f"{natural_language}\n\n"
                    f"Only output the command, without any additional explanation."
                )
            }
        ]

        try:
            response = chat(model=self.model, messages=messages)
            # Extract the command from response['message']['content']
            cleaned_text = response['message']['content'].strip()
            if not cleaned_text:
                raise ValueError("The response content is empty.")
            return cleaned_text
        except KeyError:
            raise RuntimeError("Unexpected response format from Ollama chat.")
        except Exception as e:
            raise RuntimeError(f"Error communicating with Ollama chat: {e}")
