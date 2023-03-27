from setuptools import setup, find_packages

setup(
    name="chatgpt-commit-assistant",
    version="0.6",
    packages=find_packages(),
    entry_points={"console_scripts": ["chatgpt-commit-assistant = assistant:main"]},
    install_requires=["openai", "GitPython"],
)
