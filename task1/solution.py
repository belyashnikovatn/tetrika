import inspect


def strict(func):
    """
    Декоратор для проверки типов аргументов функции.
    :param func: Функция, для которой нужно проверить типы аргументов
    :return: Обернутая функция с проверкой типов
    """
    sig = inspect.signature(func)
    annotations = func.__annotations__
    if not annotations:
        raise ValueError(
            "Функция должна иметь аннотации типов для всех аргументов и возвращаемого значения"
        )

    def wrapper(*args, **kwargs):
        bound_args = sig.bind(*args, **kwargs)
        for name, value in bound_args.arguments.items():
            param = sig.parameters[name]
            if not isinstance(value, param.annotation):
                raise TypeError(
                    f"Аргумент '{name}' должен быть {param.annotation}, а не {type(value)}"
                )
        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    """
    Суммирует два числа.
    :param a: Первое целое число
    :param b: Второе целое число
    :return: Сумма двух чисел
    """
    return a + b


if __name__ == "__main__":
    print(sum_two(1, 2))  # OK
    print(sum_two(1, 2.4))  # вызовет TypeError при прямом запуске
