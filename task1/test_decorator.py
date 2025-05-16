import unittest

from task1.solution import strict


# Функции для тестирования
@strict
def add(a: int, b: int) -> int:
    return a + b


@strict
def concat(a: str, b: str) -> str:
    return a + b


@strict
def logic_and(a: bool, b: bool) -> bool:
    return a and b


class TestStrictDecorator(unittest.TestCase):
    def test_add_correct(self):
        self.assertEqual(add(1, 2), 3)

    def test_add_incorrect_type(self):
        with self.assertRaises(TypeError):
            add(1, 2.0)

    def test_concat_correct(self):
        self.assertEqual(concat("foo", "bar"), "foobar")

    def test_concat_incorrect(self):
        with self.assertRaises(TypeError):
            concat("foo", 123)

    def test_logic_and_correct(self):
        self.assertTrue(logic_and(True, True))

    def test_logic_and_incorrect(self):
        with self.assertRaises(TypeError):
            logic_and(True, "False")

    def test_missing_annotations(self):
        def unannotated(a, b):
            return a + b

        with self.assertRaises(ValueError):
            strict(unannotated)


if __name__ == "__main__":
    unittest.main()
