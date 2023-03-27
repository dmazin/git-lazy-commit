from setuptools import setup, find_packages

setup(
    name="git-lazy-commit",
    version="0.6",
    packages=find_packages(),
    entry_points={"console_scripts": ["git-lazy-commit = assistant:main"]},
    install_requires=["openai", "GitPython"],
)
# foo