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


class OrganizationSummary(object):
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
        'name': 'str',
        'id': 'str',
        'public_identifier': 'str',
        'creator_email': 'str',
        'total_users': 'int'
    }

    attribute_map = {
        'name': 'name',
        'id': 'id',
        'public_identifier': 'public_identifier',
        'creator_email': 'creator_email',
        'total_users': 'total_users'
    }

    def __init__(self, name=None, id=None, public_identifier=None, creator_email=None, total_users=None, local_vars_configuration=None):  # noqa: E501
        """OrganizationSummary - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._id = None
        self._public_identifier = None
        self._creator_email = None
        self._total_users = None
        self.discriminator = None

        self.name = name
        self.id = id
        self.public_identifier = public_identifier
        self.creator_email = creator_email
        self.total_users = total_users

    @property
    def name(self):
        """Gets the name of this OrganizationSummary.  # noqa: E501


        :return: The name of this OrganizationSummary.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this OrganizationSummary.


        :param name: The name of this OrganizationSummary.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def id(self):
        """Gets the id of this OrganizationSummary.  # noqa: E501


        :return: The id of this OrganizationSummary.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this OrganizationSummary.


        :param id: The id of this OrganizationSummary.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def public_identifier(self):
        """Gets the public_identifier of this OrganizationSummary.  # noqa: E501


        :return: The public_identifier of this OrganizationSummary.  # noqa: E501
        :rtype: str
        """
        return self._public_identifier

    @public_identifier.setter
    def public_identifier(self, public_identifier):
        """Sets the public_identifier of this OrganizationSummary.


        :param public_identifier: The public_identifier of this OrganizationSummary.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and public_identifier is None:  # noqa: E501
            raise ValueError("Invalid value for `public_identifier`, must not be `None`")  # noqa: E501

        self._public_identifier = public_identifier

    @property
    def creator_email(self):
        """Gets the creator_email of this OrganizationSummary.  # noqa: E501


        :return: The creator_email of this OrganizationSummary.  # noqa: E501
        :rtype: str
        """
        return self._creator_email

    @creator_email.setter
    def creator_email(self, creator_email):
        """Sets the creator_email of this OrganizationSummary.


        :param creator_email: The creator_email of this OrganizationSummary.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_email is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_email`, must not be `None`")  # noqa: E501

        self._creator_email = creator_email

    @property
    def total_users(self):
        """Gets the total_users of this OrganizationSummary.  # noqa: E501


        :return: The total_users of this OrganizationSummary.  # noqa: E501
        :rtype: int
        """
        return self._total_users

    @total_users.setter
    def total_users(self, total_users):
        """Sets the total_users of this OrganizationSummary.


        :param total_users: The total_users of this OrganizationSummary.  # noqa: E501
        :type: int
        """
        if self.local_vars_configuration.client_side_validation and total_users is None:  # noqa: E501
            raise ValueError("Invalid value for `total_users`, must not be `None`")  # noqa: E501

        self._total_users = total_users

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
        if not isinstance(other, OrganizationSummary):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, OrganizationSummary):
            return True

        return self.to_dict() != other.to_dict()
