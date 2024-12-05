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


class OrganizationUsageAlert(object):
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
        'type': 'AlertType',
        'severity': 'OrganizationUsageAlertSeverity',
        'status': 'CustomerAlertStatus',
        'permission_level': 'OrganizationPermissionLevel'
    }

    attribute_map = {
        'type': 'type',
        'severity': 'severity',
        'status': 'status',
        'permission_level': 'permission_level'
    }

    def __init__(self, type=None, severity=None, status=None, permission_level=None, local_vars_configuration=None):  # noqa: E501
        """OrganizationUsageAlert - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._type = None
        self._severity = None
        self._status = None
        self._permission_level = None
        self.discriminator = None

        self.type = type
        self.severity = severity
        self.status = status
        self.permission_level = permission_level

    @property
    def type(self):
        """Gets the type of this OrganizationUsageAlert.  # noqa: E501

        Type of the alert  # noqa: E501

        :return: The type of this OrganizationUsageAlert.  # noqa: E501
        :rtype: AlertType
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this OrganizationUsageAlert.

        Type of the alert  # noqa: E501

        :param type: The type of this OrganizationUsageAlert.  # noqa: E501
        :type: AlertType
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

    @property
    def severity(self):
        """Gets the severity of this OrganizationUsageAlert.  # noqa: E501

        Severity of the alert  # noqa: E501

        :return: The severity of this OrganizationUsageAlert.  # noqa: E501
        :rtype: OrganizationUsageAlertSeverity
        """
        return self._severity

    @severity.setter
    def severity(self, severity):
        """Sets the severity of this OrganizationUsageAlert.

        Severity of the alert  # noqa: E501

        :param severity: The severity of this OrganizationUsageAlert.  # noqa: E501
        :type: OrganizationUsageAlertSeverity
        """
        if self.local_vars_configuration.client_side_validation and severity is None:  # noqa: E501
            raise ValueError("Invalid value for `severity`, must not be `None`")  # noqa: E501

        self._severity = severity

    @property
    def status(self):
        """Gets the status of this OrganizationUsageAlert.  # noqa: E501

        Status of the alert  # noqa: E501

        :return: The status of this OrganizationUsageAlert.  # noqa: E501
        :rtype: CustomerAlertStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this OrganizationUsageAlert.

        Status of the alert  # noqa: E501

        :param status: The status of this OrganizationUsageAlert.  # noqa: E501
        :type: CustomerAlertStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def permission_level(self):
        """Gets the permission_level of this OrganizationUsageAlert.  # noqa: E501

        Permission level of the user  # noqa: E501

        :return: The permission_level of this OrganizationUsageAlert.  # noqa: E501
        :rtype: OrganizationPermissionLevel
        """
        return self._permission_level

    @permission_level.setter
    def permission_level(self, permission_level):
        """Sets the permission_level of this OrganizationUsageAlert.

        Permission level of the user  # noqa: E501

        :param permission_level: The permission_level of this OrganizationUsageAlert.  # noqa: E501
        :type: OrganizationPermissionLevel
        """
        if self.local_vars_configuration.client_side_validation and permission_level is None:  # noqa: E501
            raise ValueError("Invalid value for `permission_level`, must not be `None`")  # noqa: E501

        self._permission_level = permission_level

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
        if not isinstance(other, OrganizationUsageAlert):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrganizationUsageAlert):
            return True

        return self.to_dict() != other.to_dict()
