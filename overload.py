from types import UnionType, FunctionType
from typing import get_args, NoReturn


class NoRegisterArgumentError(Exception):
    ...


class OverloadDecorator:
    """
    Класс-декоратор, играющий роль перегрузчика функции по первому аргументу
    или по аннотации типа первого параметра функции.
    При этом перегружать функцию можно несколькими типами (передав в register несколько аргументов).
    """

    def __init__(self, default: FunctionType) -> None:
        """
        Дефолтная функция будет вызвана, если нет совпадений у зарегистрированных
        ранее функций или в нее не было передано аргументов
        """

        self.default = default
        self.validators = {}

    def __register_with_annotation(self, function: FunctionType) -> FunctionType:
        """Регистрирует реализацию функции по аннотации типа первого параметра фкнкции"""

        if function.__annotations__.values():
            if isinstance(datatype := list(function.__annotations__.values())[0], UnionType):
                self.validators[get_args(datatype)] = function
            else:
                self.validators[(datatype,)] = function
        return function

    def __register_with_types(self, function: FunctionType, datatypes: tuple[type, ...]) -> FunctionType:
        """Регистрирует реализацию функции по переданным в register типам"""

        self.validators[datatypes] = function
        return function

    def register(self, *datatypes: FunctionType | type | tuple[type, ...]) -> NoReturn | FunctionType:
        """Регистрирует реализацию функции по переданным аргументам"""

        if not datatypes:
            raise NoRegisterArgumentError

        if isinstance(datatypes[0], FunctionType):
            return self.__register_with_annotation(datatypes[0])

        return lambda func: self.__register_with_types(func, datatypes=datatypes)

    def __call__(self, *args, _datatype=(), **kwargs) -> FunctionType:

        if not args or type(args[0]) not in sum(tuple(self.validators), start=()):
            return self.default(*args, **kwargs)

        for validators in tuple(self.validators)[::-1]:
            if type(args[0]) in validators:
                return self.validators[validators](*args, **kwargs)


def overload(function: FunctionType) -> OverloadDecorator:
    """Декорирует функцию для ее перегрузки"""

    return OverloadDecorator(function)


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
