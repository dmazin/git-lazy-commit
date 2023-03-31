import os
import argparse
import subprocess
import git
from .chatbot import ChatBot


class Assistant:
    def __init__(self, model="gpt-3.5-turbo", is_verbose=False, api_key_path=None):
        self.chatgpt = ChatBot(
            system="Please generate a commit message given the output of `git diff`. Please respond with a commit message without any additional text.",
            model=model,
            is_verbose=is_verbose,
            api_key_path=api_key_path,
        )

    def get_uncommitted_changes(self):
        staged_changes = subprocess.run(
            ["git", "diff", "--staged"], capture_output=True, text=True
        )
        uncommitted_changes = staged_changes.stdout.strip().split("\n")
        return uncommitted_changes

    def generate_commit_message(self, changes_summary):
        # Trim the changes summary because the most common model, gpt-3.5-turbo,
        # has a 4096 character limit
        return self.chatgpt(changes_summary[:4096])

    def generate_alternative_commit_message(self):
        return self.chatgpt(
            "Please come up with another commit message for the diff I sent earlier."
        )

    def commit_changes(self, repo, commit_message):
        repo.index.commit(commit_message)

    def get_user_approval(self, commit_msg):
        print(f"Generated commit message: {commit_msg}")
        user_input = (
            input("Do you approve this commit message? ((y)es/(n)o/(e)ditor): ")
            .strip()
            .lower()
        )

        if user_input in ["yes", "y"]:
            return True, commit_msg
        elif user_input in ["no", "n"]:
            return False, commit_msg
        elif user_input in ["editor", "e"]:
            return self.edit_commit_message(commit_msg)
        else:
            print(
                "Invalid input. Please enter 'yes (or y)', 'no (or n)', or 'editor (or e)'."
            )
            return self.get_user_approval(commit_msg)

    def edit_commit_message(self, commit_msg):
        with open("temp_commit_msg.txt", "w") as f:
            f.write(commit_msg)

        editor = os.environ.get("EDITOR", "vim")
        subprocess.run([editor, "temp_commit_msg.txt"])

        with open("temp_commit_msg.txt", "r") as f:
            edited_commit_msg = f.read().strip()

        os.remove("temp_commit_msg.txt")
        return self.get_user_approval(edited_commit_msg)


def main(args=None):
    if args is None:
        args = parse_arguments()

    assistant = Assistant(args.model, args.verbose, args.api_key_path)

    repo = git.Repo(os.getcwd())

    if args.add:
        repo.git.add(all=True)

    uncommitted_changes = assistant.get_uncommitted_changes()
    changes_summary = "\n".join(uncommitted_changes)

    if uncommitted_changes == [""]:
        print("There are no staged changes.")
        return

    generated_commit_message = assistant.generate_commit_message(changes_summary)

    while True:
        user_approved, commit_message = assistant.get_user_approval(
            generated_commit_message
        )
        if user_approved:
            break
        else:
            generated_commit_message = assistant.generate_alternative_commit_message()

    assistant.commit_changes(repo, commit_message)
    return "Changes committed."


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Generate commit messages based on staged changes."
    )
    parser.add_argument(
        "-m", "--model", default="gpt-3.5-turbo", help="OpenAI API model to use"
    )
    parser.add_argument(
        "--api-key-path",
        help="Tell me where you stored your OpenAI API key. If this isn't provided, I'll look for the OPENAPI_API_KEY env var, and failing that, ~/.openai_api_key.",
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print extra information"
    )
    parser.add_argument(
        "--add", action="store_true", help="Run `git add .` before generating the commit message"
    )
    args = parser.parse_args()
    return args
