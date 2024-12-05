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


class AppConfig(object):
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
        'id': 'str',
        'name': 'str',
        'project_id': 'str',
        'organization_id': 'str',
        'creator_id': 'str',
        'created_at': 'datetime',
        'last_modified_at': 'datetime',
        'deleted_at': 'datetime',
        'archiver_id': 'str',
        'archived_at': 'datetime',
        'is_default': 'bool',
        'anonymous': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'project_id': 'project_id',
        'organization_id': 'organization_id',
        'creator_id': 'creator_id',
        'created_at': 'created_at',
        'last_modified_at': 'last_modified_at',
        'deleted_at': 'deleted_at',
        'archiver_id': 'archiver_id',
        'archived_at': 'archived_at',
        'is_default': 'is_default',
        'anonymous': 'anonymous'
    }

    def __init__(self, id=None, name=None, project_id=None, organization_id=None, creator_id=None, created_at=None, last_modified_at=None, deleted_at=None, archiver_id=None, archived_at=None, is_default=False, anonymous=False, local_vars_configuration=None):  # noqa: E501
        """AppConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._project_id = None
        self._organization_id = None
        self._creator_id = None
        self._created_at = None
        self._last_modified_at = None
        self._deleted_at = None
        self._archiver_id = None
        self._archived_at = None
        self._is_default = None
        self._anonymous = None
        self.discriminator = None

        self.id = id
        self.name = name
        if project_id is not None:
            self.project_id = project_id
        self.organization_id = organization_id
        self.creator_id = creator_id
        self.created_at = created_at
        self.last_modified_at = last_modified_at
        if deleted_at is not None:
            self.deleted_at = deleted_at
        if archiver_id is not None:
            self.archiver_id = archiver_id
        if archived_at is not None:
            self.archived_at = archived_at
        if is_default is not None:
            self.is_default = is_default
        if anonymous is not None:
            self.anonymous = anonymous

    @property
    def id(self):
        """Gets the id of this AppConfig.  # noqa: E501

        Server assigned unique identifier.  # noqa: E501

        :return: The id of this AppConfig.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AppConfig.

        Server assigned unique identifier.  # noqa: E501

        :param id: The id of this AppConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this AppConfig.  # noqa: E501

        Name of the App Config.  # noqa: E501

        :return: The name of this AppConfig.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AppConfig.

        Name of the App Config.  # noqa: E501

        :param name: The name of this AppConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def project_id(self):
        """Gets the project_id of this AppConfig.  # noqa: E501

        ID of the Project this App Config is for.  # noqa: E501

        :return: The project_id of this AppConfig.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this AppConfig.

        ID of the Project this App Config is for.  # noqa: E501

        :param project_id: The project_id of this AppConfig.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def organization_id(self):
        """Gets the organization_id of this AppConfig.  # noqa: E501

        ID of the Organization this App Config was created in.  # noqa: E501

        :return: The organization_id of this AppConfig.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this AppConfig.

        ID of the Organization this App Config was created in.  # noqa: E501

        :param organization_id: The organization_id of this AppConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and organization_id is None:  # noqa: E501
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def creator_id(self):
        """Gets the creator_id of this AppConfig.  # noqa: E501

        ID of the User that created this record.  # noqa: E501

        :return: The creator_id of this AppConfig.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this AppConfig.

        ID of the User that created this record.  # noqa: E501

        :param creator_id: The creator_id of this AppConfig.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def created_at(self):
        """Gets the created_at of this AppConfig.  # noqa: E501

        Timestamp of when this record was created.  # noqa: E501

        :return: The created_at of this AppConfig.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this AppConfig.

        Timestamp of when this record was created.  # noqa: E501

        :param created_at: The created_at of this AppConfig.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def last_modified_at(self):
        """Gets the last_modified_at of this AppConfig.  # noqa: E501

        Timestamp of when this record was last updated.  # noqa: E501

        :return: The last_modified_at of this AppConfig.  # noqa: E501
        :rtype: datetime
        """
        return self._last_modified_at

    @last_modified_at.setter
    def last_modified_at(self, last_modified_at):
        """Sets the last_modified_at of this AppConfig.

        Timestamp of when this record was last updated.  # noqa: E501

        :param last_modified_at: The last_modified_at of this AppConfig.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and last_modified_at is None:  # noqa: E501
            raise ValueError("Invalid value for `last_modified_at`, must not be `None`")  # noqa: E501

        self._last_modified_at = last_modified_at

    @property
    def deleted_at(self):
        """Gets the deleted_at of this AppConfig.  # noqa: E501

        Timestamp of when this record was deleted.  # noqa: E501

        :return: The deleted_at of this AppConfig.  # noqa: E501
        :rtype: datetime
        """
        return self._deleted_at

    @deleted_at.setter
    def deleted_at(self, deleted_at):
        """Sets the deleted_at of this AppConfig.

        Timestamp of when this record was deleted.  # noqa: E501

        :param deleted_at: The deleted_at of this AppConfig.  # noqa: E501
        :type: datetime
        """

        self._deleted_at = deleted_at

    @property
    def archiver_id(self):
        """Gets the archiver_id of this AppConfig.  # noqa: E501

        ID of the User that archived this record.  # noqa: E501

        :return: The archiver_id of this AppConfig.  # noqa: E501
        :rtype: str
        """
        return self._archiver_id

    @archiver_id.setter
    def archiver_id(self, archiver_id):
        """Sets the archiver_id of this AppConfig.

        ID of the User that archived this record.  # noqa: E501

        :param archiver_id: The archiver_id of this AppConfig.  # noqa: E501
        :type: str
        """

        self._archiver_id = archiver_id

    @property
    def archived_at(self):
        """Gets the archived_at of this AppConfig.  # noqa: E501

        Timestamp of when this record was archived.  # noqa: E501

        :return: The archived_at of this AppConfig.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this AppConfig.

        Timestamp of when this record was archived.  # noqa: E501

        :param archived_at: The archived_at of this AppConfig.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def is_default(self):
        """Gets the is_default of this AppConfig.  # noqa: E501

        True if this App Config is created and managed by anyscale  # noqa: E501

        :return: The is_default of this AppConfig.  # noqa: E501
        :rtype: bool
        """
        return self._is_default

    @is_default.setter
    def is_default(self, is_default):
        """Sets the is_default of this AppConfig.

        True if this App Config is created and managed by anyscale  # noqa: E501

        :param is_default: The is_default of this AppConfig.  # noqa: E501
        :type: bool
        """

        self._is_default = is_default

    @property
    def anonymous(self):
        """Gets the anonymous of this AppConfig.  # noqa: E501

        True if this is an anonymous app config.  # noqa: E501

        :return: The anonymous of this AppConfig.  # noqa: E501
        :rtype: bool
        """
        return self._anonymous

    @anonymous.setter
    def anonymous(self, anonymous):
        """Sets the anonymous of this AppConfig.

        True if this is an anonymous app config.  # noqa: E501

        :param anonymous: The anonymous of this AppConfig.  # noqa: E501
        :type: bool
        """

        self._anonymous = anonymous

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
        if not isinstance(other, AppConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AppConfig):
            return True

        return self.to_dict() != other.to_dict()
