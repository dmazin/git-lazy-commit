import os
import git
from chatgpt_commit_assistant.chatbot import ChatBot


class GitCommitAssistant:
    def __init__(self):
        self.chatgpt = ChatBot(
            "You are an assistant whose job is to generate commit messages given a list of git changes. In your responses, please just send back the commit message without any additional text. In your commit messages, try to be descriptive, i.e. don't just say 'refactored code'."
        )

    def get_uncommitted_changes(self, repo):
        uncommitted_changes = repo.git.diff().split("\n")
        return uncommitted_changes

    def generate_commit_message(self, changes_summary):
        message = (
            f"Generate a commit message for the following changes:\n{changes_summary}"
        )
        return self.chatgpt(message)

    def commit_changes(self, repo, commit_message):
        repo.git.add(update=True)
        repo.index.commit(commit_message)

    def get_user_approval(self, commit_msg):
        print(f"Generated commit message: {commit_msg}")
        user_input = (
            input("Do you approve this commit message? (yes/no): ").strip().lower()
        )

        if user_input == "yes":
            return True
        elif user_input == "no":
            return False
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")
            return self.get_user_approval(commit_msg)


def main():
    assistant = GitCommitAssistant()
    repo = git.Repo(os.getcwd())
    uncommitted_changes = assistant.get_uncommitted_changes(repo)
    changes_summary = "\n".join(uncommitted_changes)

    while True:
        generated_commit_message = assistant.generate_commit_message(changes_summary)
        if assistant.get_user_approval(generated_commit_message):
            # Commit the changes if the user approves the commit message
            assistant.commit_changes(repo, generated_commit_message)
            print("Changes committed.")
            break
        else:
            print("Generating new commit message...")

    print("Exiting Git commit assistant.")


if __name__ == "__main__":
    main()
