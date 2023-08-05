from typing import Generic, TypeVar

from . import mixins

ServiceInstance = TypeVar('ServiceInstance')


class BaseService(
    mixins.CreateServiceMixin[ServiceInstance],
    mixins.UpdateServiceMixin[ServiceInstance],
    mixins.DestroyServiceMixin[ServiceInstance],
    Generic[ServiceInstance]
):
    pass


class UUIDService(
    mixins.UUIDServiceInstanceMixin[ServiceInstance],
    BaseService[ServiceInstance],
    Generic[ServiceInstance]
):
    pass
