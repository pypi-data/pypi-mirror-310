from ollama import chat

class NL2CLI:
    """
    A library for converting natural language to CLI commands using Ollama's chat functionality.
    """

    def __init__(self, model="x/llama3.2-vision:11b"):
        """
        Initialize the library with the model to be used.
        
        :param model: The name of the LLM model hosted on Ollama.
        """
        self.model = model

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
            #print("Raw response:", response)  # Debugging output

            # Correctly extract the command from response['message']['content']
            cleaned_text = response['message']['content'].strip()
            if not cleaned_text:
                raise ValueError("The response content is empty.")
            return cleaned_text
        except KeyError:
            raise RuntimeError("Unexpected response format from Ollama chat.")
        except Exception as e:
            raise RuntimeError(f"Error communicating with Ollama chat: {e}")
