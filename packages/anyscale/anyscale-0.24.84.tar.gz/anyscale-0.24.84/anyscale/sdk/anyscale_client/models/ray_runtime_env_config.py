# coding: utf-8

"""
    Anyscale API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from anyscale_client.configuration import Configuration


class RayRuntimeEnvConfig(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'working_dir': 'str',
        'py_modules': 'list[str]',
        'pip': 'list[str]',
        'conda': 'object',
        'env_vars': 'dict(str, str)',
        'config': 'object'
    }

    attribute_map = {
        'working_dir': 'working_dir',
        'py_modules': 'py_modules',
        'pip': 'pip',
        'conda': 'conda',
        'env_vars': 'env_vars',
        'config': 'config'
    }

    def __init__(self, working_dir=None, py_modules=None, pip=None, conda=None, env_vars=None, config=None, local_vars_configuration=None):  # noqa: E501
        """RayRuntimeEnvConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._working_dir = None
        self._py_modules = None
        self._pip = None
        self._conda = None
        self._env_vars = None
        self._config = None
        self.discriminator = None

        if working_dir is not None:
            self.working_dir = working_dir
        if py_modules is not None:
            self.py_modules = py_modules
        if pip is not None:
            self.pip = pip
        if conda is not None:
            self.conda = conda
        if env_vars is not None:
            self.env_vars = env_vars
        if config is not None:
            self.config = config

    @property
    def working_dir(self):
        """Gets the working_dir of this RayRuntimeEnvConfig.  # noqa: E501

        The working directory that your code will run in. Must be a remote URI like an s3 or git path.  # noqa: E501

        :return: The working_dir of this RayRuntimeEnvConfig.  # noqa: E501
        :rtype: str
        """
        return self._working_dir

    @working_dir.setter
    def working_dir(self, working_dir):
        """Sets the working_dir of this RayRuntimeEnvConfig.

        The working directory that your code will run in. Must be a remote URI like an s3 or git path.  # noqa: E501

        :param working_dir: The working_dir of this RayRuntimeEnvConfig.  # noqa: E501
        :type: str
        """

        self._working_dir = working_dir

    @property
    def py_modules(self):
        """Gets the py_modules of this RayRuntimeEnvConfig.  # noqa: E501

        Python modules that will be installed along with your runtime env. These must be remote URIs.  # noqa: E501

        :return: The py_modules of this RayRuntimeEnvConfig.  # noqa: E501
        :rtype: list[str]
        """
        return self._py_modules

    @py_modules.setter
    def py_modules(self, py_modules):
        """Sets the py_modules of this RayRuntimeEnvConfig.

        Python modules that will be installed along with your runtime env. These must be remote URIs.  # noqa: E501

        :param py_modules: The py_modules of this RayRuntimeEnvConfig.  # noqa: E501
        :type: list[str]
        """

        self._py_modules = py_modules

    @property
    def pip(self):
        """Gets the pip of this RayRuntimeEnvConfig.  # noqa: E501

        A list of pip packages to install.  # noqa: E501

        :return: The pip of this RayRuntimeEnvConfig.  # noqa: E501
        :rtype: list[str]
        """
        return self._pip

    @pip.setter
    def pip(self, pip):
        """Sets the pip of this RayRuntimeEnvConfig.

        A list of pip packages to install.  # noqa: E501

        :param pip: The pip of this RayRuntimeEnvConfig.  # noqa: E501
        :type: list[str]
        """

        self._pip = pip

    @property
    def conda(self):
        """Gets the conda of this RayRuntimeEnvConfig.  # noqa: E501

        [Union[Dict[str, Any], str]: Either the conda YAML config or the name of a local conda env (e.g., \"pytorch_p36\"),   # noqa: E501

        :return: The conda of this RayRuntimeEnvConfig.  # noqa: E501
        :rtype: object
        """
        return self._conda

    @conda.setter
    def conda(self, conda):
        """Sets the conda of this RayRuntimeEnvConfig.

        [Union[Dict[str, Any], str]: Either the conda YAML config or the name of a local conda env (e.g., \"pytorch_p36\"),   # noqa: E501

        :param conda: The conda of this RayRuntimeEnvConfig.  # noqa: E501
        :type: object
        """

        self._conda = conda

    @property
    def env_vars(self):
        """Gets the env_vars of this RayRuntimeEnvConfig.  # noqa: E501

        Environment variables to set.  # noqa: E501

        :return: The env_vars of this RayRuntimeEnvConfig.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._env_vars

    @env_vars.setter
    def env_vars(self, env_vars):
        """Sets the env_vars of this RayRuntimeEnvConfig.

        Environment variables to set.  # noqa: E501

        :param env_vars: The env_vars of this RayRuntimeEnvConfig.  # noqa: E501
        :type: dict(str, str)
        """

        self._env_vars = env_vars

    @property
    def config(self):
        """Gets the config of this RayRuntimeEnvConfig.  # noqa: E501

        Config for runtime environment. Can be used to setup setup_timeout_seconds, the timeout of runtime environment creation.  # noqa: E501

        :return: The config of this RayRuntimeEnvConfig.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this RayRuntimeEnvConfig.

        Config for runtime environment. Can be used to setup setup_timeout_seconds, the timeout of runtime environment creation.  # noqa: E501

        :param config: The config of this RayRuntimeEnvConfig.  # noqa: E501
        :type: object
        """

        self._config = config

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, RayRuntimeEnvConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, RayRuntimeEnvConfig):
            return True

        return self.to_dict() != other.to_dict()
