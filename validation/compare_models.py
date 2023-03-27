import os
import sys
from assistant import Assistant


def read_diffs_from_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        diffs = content.split("###separator###")
    return diffs


def generate_commit_messages(diffs, model):
    assistant = Assistant(model=model)
    commit_messages = []

    for diff in diffs:
        commit_message = assistant.generate_commit_message(diff)
        commit_messages.append(commit_message)

    return commit_messages


def main():
    if len(sys.argv) != 2:
        print("Usage: python compare_models.py <diff_file>")
        sys.exit(1)

    diff_file_path = sys.argv[1]
    diffs = read_diffs_from_file(diff_file_path)

    models = ["gpt-3.5-turbo", "gpt-4"]

    for i, diff in enumerate(diffs):
        print(f"\ndiff {i + 1}:\n{diff}")
        for model in models:
            commit_message = generate_commit_messages([diff], model)[0]
            print(f"{model} output: {commit_message}")


if __name__ == "__main__":
    main()
