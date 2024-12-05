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


class UpdateClusterDns(object):
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
        'cluster_id': 'str',
        'address': 'str'
    }

    attribute_map = {
        'cluster_id': 'cluster_id',
        'address': 'address'
    }

    def __init__(self, cluster_id=None, address=None, local_vars_configuration=None):  # noqa: E501
        """UpdateClusterDns - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._cluster_id = None
        self._address = None
        self.discriminator = None

        self.cluster_id = cluster_id
        self.address = address

    @property
    def cluster_id(self):
        """Gets the cluster_id of this UpdateClusterDns.  # noqa: E501

        Id of the cluster  # noqa: E501

        :return: The cluster_id of this UpdateClusterDns.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this UpdateClusterDns.

        Id of the cluster  # noqa: E501

        :param cluster_id: The cluster_id of this UpdateClusterDns.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cluster_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_id`, must not be `None`")  # noqa: E501

        self._cluster_id = cluster_id

    @property
    def address(self):
        """Gets the address of this UpdateClusterDns.  # noqa: E501

        Head node address of the cluster  # noqa: E501

        :return: The address of this UpdateClusterDns.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this UpdateClusterDns.

        Head node address of the cluster  # noqa: E501

        :param address: The address of this UpdateClusterDns.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and address is None:  # noqa: E501
            raise ValueError("Invalid value for `address`, must not be `None`")  # noqa: E501

        self._address = address

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
        if not isinstance(other, UpdateClusterDns):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateClusterDns):
            return True

        return self.to_dict() != other.to_dict()
