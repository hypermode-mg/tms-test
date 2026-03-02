def add(a: int, b: int):
    return a + b


def div(a: int, b: int) -> float:
    if b == 0:
         raise ValueError("Деление на ноль!")
    return a / b