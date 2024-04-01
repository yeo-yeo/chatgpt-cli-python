from setuptools import setup, find_packages

setup(
    name="quaero",
    version="1.0.0",
    description="Simple CLI tool for asking ChatGPT questions in the CLI",
    author="Gillian Yeomans",
    author_email="hello@gillian.codes",
    url="https://github.com/yeo-yeo/chatgpt-cli-python",
    packages=find_packages(),
    install_requires=["aiohttp", "colorama", "python-dotenv"],
    entry_points={
        "console_scripts": [
            "quaero=quaero.index:main",
        ],
    },
)
