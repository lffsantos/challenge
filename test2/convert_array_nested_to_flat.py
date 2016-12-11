import argparse
import json


def exception_type_value(value, type_value):
    return TypeError('invalid type, should be {} but receive {}'.format(
        type_value.__name__, type(value).__name__)
    )


def array_nested_to_flat(nested_array):
    """
    Flatten an array of arbitrarily nested arrays of integers into a flat array of
    integers. If has value other than integer or list, throw exception TypeError
    :param nested_array: e.g: [[1,2,[3]],4]
    :return: [1,2,3,4]
    """
    if not isinstance(nested_array, list):
        raise exception_type_value(nested_array, list)

    flat_array = []
    for value in nested_array:
        if not isinstance(value, list) and not isinstance(value, int):
            raise exception_type_value(value, type(value))

        if isinstance(value, list):
            flat_array.extend(array_nested_to_flat(value))
        else:
            flat_array.append(value)

    return flat_array


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Nested array in flat array')
    parser.add_argument('-a', '--array', default='[1, [2]]', help='Nested Array')
    args = parser.parse_args()
    try:
        nested_array = json.loads(args.array)
    except ValueError:
        raise ValueError('invalid format array')

    flat_array = array_nested_to_flat(nested_array)

    print('flat array : {}'.format(flat_array))
