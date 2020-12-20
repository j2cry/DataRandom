import random


class DataRandom:
    symbols = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    __TYPE_NAMES = ('int', 'float', 'str', 'bool', 'NoneType', 'list', 'dict')

    FL_INT = 0x01
    FL_FLOAT = 0x02
    FL_STR = 0x04
    FL_BOOL = 0x08
    FL_NONE = 0x10

    FL_NUMERIC = FL_INT | FL_FLOAT  # 0x03
    FL_SIMPLE_WITHOUT_NONE = FL_INT | FL_FLOAT | FL_STR | FL_BOOL  # 0x0F
    FL_WITHOUT_COLLECTIONS = 0x1F

    FL_LIST = 0x20
    FL_DICT = 0x40
    FL_ALL = 0x7F

    # init object with defaults or selected params
    def __init__(self, int_bundle=(-1, 1), float_bundle=(-1, 1), round_digits=3, length=8, nested_level=1, elem_count=5,
                 nested_elem_count=10, flags=FL_SIMPLE_WITHOUT_NONE):
        try:
            self.__int_bundle = (min(int_bundle), max(int_bundle))
        except TypeError:
            self.__int_bundle = (-1, 1)

        try:
            self.__float_bundle = (min(float_bundle), max(float_bundle))
        except TypeError:
            self.__float_bundle = (-1, 1)

        self.__rd = round_digits
        self.__ln = length
        self.__level = nested_level
        self.__count = elem_count
        self.__nested_count = nested_elem_count
        self.__flags = flags
        self.__update_types()

    # modify generator parameters
    def set_param(self, int_bundle=None, float_bundle=None, round_digits=None, length=None, nested_level=None,
                  elem_count=None, nested_elem_count=None, flags=None):
        try:
            self.__int_bundle = (min(int_bundle), max(int_bundle)) if int_bundle else self.__int_bundle
        except TypeError:
            pass

        try:
            self.__float_bundle = (min(float_bundle), max(float_bundle)) if float_bundle else self.__float_bundle
        except TypeError:
            pass

        self.__float_bundle = (min(float_bundle), max(float_bundle)) if float_bundle else self.__float_bundle
        self.__rd = round_digits if round_digits else self.__rd
        self.__ln = length if length else self.__ln
        self.__level = nested_level if nested_level else self.__level
        self.__count = elem_count if elem_count else self.__count
        self.__nested_count = nested_elem_count if nested_elem_count else self.__nested_count
        self.__flags = flags if flags else self.__flags
        self.__update_types()

    def __update_types(self):
        # напихиваем в словарь названия типов
        self.__types = []
        if self.__flags & self.FL_INT != 0:
            self.__types.append(self.__TYPE_NAMES[0])  # int
        if self.__flags & self.FL_FLOAT != 0:
            self.__types.append(self.__TYPE_NAMES[1])  # float
        if self.__flags & self.FL_STR != 0:
            self.__types.append(self.__TYPE_NAMES[2])  # str
        if self.__flags & self.FL_BOOL != 0:
            self.__types.append(self.__TYPE_NAMES[3])  # bool
        if self.__flags & self.FL_NONE != 0:
            self.__types.append(self.__TYPE_NAMES[4])  # NoneType
        if (self.__flags & self.FL_LIST) != 0:
            self.__types.append(self.__TYPE_NAMES[5])  # list
        if (self.__flags & self.FL_DICT) != 0:
            self.__types.append(self.__TYPE_NAMES[6])  # dict

    # set random sign for numeric
    @staticmethod
    def random_sign(num):
        if isinstance(num, int) or isinstance(num, float):
            return num if random.randint(0, 1) else -num
        else:
            return None

    # Returns random int, float, str, bool or None
    def random_primitive(self):
        if not self.__flags:
            return None

        # Random type of value
        tp = random.choice(self.__types)

        # Random value of needed type
        if tp == self.__TYPE_NAMES[0]:      # int
            r = random.randint(self.__int_bundle[0], self.__int_bundle[1])
        elif tp == self.__TYPE_NAMES[1]:    # float
            n = random.randint(self.__float_bundle[0], self.__float_bundle[1])
            r = random.random()
            r = round(n + r, self.__rd) if n + r <= self.__float_bundle[1] else round(n - r, self.__rd)
        elif tp == self.__TYPE_NAMES[2]:    # str
            r = ''.join([random.choice(list(self.symbols)) for i in range(self.__ln)])
        elif tp == self.__TYPE_NAMES[3]:    # bool
            r = bool(random.randint(0, 1))
        elif tp == self.__TYPE_NAMES[4]:    # None
            r = None
        else:  # set as None if type = list or dict
            r = None
        return r

    # Returns random list with nested lists according to nesting level; level=0 returns list with primitives
    # level=-2 runs method with non-object based parameter 'nested_level'
    def random_list(self, nested=False):
        res = []
        # checking if is running for nested
        items_count = self.__nested_count if nested else self.__count
        for i in range(items_count):
            if self.__level:
                self.__level -= 1
                res.append(self.random_list(True))
                self.__level += 1
            else:
                res.append(self.random_primitive())
        return res

    # TODO: Returns random list with primitives, lists and dicts
    def random_data(self, nested=False):
        pass


if __name__ == '__main__':
    a = DataRandom(float_bundle=(-3, 3), flags=DataRandom.FL_FLOAT)
    print(a.random_list())
    pass
