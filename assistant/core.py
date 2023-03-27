import os
import argparse
import subprocess
import git
from .chatbot import ChatBot


class Assistant:
    def __init__(self, model="gpt-3.5-turbo", is_verbose=False):
        self.chatgpt = ChatBot(
            system="You are an assistant whose job is to generate commit messages given a list of git changes. In your responses, please just send back the commit message without any additional text. In your commit messages, try to be descriptive, i.e. don't just say 'refactored code.' I will send you the output of `git diff --staged`. Please respond with a commit message that describes the changes in the given diff. Also, the diff may include multiple changes. Put these in a list.",
            model=model,
            is_verbose=is_verbose,
        )

    def get_uncommitted_changes(self):
        staged_changes = subprocess.run(
            ["git", "diff", "--staged"], capture_output=True, text=True
        )
        uncommitted_changes = staged_changes.stdout.strip().split("\n")
        return uncommitted_changes

    def generate_commit_message(self, changes_summary):
        return self.chatgpt(changes_summary)

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


def main(args=None):
    if args is None:
        args = parse_arguments()

    assistant = Assistant(args.model, args.verbose)

    repo = git.Repo(os.getcwd())
    uncommitted_changes = assistant.get_uncommitted_changes()
    changes_summary = "\n".join(uncommitted_changes)

    if uncommitted_changes == [""]:
        print("There are no uncommitted changes.")
        return

    generated_commit_message = assistant.generate_commit_message(changes_summary)

    while not assistant.get_user_approval(generated_commit_message):
        generated_commit_message = assistant.generate_commit_message(changes_summary)

    assistant.commit_changes(repo, generated_commit_message)
    return "Changes committed."


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate commit messages based on staged changes."
    )
    parser.add_argument(
        "-m", "--model", default="gpt-3.5-turbo", help="OpenAI API model to use"
    )
    parser.add_argument(
        "--verbose", action='store_true', help="Print extra information"
    )
    args = parser.parse_args()
    return args
