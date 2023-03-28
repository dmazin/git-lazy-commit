# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0

# This entire module was created by Simon Willison, and slightly modified by
# Dmitry Mazin. The blog post where Simon published the code is here:
# https://til.simonwillison.net/gpt3/chatgpt-api
import os
import openai


class ChatBot:
    def __init__(self, model, system="", is_verbose=False, api_key_path=None):
        self.system = system
        self.messages = []
        self.model: str = model
        self.is_verbose: bool = is_verbose

        # Precedence of ways to submit the API key:
        # 1. --api-key-path
        # 2. OPENAI_API_KEY environment variable
        # 3. ~/.openai-api-key
        if api_key_path:
            openai.api_key_path = api_key_path
            if self.is_verbose:
                print("Using API key from {}".format(api_key_path))
        elif os.getenv("OPENAI_API_KEY"):
            # Not actually setting the api key here, because OpenAI will itself
            # look for this env var
            if self.is_verbose:
                print("Using API key from OPENAI_API_KEY environment variable")
        elif api_key_path is None:
            default_key_path: str = os.path.join(
                os.path.expanduser("~"), ".openai-api-key"
            )
            if os.path.exists(default_key_path):
                with open(default_key_path) as f:
                    openai.api_key = f.read().strip()
                    if self.is_verbose:
                        print("Using API key from {}".format(default_key_path))
            else:
                raise ValueError(
                    "Please provide an API key path using --api-key-path or set the OPENAI_API_KEY environment variable."
                )

        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = openai.ChatCompletion.create(
            model=self.model, messages=self.messages
        )
        if self.is_verbose:
            # eg: {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
            print(completion.usage)
        return completion.choices[0].message.content
