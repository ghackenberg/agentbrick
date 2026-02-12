from langchain.tools import tool


@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers.

    Args:
        a(int): First number.
        b(int): Second number.
    """
    return a + b
