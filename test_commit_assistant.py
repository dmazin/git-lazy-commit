import unittest
from unittest.mock import MagicMock, patch

from chatgpt_commit_assistant.commit_assistant import GitCommitAssistant


class TestGitCommitAssistant(unittest.TestCase):
    def setUp(self):
        self.assistant = GitCommitAssistant()

    def test_get_uncommitted_changes(self):
        repo_mock = MagicMock()
        repo_mock.git.diff.return_value = "example change"

        changes = self.assistant.get_uncommitted_changes(repo_mock)
        self.assertEqual(changes, ["example change"])

    def test_generate_commit_message(self):
        changes_summary = "example change"
        with patch.object(
            self.assistant.chatgpt, "execute", return_value="Update example feature"
        ) as chatgpt_mock:
            commit_message = self.assistant.generate_commit_message(changes_summary)
            chatgpt_mock.assert_called_once()
            self.assertEqual(commit_message, "Update example feature")

    def test_commit_changes(self):
        repo_mock = MagicMock()
        commit_message = "Update example feature"
        self.assistant.commit_changes(repo_mock, commit_message)
        repo_mock.git.add.assert_called_once_with(update=True)
        repo_mock.index.commit.assert_called_once_with(commit_message)


if __name__ == "__main__":
    unittest.main()
