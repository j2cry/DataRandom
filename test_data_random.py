from data_random import DataRandom, expand_nested


def check_values(source, func):
    """ Testing values with func. Return True if all func(source) are True """
    return all(func(result) for result in expand_nested(source))


def test_single_type_gen_list():
    source = DataRandom(int_bundle=(-5, 7), float_bundle=(-0.5, 1.0), elem_count=20, types=float, nested_level=0)
    data = source.random_list()
    assert check_values(data, lambda b: isinstance(b, source.types))


def test_multi_type_gen_list():
    source = DataRandom(int_bundle=(-5, 7), float_bundle=(-0.5, 1.0), elem_count=20, types=(float, int, bool),
                        nested_level=0)
    data = source.random_list()
    assert check_values(data, lambda b: isinstance(b, source.types))
