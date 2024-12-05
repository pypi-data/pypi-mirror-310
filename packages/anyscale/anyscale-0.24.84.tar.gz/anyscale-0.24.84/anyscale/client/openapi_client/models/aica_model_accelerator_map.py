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


class AicaModelAcceleratorMap(object):
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
        'accelerator_map': 'dict(str, AicaModelConfiguration)'
    }

    attribute_map = {
        'accelerator_map': 'accelerator_map'
    }

    def __init__(self, accelerator_map=None, local_vars_configuration=None):  # noqa: E501
        """AicaModelAcceleratorMap - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._accelerator_map = None
        self.discriminator = None

        self.accelerator_map = accelerator_map

    @property
    def accelerator_map(self):
        """Gets the accelerator_map of this AicaModelAcceleratorMap.  # noqa: E501

        Map of accelerator type to model configuration  # noqa: E501

        :return: The accelerator_map of this AicaModelAcceleratorMap.  # noqa: E501
        :rtype: dict(str, AicaModelConfiguration)
        """
        return self._accelerator_map

    @accelerator_map.setter
    def accelerator_map(self, accelerator_map):
        """Sets the accelerator_map of this AicaModelAcceleratorMap.

        Map of accelerator type to model configuration  # noqa: E501

        :param accelerator_map: The accelerator_map of this AicaModelAcceleratorMap.  # noqa: E501
        :type: dict(str, AicaModelConfiguration)
        """
        if self.local_vars_configuration.client_side_validation and accelerator_map is None:  # noqa: E501
            raise ValueError("Invalid value for `accelerator_map`, must not be `None`")  # noqa: E501

        self._accelerator_map = accelerator_map

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
        if not isinstance(other, AicaModelAcceleratorMap):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AicaModelAcceleratorMap):
            return True

        return self.to_dict() != other.to_dict()
