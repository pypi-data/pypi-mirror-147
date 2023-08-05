import copy
from dataclasses import dataclass
from typing import Callable, Optional, Type


@dataclass
class FunctionInformation:
    function_object: Callable
    order: Optional[int] = None


_BASE_DICT_CREATE_FUNCS_KEY: str = 'create'
_BASE_DICT_UPDATE_FUNCS_KEY: str = 'update'
_BASE_DICT_DESTROY_FUNCS_KEY: str = 'destroy'
_BASE_CLASS_FUNCS_DICT: dict[str, list[FunctionInformation]] = {
    _BASE_DICT_CREATE_FUNCS_KEY: [],
    _BASE_DICT_UPDATE_FUNCS_KEY: [],
    _BASE_DICT_DESTROY_FUNCS_KEY: []
}


class _base_service_decorator:  # noqa
    @staticmethod
    def get_method_class_identifier(method: Callable) -> str:
        class_name = method.__qualname__.split('.')[0]
        return f'{method.__module__}.{class_name}'  # noqa

    @staticmethod
    def get_class_identifier(class_obj: Type) -> str:
        class_name = class_obj.__qualname__
        return f'{class_obj.__module__}.{class_name}'


class pre(_base_service_decorator):  # noqa
    """
    Decorators collection for automatic running pre-operation functions
    """
    __classes: dict[str, dict[str, list[FunctionInformation]]] = {}

    @classmethod
    def get_class_funcs_by_identifier(cls, class_identifier: str) -> dict[str, list[FunctionInformation]]:
        if (res := cls.__classes.get(class_identifier, None)) is None:
            res = cls.__classes[class_identifier] = copy.deepcopy(_BASE_CLASS_FUNCS_DICT)
        return res

    @classmethod
    def get_class_funcs(cls, class_obj) -> dict[str, list[FunctionInformation]]:
        identifier = cls.get_class_identifier(class_obj)
        return cls.get_class_funcs_by_identifier(identifier)

    @classmethod
    def get_class_funcs_by_method(cls, method: Callable) -> dict[str, list[FunctionInformation]]:
        identifier = cls.get_method_class_identifier(method)
        return cls.get_class_funcs_by_identifier(identifier)

    # Pre-create decorators functional

    @classmethod
    def create(cls, original_function):
        funcs_list = cls.get_class_funcs_by_method(original_function)[_BASE_DICT_CREATE_FUNCS_KEY]
        funcs_list.append(FunctionInformation(
            function_object=original_function,
        ))
        return original_function

    @classmethod
    def get_class_create_funcs(cls, class_obj) -> list[FunctionInformation]:
        return cls.get_class_funcs(class_obj)[_BASE_DICT_CREATE_FUNCS_KEY]

    @classmethod
    def get_class_create_funcs_by_method(cls, method: Callable) -> list[FunctionInformation]:
        return cls.get_class_funcs_by_method(method)[_BASE_DICT_CREATE_FUNCS_KEY]

    # Pre-update decorators functional

    @classmethod
    def update(cls, original_function, ):
        funcs_list = cls.get_class_funcs_by_method(original_function)[_BASE_DICT_UPDATE_FUNCS_KEY]
        funcs_list.append(FunctionInformation(
            function_object=original_function,
        ))
        return original_function

    @classmethod
    def get_class_update_funcs(cls, class_obj) -> list[FunctionInformation]:
        return cls.get_class_funcs(class_obj)[_BASE_DICT_UPDATE_FUNCS_KEY]

    @classmethod
    def get_class_update_funcs_by_method(cls, method: Callable) -> list[FunctionInformation]:
        return cls.get_class_funcs_by_method(method)[_BASE_DICT_UPDATE_FUNCS_KEY]

    # Pre-destroy decorators functional

    @classmethod
    def destroy(cls, original_function, ):
        funcs_list = cls.get_class_funcs_by_method(original_function)[_BASE_DICT_DESTROY_FUNCS_KEY]
        funcs_list.append(FunctionInformation(
            function_object=original_function,
        ))
        return original_function

    @classmethod
    def get_class_destroy_funcs(cls, class_obj) -> list[FunctionInformation]:
        return cls.get_class_funcs(class_obj)[_BASE_DICT_DESTROY_FUNCS_KEY]

    @classmethod
    def get_class_destroy_funcs_by_method(cls, method: Callable) -> list[FunctionInformation]:
        return cls.get_class_funcs_by_method(method)[_BASE_DICT_DESTROY_FUNCS_KEY]

class post(_base_service_decorator):  # noqa
    """
    Decorators collection for automatic running pre-operation functions
    """
    __classes: dict[str, dict[str, list[FunctionInformation]]] = {}

    @classmethod
    def get_class_funcs_by_identifier(cls, class_identifier: str) -> dict[str, list[FunctionInformation]]:
        if (res := cls.__classes.get(class_identifier, None)) is None:
            res = cls.__classes[class_identifier] = copy.deepcopy(_BASE_CLASS_FUNCS_DICT)
        return res

    @classmethod
    def get_class_funcs(cls, class_obj) -> dict[str, list[FunctionInformation]]:
        identifier = cls.get_class_identifier(class_obj)
        return cls.get_class_funcs_by_identifier(identifier)

    @classmethod
    def get_class_funcs_by_method(cls, method: Callable) -> dict[str, list[FunctionInformation]]:
        identifier = cls.get_method_class_identifier(method)
        return cls.get_class_funcs_by_identifier(identifier)

    # Pre-create decorators functional

    @classmethod
    def create(cls, original_function):
        funcs_list = cls.get_class_funcs_by_method(original_function)[_BASE_DICT_CREATE_FUNCS_KEY]
        funcs_list.append(FunctionInformation(
            function_object=original_function,
        ))
        return original_function

    @classmethod
    def get_class_create_funcs(cls, class_obj) -> list[FunctionInformation]:
        return cls.get_class_funcs(class_obj)[_BASE_DICT_CREATE_FUNCS_KEY]

    @classmethod
    def get_class_create_funcs_by_method(cls, method: Callable) -> list[FunctionInformation]:
        return cls.get_class_funcs_by_method(method)[_BASE_DICT_CREATE_FUNCS_KEY]

    # Pre-update decorators functional

    @classmethod
    def update(cls, original_function, ):
        funcs_list = cls.get_class_funcs_by_method(original_function)[_BASE_DICT_UPDATE_FUNCS_KEY]
        funcs_list.append(FunctionInformation(
            function_object=original_function,
        ))
        return original_function

    @classmethod
    def get_class_update_funcs(cls, class_obj) -> list[FunctionInformation]:
        return cls.get_class_funcs(class_obj)[_BASE_DICT_UPDATE_FUNCS_KEY]

    @classmethod
    def get_class_update_funcs_by_method(cls, method: Callable) -> list[FunctionInformation]:
        return cls.get_class_funcs_by_method(method)[_BASE_DICT_UPDATE_FUNCS_KEY]

    # Pre-destroy decorators functional

    @classmethod
    def destroy(cls, original_function, ):
        funcs_list = cls.get_class_funcs_by_method(original_function)[_BASE_DICT_DESTROY_FUNCS_KEY]
        funcs_list.append(FunctionInformation(
            function_object=original_function,
        ))
        return original_function

    @classmethod
    def get_class_destroy_funcs(cls, class_obj) -> list[FunctionInformation]:
        return cls.get_class_funcs(class_obj)[_BASE_DICT_DESTROY_FUNCS_KEY]

    @classmethod
    def get_class_destroy_funcs_by_method(cls, method: Callable) -> list[FunctionInformation]:
        return cls.get_class_funcs_by_method(method)[_BASE_DICT_DESTROY_FUNCS_KEY]
