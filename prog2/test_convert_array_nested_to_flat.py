import pytest

from prog2.convert_array_nested_to_flat import array_nested_to_flat, exception_type_value


@pytest.mark.parametrize('nested_array, expected', [
    ([[1, 2, [3]], 4], [1, 2, 3, 4]),
    ([[[1, [2]], [3]], 4], [1, 2, 3, 4]),
    ([], []),
    ([-1, [2, [0, 3]]], [-1, 2, 0, 3]),
    (2, TypeError),
    ('A', TypeError),
    ([1.5, 1], TypeError),
    ([1, ['A'], 1, ['2', 4]], TypeError),
    ([[], [], [], [1]], [1]),
])
def test_array_nested_to_flat(nested_array, expected):
    if expected == TypeError:
        with pytest.raises(TypeError):
            array_nested_to_flat(nested_array)
    else:
        assert array_nested_to_flat(nested_array) == expected


@pytest.mark.parametrize('value, type_value, expected_exception', [
    (1.4, list, TypeError('invalid type, should be list but receive float')),
    (1, str, TypeError('invalid type, should be str but receive int')),
    ('A', int, TypeError('invalid type, should be int but receive str')),
])
def test_exception_type_value(value, type_value, expected_exception):
    error = exception_type_value(value, type_value)
    assert expected_exception.args[0] == error.args[0]
    assert type(error) == type(expected_exception)
