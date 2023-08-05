__version__ = "1.0.1"

import typing
from typing import Any, ClassVar, Dict, Optional, Union, ForwardRef

from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass

class UUIDAlreadyExists(Exception):
    uuid: str
    name: Optional[str]

    def __init__(self, uuid: str, name: Optional[str] = None):
        if name is not None:
            msg = f"Cannot register class '{name}' with UUID '{uuid}', as another class with this UUID is already registered"
        else:
            msg = f"Cannot register class with UUID '{uuid}' as another class with this UUID is already registered"
        super().__init__(msg)
        self.uuid = uuid
        self.name = name


class UUIDModelMetaclass(ModelMetaclass):

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        uuid_name = cls.__sub_classes__[None]
        if uuid_name not in kwargs:
            return super().__call__(*args, **kwargs)
        uuid = kwargs.pop(uuid_name)
        if uuid is not None:
            cls = cls.__sub_classes__[str(uuid)]
        return cls(*args, **kwargs)

    def __new__(mcs, name, bases, namespace, uuid_name: Optional[str] = None, base: bool = False, **kwargs):
        return super().__new__(mcs, name, bases, namespace, **kwargs)

    def __init__(cls, name, bases, namespace, uuid_name: Optional[str] = None, base: bool = False, **kwargs):
        if hasattr(cls, "__sub_classes__") and uuid_name is None and not base:
            uuid_name = cls.__sub_classes__[None]
            uuid = namespace.get(uuid_name, None)
            if uuid is not None:
                uuid = str(uuid)
                if uuid in cls.__sub_classes__:
                    raise UUIDAlreadyExists(uuid, name)
                cls.__sub_classes__[uuid] = cls
        else:
            uuid_name = uuid_name or "muuid"
            d = dict()
            d[None] = uuid_name
            setattr(cls, "__sub_classes__", d)


class UUIDBaseModel(BaseModel, metaclass=UUIDModelMetaclass):
    muuid: Optional[str]
    __sub_classes__: ClassVar[Dict[Optional[str], Union[str, "UUIDBaseModel"]]]

