import os
from os.path import exists
from configparser import ConfigParser
from properties_loader.inmutables import _EnvVars, _Params
from properties_loader.inmutables import _DfValues
from properties_loader.inmutables import _PriorityProperties
from properties_loader.interfaces import LoadConfigInterface
from properties_loader.interfaces import PropertiesInterface
from properties_loader.exceptions import PropertiesNotFoundError


class LoadConfig(LoadConfigInterface):
    """
        Esta clase se encarga de cargar correctamente por orden de prioridad
        los parametros o variables de entornos para cargar las propiedades
        Prioridades:
            1 - Paso por parametros
            2 - Variables de entrno
            3 - Valores por defecto
    """

    _priority: int = 0
    _kwargs: dict
    _root_path: str
    _path_file: str

    def __init__(self, root_path: str = None, path_file: str = None, **kwargs):
        """
            Evalua el orden de prioridad de carga del archivo de configuración
        """
        super(LoadConfig, self).__init__(root_path=root_path, path_file=path_file, **kwargs)
        self.__load_parameters()
        if self._priority == 0:
            self.__load_env_vars()
        if self._priority == 0:
            self.__load_default()
        if self._priority == 0:
            raise PropertiesNotFoundError(path_file)

    def __load_parameters(self):
        """
           Evalua si vienen la dirección del archivo de configuración viene por parametros
           y comprueba si dichar direccion es valida
        """
        root_path = self._root_path
        path_file = self._path_file
        if root_path and path_file and self.__check_properties():
            self._priority = int(_PriorityProperties.PARAMS)

    def __load_env_vars(self):
        """
           Evalua si vienen la dirección del archivo de configuración viene por variables de entorno
           y comprueba si dichar direccion es valida
        """
        self._root_path = os.getenv(_EnvVars.ROOT_PATH)
        self._path_file = os.getenv(_EnvVars.CONFIG_FILE)
        root_path = self._root_path
        path_file = self._path_file
        if root_path and path_file and self.__check_properties():
            self._priority = int(_PriorityProperties.ENVS_VARS)

    def __load_default(self):
        """
           Evalua si el archivo de configuracion se encuentra en el lugar por defecto
           root_path: La ruta relativa al archivo.py que fue ejecutado
           path_file: properties.ini
           Si no lanza un error indicando la ubicacion del archivo que se esta buscando e indicando que no
           fue encontrado
        """
        self._root_path = _DfValues.DF_ROOT_PATH
        self._path_file = _DfValues.DF_PATH_FILE
        if self.__check_properties():
            self._priority = int(_PriorityProperties.ENVS_VARS)
        else:
            path_file: str = f"{self._root_path}/{self._path_file}"
            raise PropertiesNotFoundError(path_file)

    def __check_properties(self):
        return exists(f'{self.root_path}/{self.path_file}')

    @property
    def path_properties(self):
        return f'{self.root_path}/{self.path_file}'

    @property
    def root_path(self):
        return self._root_path

    @property
    def path_file(self):
        return self._path_file

    @property
    def priority(self):
        return self._priority

    @property
    def kwargs(self) -> dict:
        return self._kwargs


class Properties(PropertiesInterface, LoadConfig):
    """
        Esta clase se encarga de convertir el archivo de configuración en un dict de python
    """

    _root_path: str
    _path_file: str

    def __init__(self, root_path: str = None, path_file: str = None, **kwargs):
        LoadConfig.__init__(self, root_path=root_path, path_file=path_file, **kwargs)

    def __load_configparser(self):
        config_parser = ConfigParser()
        path_file: str = f"{self._root_path}/{self._path_file}"
        try:
            config_parser.read(path_file)
        except Exception:
            from properties_loader.exceptions import PropertiesNotFoundError
            raise PropertiesNotFoundError(path_file)
        else:
            return config_parser

    @property
    def __dict__(self):
        properties_to_json: dict = {}
        config_parser: ConfigParser = self.__load_configparser()
        for section in config_parser.sections():
            keys_values_json = {}
            for key in config_parser.options(section):
                keys_values_json[key] = config_parser[section][key]
            properties_to_json[section] = keys_values_json
        return properties_to_json


class PropertiesClassLoader(Properties):

    def __init__(self, root_path: str = None, path_file: str = None, **kwargs):
        super(PropertiesClassLoader, self).__init__(root_path=root_path, path_file=path_file, **kwargs)
        self.__load_kwargs(**kwargs)
        self.__load_properties()

    def __load_kwargs(self, **kwargs):
        self.__groups = self.__load_groups(**kwargs)
        self.__efective_properties = self.__load_efective_properties()

    def __load_properties(self):
        for group in self.__efective_properties.keys():
            setattr(self, f'_{group}', self.__efective_properties.get(group))

    def __load_efective_properties(self):
        if self.__groups is None:
            return self.__dict__

        json_data: dict = {}
        for group in self.__dict__.keys():
            if group in self.__groups:
                json_data[group] = self.__dict__.get(group)
        return json_data

    def __load_groups(self, **kwargs):
        groups: list = kwargs.get(_Params.GROUPS)
        return groups

    @property
    def efective_properties(self):
        return self.__efective_properties
