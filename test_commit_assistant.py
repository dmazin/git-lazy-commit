import unittest
from unittest.mock import MagicMock, patch

from commit_assistant import GitCommitAssistant


class TestGitCommitAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = GitCommitAssistant()

    def test_get_uncommitted_changes(self):
        repo_mock = MagicMock()
        diff_mock = MagicMock()
        diff_mock.diff = "example change"
        repo_mock.index.diff.return_value = [diff_mock]

        changes = self.assistant.get_uncommitted_changes(repo_mock)
        self.assertEqual(changes, ["example change"])

    def test_generate_commit_message(self):
        changes_summary = "example change"
        with patch.object(self.assistant.chatgpt, "execute", return_value="Update example feature") as chatgpt_mock:
            commit_message = self.assistant.generate_commit_message(changes_summary)
            chatgpt_mock.assert_called_once()
            self.assertEqual(commit_message, "Update example feature")

if __name__ == "__main__":
    unittest.main()
