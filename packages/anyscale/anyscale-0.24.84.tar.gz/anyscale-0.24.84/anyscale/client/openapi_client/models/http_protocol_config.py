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


class HttpProtocolConfig(object):
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
        'enabled': 'bool',
        'port': 'int'
    }

    attribute_map = {
        'enabled': 'enabled',
        'port': 'port'
    }

    def __init__(self, enabled=True, port=8000, local_vars_configuration=None):  # noqa: E501
        """HttpProtocolConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._enabled = None
        self._port = None
        self.discriminator = None

        if enabled is not None:
            self.enabled = enabled
        if port is not None:
            self.port = port

    @property
    def enabled(self):
        """Gets the enabled of this HttpProtocolConfig.  # noqa: E501

        Flag to enable the protocol in alb  # noqa: E501

        :return: The enabled of this HttpProtocolConfig.  # noqa: E501
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """Sets the enabled of this HttpProtocolConfig.

        Flag to enable the protocol in alb  # noqa: E501

        :param enabled: The enabled of this HttpProtocolConfig.  # noqa: E501
        :type: bool
        """

        self._enabled = enabled

    @property
    def port(self):
        """Gets the port of this HttpProtocolConfig.  # noqa: E501

        The port this protocol listens on.  # noqa: E501

        :return: The port of this HttpProtocolConfig.  # noqa: E501
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port):
        """Sets the port of this HttpProtocolConfig.

        The port this protocol listens on.  # noqa: E501

        :param port: The port of this HttpProtocolConfig.  # noqa: E501
        :type: int
        """

        self._port = port

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
        if not isinstance(other, HttpProtocolConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, HttpProtocolConfig):
            return True

        return self.to_dict() != other.to_dict()
