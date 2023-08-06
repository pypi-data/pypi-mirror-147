from abc import ABC
from abc import abstractmethod
from properties_loader.inmutables import _Params


class GenericConstructorInterface(ABC):
    _root_path: str
    _path_file: str
    _kwargs: dict

    @abstractmethod
    def __init__(self, root_path: str, path_file: str, **kwargs):
        self._root_path = root_path
        self._path_file = path_file
        self._kwargs: dict = {str(_Params.ROOT_PATH): root_path, str(_Params.PATH_FILE): path_file} | kwargs

    @property
    @abstractmethod
    def kwargs(self) -> dict:
        raise NotImplemented

    @property
    @abstractmethod
    def root_path(self) -> str:
        raise NotImplemented

    @property
    @abstractmethod
    def path_file(self) -> str:
        raise NotImplemented


class LoadConfigInterface(GenericConstructorInterface):

    @abstractmethod
    def __init__(self, root_path: str, path_file: str, **kwargs):
        super(LoadConfigInterface, self).__init__(root_path, path_file, **kwargs)
    
    @property
    @abstractmethod
    def path_properties(self) -> str:
        raise NotImplemented


class PropertiesInterface(GenericConstructorInterface):

    @abstractmethod
    def __init__(self, root_path: str, path_file: str, **kwargs):
        super(LoadConfigInterface, self).__init__(root_path, path_file, **kwargs)

    @property
    @abstractmethod
    def __dict__(self) -> dict:
        raise NotImplemented


