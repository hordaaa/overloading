from types import UnionType, FunctionType
from typing import get_args, Optional


class NoRegisterArgumentError(Exception):
    ...


class OverloadDecorator:
    """
    Класс-декоратор, играющий роль перегрузчика функции по первому аргументу
    или по аннотации типа первого параметра функции.
    При этом перегружать функцию можно несколькими типами (передав в register несколько аргументов).
    """

    def __init__(self, default: FunctionType):
        """
        Дефолтная функция будет вызвана, если нет совпадений у зарегистрированных
        ранее функций или в нее не было передано аргументов
        """

        self.default = default
        self.validators = {}

    def __register_annotation(self, function: FunctionType):
        """Регистрирует аннотацию типа первого параметра фкнкции"""

        if function.__annotations__.values():
            if isinstance(datatype := list(function.__annotations__.values())[0], UnionType):
                self.validators[get_args(datatype)] = function
            else:
                self.validators[(datatype,)] = function
        return function

    def register(self, *datatype: FunctionType | type | tuple[type, ...]):
        """Регистрирует тип/ы данных для перегрузки функции"""

        if not datatype:
            raise NoRegisterArgumentError

        if isinstance(datatype[0], FunctionType):
            return self.__register_annotation(datatype[0])

        return lambda func: self(func, _is_main_call=False, _datatype=datatype)

    def __call__(self, *args, _is_main_call=True, _datatype=(), **kwargs):

        if _is_main_call:

            if not args or type(args[0]) not in sum(tuple(self.validators), start=()):
                return self.default(*args, **kwargs)

            for validators in tuple(self.validators)[::-1]:
                if type(args[0]) in validators:
                    return self.validators[validators](*args, **kwargs)

        self.validators[_datatype] = args[0]
        return args[0]


def overload(func: FunctionType) -> OverloadDecorator:
    """Декорирует функцию для ее перегрузки"""

    return OverloadDecorator(func)


if __name__ == "__main__":

    @overload
    def test():
        print("call default")

    @test.register(int)
    def _(a, b):
        print(a + b)

    @test.register
    def _(name: str):
        print(f"hello {name}!")

    @test.register
    def _(collection: tuple | list | set):
        print(type(collection))

    test(10, 5)
    test("denis")
    test(())
    test([])
    test()
