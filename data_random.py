from random import random, randint, choice, choices
from string import ascii_letters, digits, punctuation
from collections.abc import Iterable, Generator


class DataRandom:
    symbols = ascii_letters + digits + punctuation

    NUMERIC = (int, float)
    SIMPLE_WITHOUT_NONE = (int, float, str, bool)
    WITHOUT_COLLECTIONS = (int, float, str, bool, None)

    def __init__(self, int_bundle: (int, int) = (-1, 1), float_bundle: (float, float) = (-1.0, 1.0), round_digits=3,
                 length=8, nested_level=1, elem_count=5, nested_elem_count=10, types=NUMERIC):
        """ Initialize randomization object with defaults or selected parameters """
        self.__rd = round_digits
        self.__set_bundle(int_bundle)
        self.__set_bundle(float_bundle)

        self.__ln = length
        self.__level = nested_level
        self.__count = elem_count
        self.__nested_count = nested_elem_count
        self.__set_types(types)

    def set_param(self, int_bundle: (int, int) = None, float_bundle: (float, float) = None, round_digits=None,
                  length=None, nested_level=None, elem_count=None, nested_elem_count=None, types=None):
        """ Modify randomization parameters """
        self.__rd = round_digits if round_digits else self.__rd
        self.__set_bundle(int_bundle)
        self.__set_bundle(float_bundle)

        self.__ln = length if length else self.__ln
        self.__level = nested_level if nested_level else self.__level
        self.__count = elem_count if elem_count else self.__count
        self.__nested_count = nested_elem_count if nested_elem_count else self.__nested_count
        self.__set_types(types)

    def __set_bundle(self, bundle: (int, int) or (float, float)):
        """ Set bundles for int / float randomization (depends on values in bundle) """
        if isinstance(bundle, Iterable):
            if all(isinstance(value, int) for value in bundle):         # set int bundle
                self.__int_bundle = (min(bundle), max(bundle))
            elif all(isinstance(value, float) for value in bundle):     # set float bundle
                self.__float_bundle = (round(min(bundle), self.__rd), round(max(bundle), self.__rd))
            else:       # set defaults if bundle is iterable with non-numeric elements
                self.__int_bundle = (-1, 1)
                self.__float_bundle = (-1.0, 1.0)

    def __set_types(self, types):
        """ Set types for randomization and transpose to Iterable if required """
        if isinstance(types, Iterable) and not isinstance(types, str):
            self.__types = types
        else:
            self.__types = tuple([types])

    @property
    def types(self):
        return self.__types

    def random_primitive(self, target_type=None):
        """ Returns random value of acceptable type (set in .__types) : int, float, str, bool or None """
        if not self.__types:
            return None

        # Random type of value if it isn't set directly
        tp = target_type if target_type else choice(self.__types)
        if tp is int:           # generate int
            r = randint(self.__int_bundle[0], self.__int_bundle[1])

        elif tp is float:       # generate float
            # generate correct range
            available_range = sum(map(abs, self.__float_bundle))
            r = round(available_range * random() - abs(self.__float_bundle[0]), self.__rd)

        elif tp is str:         # generate str
            r = ''.join(choices(self.symbols, k=self.__ln))

        elif tp is bool:        # generate bool
            r = bool(randint(0, 1))

        elif tp is None:        # generate NoneType
            r = None
        else:                   # NOTE: you can add your own class here
            r = None
        return r

    def generate_list(self, nested=False):
        """ Returns generator of random values with nested lists according to nesting level;
            level=0 returns list with primitives (int, float, str, bool or None) """
        # checking if is running for nested
        items_count = self.__nested_count if nested else self.__count
        for i in range(items_count):
            if self.__level:
                self.__level -= 1
                yield self.generate_list(True)
                self.__level += 1
            else:
                yield self.random_primitive()

    def random_list(self, generator: Generator = None):
        """ Returns list of random values with nested lists according to nesting level;
            level=0 returns list with primitives (int, float, str, bool or None) """
        res = []
        generator = self.generate_list() if not generator else generator
        for element in generator:
            if isinstance(element, Generator):
                res.append(self.random_list(element))
            else:
                res.append(element)
        return res

    def random_dict(self, nested=False):
        """ Generate dictionary with actual parameters """
        items_count = self.__nested_count if nested else self.__count
        dictionary = {}
        for i in range(items_count):
            dictionary[i] = self.random_primitive()
        return dictionary

    def random_by_model(self, model):
        """ Returns list of random values according to model structure
            model looks like this in any combinations
            [{0: str, 1: [float, float], 2: bool}, {0: str, 1: [int, int], 2: bool}, {0: str, 1: float, 2: bool}] or
            {0: float, 1: float, 2: [bool, str], 3: [{0: float, 1: float}, {0: str, 1: str}] } """
        if isinstance(model, dict):
            dictionary = dict()
            for key, value in model.items():
                random_value = self.random_by_model(value) if isinstance(value, Iterable) \
                    else self.random_primitive(value)
                dictionary[key] = random_value
            return dictionary
        if isinstance(model, Iterable):
            collection = []
            for element in model:
                collection.append(self.random_by_model(element))
            return collection
        else:
            return self.random_primitive(model)


def random_sign(num):
    """ Set random sign for given numeric """
    if isinstance(num, int) or isinstance(num, float):
        return num if randint(0, 1) else -num
    else:
        return None


def expand_nested(source) -> Iterable:
    """ Generator expands all nested values to non-nested iterable
        str expands as whole str (without per char expanding) """
    for element in source:
        if isinstance(element, Iterable) and not isinstance(element, str):
            yield from expand_nested(element)
        else:
            yield element


# debug
if __name__ == '__main__':
    from itertools import chain
    data = DataRandom(float_bundle=(-3.0, 3.0), nested_level=2, elem_count=4, nested_elem_count=3, types=float)

    # pattern = [str, int, float, float, bool, [float, float, str]]
    # pattern = [float, {0: float, 3: [float, {0: str, 1: str}], 'text': str, 4: bool}]
    # pattern = [{0: str, 1: [float, float], 2: bool}, {0: str, 1: [int, int], 2: bool}, {0: str, 1: float, 2: bool}]

    numbers = data.random_list()
    print(numbers)

    # dbg = check_nested_values(numbers, lambda b: isinstance(b, data.types))
    # print(dbg)
