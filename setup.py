from setuptools import setup, find_packages

setup(
    name="chatgpt-commit-assistant",
    version="0.3",
    packages=find_packages(),
    entry_points={"console_scripts": ["chatgpt-commit-assistant = chatgpt_commit_assistant.commit_assistant:main"]},
    install_requires=["openai", "GitPython"],
)
