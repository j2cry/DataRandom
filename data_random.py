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
        self.__set_bundle(int_bundle)
        self.__set_bundle(float_bundle)

        self.__rd = round_digits
        self.__ln = length
        self.__level = nested_level
        self.__count = elem_count
        self.__nested_count = nested_elem_count
        self.__types = types if isinstance(types, Iterable) else [types]

    def set_param(self, int_bundle: (int, int) = None, float_bundle: (float, float) = None, round_digits=None,
                  length=None, nested_level=None, elem_count=None, nested_elem_count=None, types=None):
        """ Modify randomization parameters """
        self.__set_bundle(int_bundle)
        self.__set_bundle(float_bundle)

        self.__rd = round_digits if round_digits else self.__rd
        self.__ln = length if length else self.__ln
        self.__level = nested_level if nested_level else self.__level
        self.__count = elem_count if elem_count else self.__count
        self.__nested_count = nested_elem_count if nested_elem_count else self.__nested_count

        types = types if isinstance(types, Iterable) else [types]
        self.__types = types if types else self.__types

    def __set_bundle(self, bundle: tuple):
        """ Set bundles for int / float randomization (depends on values in bundle) """
        if isinstance(bundle, Iterable):
            if all(isinstance(value, int) for value in bundle):         # set int bundle
                self.__int_bundle = (min(bundle), max(bundle))
            elif all(isinstance(value, float) for value in bundle):     # set float bundle
                self.__float_bundle = (min(bundle), max(bundle))
            else:       # set defaults if bundle is iterable with non-numeric elements
                self.__int_bundle = (-1, 1)
                self.__float_bundle = (-1, 1)

    @staticmethod
    def random_sign(num):
        """ Set random sign for given numeric """
        if isinstance(num, int) or isinstance(num, float):
            return num if randint(0, 1) else -num
        else:
            return None

    def random_primitive(self, target_type=None):
        """ Returns random value of acceptable type (set in .__types) : int, float, str, bool or None """
        if not self.__types:
            return None

        # Random type of value if it isn't set directly
        tp = target_type if target_type else choice(self.__types)
        if tp is int:           # generate int
            r = randint(self.__int_bundle[0], self.__int_bundle[1])
        elif tp is float:       # generate float
            n = randint(self.__float_bundle[0], self.__float_bundle[1])
            r = random()
            r = round(n + r, self.__rd) if n + r <= self.__float_bundle[1] else round(n - r, self.__rd)
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


# debug
if __name__ == '__main__':
    a = DataRandom(float_bundle=(-3.0, 3.0), nested_level=1, elem_count=4, nested_elem_count=3, types=(float, str))

    # pattern = [str, int, float, float, bool, [float, float, str]]
    # pattern = [float, {0: float, 3: [float, {0: str, 1: str}], 'text': str, 4: bool}]
    pattern = [{0: str, 1: [float, float], 2: bool}, {0: str, 1: [int, int], 2: bool}, {0: str, 1: float, 2: bool}]
    # print(pattern)
    # data = a.random_by_model(pattern)
    # data = a.random_dict()

    # gen = a.generator()
    # res = []
    # try:
    #     value = next(gen)
    #     res.append(value)
    #     if isinstance(value, Generator):
    #         print('yeah')
    #     while value:
    #         value = next(gen)
    #         res.append(value)
    # except StopIteration:
    #     pass
    # print(res)
    data = a.random_list()
    numbers = DataRandom(int_bundle=(-10, 10), elem_count=40, types=int, nested_level=0).random_list()

    print(numbers)
