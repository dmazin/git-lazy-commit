import unittest
from unittest.mock import Mock, patch

from .context import assistant


class TestChatBot(unittest.TestCase):
    def setUp(self):
        self.model = "gpt-4"
        self.system_message = "Welcome to the ChatBot!"

    @patch("assistant.chatbot.openai.ChatCompletion.create")
    def test_init_without_system_message(self, mock_create):
        chatbot = assistant.ChatBot(self.model)
        self.assertEqual(chatbot.model, self.model)
        self.assertEqual(chatbot.system, "")
        self.assertEqual(chatbot.messages, [])

    @patch("assistant.chatbot.openai.ChatCompletion.create")
    def test_init_with_system_message(self, mock_create):
        chatbot = assistant.ChatBot(self.model, self.system_message)
        self.assertEqual(chatbot.model, self.model)
        self.assertEqual(chatbot.system, self.system_message)
        self.assertEqual(
            chatbot.messages, [{"role": "system", "content": self.system_message}]
        )

    @patch("assistant.chatbot.openai.ChatCompletion.create")
    def test_call(self, mock_create):
        chatbot = assistant.ChatBot(self.model, self.system_message)
        user_message = "Hello, ChatBot!"
        chatbot_response = "Hello, User!"

        # Set up the mock response from the API
        mock_create.return_value = Mock(
            choices=[Mock(message=Mock(content=chatbot_response))]
        )

        response = chatbot(user_message)

        self.assertEqual(response, chatbot_response)
        self.assertEqual(
            chatbot.messages[-1], {"role": "assistant", "content": chatbot_response}
        )

    @patch("assistant.chatbot.openai.ChatCompletion.create")
    def test_call_and_execute(self, mock_create):
        chatbot = assistant.ChatBot(self.model, self.system_message)
        user_message = "What's the weather like today?"
        chatbot_response = "It's a sunny day!"

        # Set up the mock response from the API
        mock_create.return_value = Mock(
            choices=[Mock(message=Mock(content=chatbot_response))]
        )

        response = chatbot(user_message)

        self.assertEqual(response, chatbot_response)
        mock_create.assert_called_once()


if __name__ == "__main__":
    unittest.main()
