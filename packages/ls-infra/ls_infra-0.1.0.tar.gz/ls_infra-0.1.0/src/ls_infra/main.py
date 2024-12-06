# src/ls_infra/main.py
"""Main module for ls-infra package."""


def say_hello(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: Name to greet. Defaults to "World".

    Returns:
        A greeting string
    """
    return f"Hello, {name}!"


if __name__ == "__main__":
    print(say_hello())
