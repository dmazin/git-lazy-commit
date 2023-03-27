# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0

# This entire module was created by Simon Willison. The blog post where he
# published the code is here: https://til.simonwillison.net/gpt3/chatgpt-api
import openai


class ChatBot:
    def __init__(self, model, system="", is_verbose=False):
        self.system = system
        self.messages = []
        self.model: str = model
        self.is_verbose: bool = is_verbose
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
