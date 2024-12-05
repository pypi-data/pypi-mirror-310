# coding: utf-8

"""
    Managed Ray API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 0.1.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from openapi_client.configuration import Configuration


class CreateBYODAppConfigConfigurationSchema(object):
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
        'docker_image': 'str',
        'ray_version': 'str',
        'env_vars': 'object',
        'registry_login_secret': 'str'
    }

    attribute_map = {
        'docker_image': 'docker_image',
        'ray_version': 'ray_version',
        'env_vars': 'env_vars',
        'registry_login_secret': 'registry_login_secret'
    }

    def __init__(self, docker_image=None, ray_version=None, env_vars=None, registry_login_secret=None, local_vars_configuration=None):  # noqa: E501
        """CreateBYODAppConfigConfigurationSchema - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._docker_image = None
        self._ray_version = None
        self._env_vars = None
        self._registry_login_secret = None
        self.discriminator = None

        self.docker_image = docker_image
        self.ray_version = ray_version
        if env_vars is not None:
            self.env_vars = env_vars
        if registry_login_secret is not None:
            self.registry_login_secret = registry_login_secret

    @property
    def docker_image(self):
        """Gets the docker_image of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501

        The custom docker image to use to create a new app config.  # noqa: E501

        :return: The docker_image of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :rtype: str
        """
        return self._docker_image

    @docker_image.setter
    def docker_image(self, docker_image):
        """Sets the docker_image of this CreateBYODAppConfigConfigurationSchema.

        The custom docker image to use to create a new app config.  # noqa: E501

        :param docker_image: The docker_image of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and docker_image is None:  # noqa: E501
            raise ValueError("Invalid value for `docker_image`, must not be `None`")  # noqa: E501

        self._docker_image = docker_image

    @property
    def ray_version(self):
        """Gets the ray_version of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501


        :return: The ray_version of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :rtype: str
        """
        return self._ray_version

    @ray_version.setter
    def ray_version(self, ray_version):
        """Sets the ray_version of this CreateBYODAppConfigConfigurationSchema.


        :param ray_version: The ray_version of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and ray_version is None:  # noqa: E501
            raise ValueError("Invalid value for `ray_version`, must not be `None`")  # noqa: E501

        self._ray_version = ray_version

    @property
    def env_vars(self):
        """Gets the env_vars of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501

        Environment variables in the docker image that'll be used at runtime.  # noqa: E501

        :return: The env_vars of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :rtype: object
        """
        return self._env_vars

    @env_vars.setter
    def env_vars(self, env_vars):
        """Sets the env_vars of this CreateBYODAppConfigConfigurationSchema.

        Environment variables in the docker image that'll be used at runtime.  # noqa: E501

        :param env_vars: The env_vars of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :type: object
        """

        self._env_vars = env_vars

    @property
    def registry_login_secret(self):
        """Gets the registry_login_secret of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501

        The name or identifier of a secret containing credentials to authenticate to the docker registry hosting the image.  # noqa: E501

        :return: The registry_login_secret of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :rtype: str
        """
        return self._registry_login_secret

    @registry_login_secret.setter
    def registry_login_secret(self, registry_login_secret):
        """Sets the registry_login_secret of this CreateBYODAppConfigConfigurationSchema.

        The name or identifier of a secret containing credentials to authenticate to the docker registry hosting the image.  # noqa: E501

        :param registry_login_secret: The registry_login_secret of this CreateBYODAppConfigConfigurationSchema.  # noqa: E501
        :type: str
        """

        self._registry_login_secret = registry_login_secret

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
        if not isinstance(other, CreateBYODAppConfigConfigurationSchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateBYODAppConfigConfigurationSchema):
            return True

        return self.to_dict() != other.to_dict()
