import os
import subprocess
import logging
import dotenv
import argparse

from langchain_openai import ChatOpenAI
from rich.console import Console
from rich.markdown import Markdown

logging.basicConfig(
    level=logging.WARN, format="%(asctime)s - %(levelname)s - %(message)s"
)
dotenv.load_dotenv()


MODEL = os.getenv("MODEL")
LANGUAGE = os.getenv("LANGUAGE")

console = Console()


def main():
    args = parse_args()
    check_env()

    model, language = args

    llm = ChatOpenAI(model=model)

    diff = get_diff()

    review = get_review(llm, diff, language=language)

    formatted_review = format_review(review)

    console.print(formatted_review)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m", "--model", type=str, help="Specify the model. (default: o1-mini)"
    )
    parser.add_argument(
        "-l", "--language", type=str, help="Specify the language. (default: ENGLISH)"
    )
    args = parser.parse_args()

    args.model = args.model or MODEL or "o1-mini"
    args.language = args.language or LANGUAGE or "ENGLISH"

    return args.model, args.language


def check_env():
    required_vars = ["OPENAI_API_KEY"]

    for var in required_vars:
        if not os.getenv(var):
            raise EnvironmentError(f"Required environment variable '{var}' is not set.")


def get_diff() -> str:
    result = subprocess.run(["git", "show", "head"], capture_output=True)

    if result.returncode == 128:
        raise ValueError("No commits found")

    return result.stdout.decode("utf-8")


def get_review(llm: ChatOpenAI, diff: str, language: str) -> str:
    review = llm.invoke(
        [
            (
                "assistant",
                f"Review the user's git diff, checking for typos, grammar, and code style issues. OUTPUT THE REVIEW IN {language}.",
            ),
            ("human", diff),
        ]
    ).content

    review = str(review)

    return review


def format_review(review: str):
    diff_syntax = Markdown(review, code_theme="ansi_dark")

    return diff_syntax


if __name__ == "__main__":
    main()
