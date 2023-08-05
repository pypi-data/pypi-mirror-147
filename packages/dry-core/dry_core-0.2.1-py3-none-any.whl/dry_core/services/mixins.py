import copy
from typing import Any, Optional, NamedTuple, Generic, TypeVar, Type, Union, Iterable
from uuid import UUID

from dry_core.selectors.generics import BaseSelector
from dry_core.services.decorators import pre, post

ServiceInstance = TypeVar('ServiceInstance')
BaseInstanceSelector = TypeVar('BaseInstanceSelector', bound=BaseSelector)


class BaseServiceMixin(Generic[ServiceInstance]):
    model: Type[ServiceInstance]

    def __init__(self, *args, **kwargs):
        self.validate_service_model_defined()
        self._stop_pre_operations: bool = False
        self._stop_main_operation: bool = False
        self._stop_post_operations: bool = False

    @property
    def pre_operations_stopped(self) -> bool:
        return self._stop_pre_operations

    @property
    def main_operation_stopped(self) -> bool:
        return self._stop_main_operation

    @property
    def post_operations_stopped(self) -> bool:
        return self._stop_post_operations

    def validate_service_model_defined(self) -> None:
        if self.model is None:
            raise AttributeError(f'Service class {self.__class__.__name__} must setup "model" field')

    def stop_operations(
            self,
            pre_operations: bool = True,
            main_operation: bool = True,
            post_operations: bool = True,
    ) -> None:
        if pre_operations:
            self.stop_pre_operations()
        if main_operation:
            self.stop_main_operation()
        if post_operations:
            self.stop_post_operations()

    def reset_stop_operations_flags(self) -> None:
        self._stop_pre_operations: bool = False
        self._stop_main_operation: bool = False
        self._stop_post_operations: bool = False

    def stop_pre_operations(self) -> None:
        self._stop_pre_operations = True

    def stop_main_operation(self) -> None:
        self._stop_main_operation = True

    def stop_post_operations(self) -> None:
        self._stop_post_operations = True

    def common_clear_after_action(self):
        self.reset_stop_operations_flags()


class ServiceInstanceMixin(BaseServiceMixin[ServiceInstance], Generic[ServiceInstance]):
    def __init__(self, instance: Optional[ServiceInstance] = None, *args, **kwargs):
        super(ServiceInstanceMixin, self).__init__(*args, **kwargs)
        self.validate_service_model_defined()
        # if instance don't set on higher level, like it can be in UUIDServiceMixin, try init it from arguments
        if getattr(self, 'instance', None) is None:
            self.instance: Optional[ServiceInstance] = instance

    def validate_instance_filled(self, validate_type: bool = True, raise_exception: bool = True) -> bool:
        if self.instance is None:
            if raise_exception:
                raise ValueError('{class_name} object field "instance" is None'.format(class_name=self.__class__.__name__))
            return False
        if validate_type:
            if not isinstance(self.instance, self.model):
                if raise_exception:
                    raise TypeError(
                        '{class_name} field "instance" is type {instance_type}, must be {service_instance_model}'.format(
                            class_name=self.__class__.__name__,
                            instance_type=self.instance.__class__.__name__,
                            service_instance_model=self.model.__name__,
                        )
                    )
                return False
        return True


class CreateServiceMixin(ServiceInstanceMixin[ServiceInstance], BaseServiceMixin[ServiceInstance], Generic[ServiceInstance]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._create_args: Optional[dict[str, Any]] = None
        self._post_create_args: Optional[dict[str, Any]] = None

    def pre_create(self, **kwargs):
        pre_create_funcs = pre.get_class_create_funcs(self.__class__)
        for func_info in pre_create_funcs:
            func_info.function_object(self, **kwargs)

    def prepare_create_arguments(self) -> None:
        pass

    def validate_create_arguments(self) -> bool:
        return True

    def extract_post_create_arguments(self) -> None:
        self._post_create_args = {}

    def create(self, **kwargs) -> ServiceInstance:
        self._create_args = copy.deepcopy(kwargs)
        self.extract_post_create_arguments()
        self.prepare_create_arguments()
        self.validate_create_arguments()
        if not self.pre_operations_stopped:
            self.pre_create(**self._create_args)
        if not self.main_operation_stopped:
            self.instance_create(**self._create_args)
        if not self.post_operations_stopped:
            self.post_create(**self._post_create_args)
        self._cleanup_after_create()
        return self.instance

    def instance_create(self, **kwargs) -> ServiceInstance:
        if self.model:
            self.instance = self.model(**kwargs)
        else:
            raise NotImplementedError('Set service class "model" attribute or implement "instance_create" method')
        return self.instance

    def post_create(self, **kwargs) -> None:
        post_create_funcs = post.get_class_create_funcs(self.__class__)
        for func_info in post_create_funcs:
            func_info.function_object(self, **kwargs)

    def _cleanup_after_create(self):
        self.common_clear_after_action()
        self._post_create_args = None


class UpdateServiceMixin(ServiceInstanceMixin[ServiceInstance], BaseServiceMixin[ServiceInstance], Generic[ServiceInstance]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._update_args: Optional[dict[str, Any]] = None
        self._post_update_args: Optional[dict[str, Any]] = None

    def pre_update(self, **kwargs):
        pre_update_funcs = pre.get_class_update_funcs(self.__class__)
        for func_info in pre_update_funcs:
            func_info.function_object(self, **kwargs)

    def prepare_update_arguments(self) -> None:
        pass

    def validate_update_arguments(self) -> bool:
        return True

    def extract_post_update_arguments(self) -> None:
        self._post_update_args = {}

    def update(self, **kwargs) -> ServiceInstance:
        if (instance := kwargs.get('instance', None)) is not None:
            setattr(self, 'instance', instance)
        self.validate_instance_filled()

        self._update_args = copy.deepcopy(kwargs)
        self.extract_post_update_arguments()
        self.prepare_update_arguments()
        self.validate_update_arguments()
        if not self.pre_operations_stopped:
            self.pre_update(**self._update_args)
        if not self.main_operation_stopped:
            self.instance_update(**self._update_args)
        if not self.post_operations_stopped:
            self.post_update(**self._post_update_args)
        self._cleanup_after_update()
        return self.instance

    def instance_update(self, **kwargs) -> ServiceInstance:
        for attr, value in kwargs.items():
            if hasattr(self.instance, attr):
                setattr(self.instance, attr, value)
        return self.instance

    def post_update(self, **kwargs) -> None:
        post_update_funcs = post.get_class_update_funcs(self.__class__)
        for func_info in post_update_funcs:
            func_info.function_object(self, **kwargs)

    def _cleanup_after_update(self):
        self.common_clear_after_action()
        self._post_update_args = None


class DestroyServiceMixin(ServiceInstanceMixin[ServiceInstance], BaseServiceMixin[ServiceInstance], Generic[ServiceInstance]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._destroy_args: Optional[dict[str, Any]] = None
        self._post_destroy_args: Optional[dict[str, Any]] = None

    def pre_destroy(self, **kwargs):
        pre_destroy_funcs = pre.get_class_destroy_funcs(self.__class__)
        for func_info in pre_destroy_funcs:
            func_info.function_object(self, **kwargs)

    def prepare_destroy_arguments(self) -> None:
        pass

    def validate_destroy_arguments(self) -> bool:
        return True

    def extract_post_destroy_arguments(self) -> None:
        self._post_destroy_args = {}

    def destroy(self, **kwargs) -> Optional[ServiceInstance]:
        if (instance := kwargs.get('instance', None)) is not None:
            setattr(self, 'instance', instance)
        self.validate_instance_filled()

        self._destroy_args = copy.deepcopy(kwargs)
        self.extract_post_destroy_arguments()
        self.prepare_destroy_arguments()
        self.validate_destroy_arguments()
        if not self.pre_operations_stopped:
            self.pre_destroy(**self._destroy_args)
        if not self.main_operation_stopped:
            self.instance_destroy(**self._destroy_args)
        if not self.post_operations_stopped:
            self.post_destroy(**self._post_destroy_args)
        self._cleanup_after_destroy()
        instance = self.instance
        self.instance = None
        return instance

    def instance_destroy(self, **kwargs) -> Optional[ServiceInstance]:
        pass

    def post_destroy(self, **kwargs) -> None:
        post_destroy_funcs = post.get_class_destroy_funcs(self.__class__)
        for func_info in post_destroy_funcs:
            func_info.function_object(self, **kwargs)

    def _cleanup_after_destroy(self):
        self.common_clear_after_action()
        self._post_destroy_args = None


class UUIDServiceInstanceMixin(ServiceInstanceMixin[ServiceInstance], Generic[ServiceInstance]):
    selector: Type[BaseInstanceSelector]
    selector_get_by_uuid_method_name: str = 'get_by_uuid'
    selector_get_by_uuid_param_name: str = 'uuid'

    def __init__(self, *args, uuid: Optional[Union[UUID, str]] = None, **kwargs):
        if self.selector is None:
            raise AttributeError(f'"selector" class attr must be defined for {self.__class__}')
        if getattr(self.selector, self.selector_get_by_uuid_method_name, None) is None:
            raise AttributeError(f'"selector" class must have method "{self.selector_get_by_uuid_method_name}"')
        if uuid is not None:
            if isinstance(uuid, UUID):
                uuid = str(uuid)
            self.instance: ServiceInstance = getattr(self.selector, self.selector_get_by_uuid_method_name)(
                **{self.selector_get_by_uuid_param_name: uuid})
        super(UUIDServiceInstanceMixin, self).__init__(*args, **kwargs)
