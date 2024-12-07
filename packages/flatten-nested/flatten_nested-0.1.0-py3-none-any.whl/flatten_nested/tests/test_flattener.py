import unittest
from flatten_nested import flatten
from flatten_nested.exceptions import UnsupportedTypeError

class TestFlattener(unittest.TestCase):
    def test_flatten_list(self):
        nested_list = [1, [2, 3, [4, 5]], 6]
        self.assertEqual(flatten(nested_list), [1, 2, 3, 4, 5, 6])

    def test_flatten_tuple(self):
        nested_tuple = (1, (2, 3, (4, 5)), 6)
        self.assertEqual(flatten(nested_tuple), [1, 2, 3, 4, 5, 6])

    def test_flatten_dict(self):
        nested_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        expected = [('a', 1), ('b.c', 2), ('b.d.e', 3)]
        self.assertEqual(flatten(nested_dict), expected)

    def test_flatten_set(self):
        nested_set = {1, frozenset({2, 3}), 4}
        self.assertEqual(sorted(flatten(nested_set)), [1, 2, 3, 4])

    def test_flatten_mixed(self):
        mixed = {'a': [1, 2, (3, 4)], 'b': {5, 6}}
        self.assertEqual(
            sorted(flatten(mixed, keep_dict_keys=False)),
            [1, 2, 3, 4, 5, 6]
        )

    def test_depth_limit(self):
        nested = [1, [2, [3, [4]]]]
        self.assertEqual(flatten(nested, depth=1), [1, 2, [3, [4]]])

    def test_invalid_input(self):
        with self.assertRaises(UnsupportedTypeError):
            flatten(lambda x: x)