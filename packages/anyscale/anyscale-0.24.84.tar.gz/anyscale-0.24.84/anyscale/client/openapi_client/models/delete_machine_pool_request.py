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


class DeleteMachinePoolRequest(object):
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
        'machine_pool_name': 'str'
    }

    attribute_map = {
        'machine_pool_name': 'machine_pool_name'
    }

    def __init__(self, machine_pool_name=None, local_vars_configuration=None):  # noqa: E501
        """DeleteMachinePoolRequest - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._machine_pool_name = None
        self.discriminator = None

        self.machine_pool_name = machine_pool_name

    @property
    def machine_pool_name(self):
        """Gets the machine_pool_name of this DeleteMachinePoolRequest.  # noqa: E501

        The name of the machine pool to delete.  # noqa: E501

        :return: The machine_pool_name of this DeleteMachinePoolRequest.  # noqa: E501
        :rtype: str
        """
        return self._machine_pool_name

    @machine_pool_name.setter
    def machine_pool_name(self, machine_pool_name):
        """Sets the machine_pool_name of this DeleteMachinePoolRequest.

        The name of the machine pool to delete.  # noqa: E501

        :param machine_pool_name: The machine_pool_name of this DeleteMachinePoolRequest.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and machine_pool_name is None:  # noqa: E501
            raise ValueError("Invalid value for `machine_pool_name`, must not be `None`")  # noqa: E501

        self._machine_pool_name = machine_pool_name

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
        if not isinstance(other, DeleteMachinePoolRequest):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, DeleteMachinePoolRequest):
            return True

        return self.to_dict() != other.to_dict()
