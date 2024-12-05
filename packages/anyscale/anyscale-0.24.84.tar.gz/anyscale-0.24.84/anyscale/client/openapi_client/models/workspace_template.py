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


class WorkspaceTemplate(object):
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
        'title': 'str',
        'description': 'str',
        'emoji': 'str',
        'labels': 'list[str]',
        'url': 'str',
        'maximum_uptime_minutes': 'int',
        'logo_ids': 'list[str]',
        'oa_group_name': 'str'
    }

    attribute_map = {
        'id': 'id',
        'title': 'title',
        'description': 'description',
        'emoji': 'emoji',
        'labels': 'labels',
        'url': 'url',
        'maximum_uptime_minutes': 'maximum_uptime_minutes',
        'logo_ids': 'logo_ids',
        'oa_group_name': 'oa_group_name'
    }

    def __init__(self, id=None, title=None, description=None, emoji=None, labels=None, url=None, maximum_uptime_minutes=None, logo_ids=None, oa_group_name=None, local_vars_configuration=None):  # noqa: E501
        """WorkspaceTemplate - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._title = None
        self._description = None
        self._emoji = None
        self._labels = None
        self._url = None
        self._maximum_uptime_minutes = None
        self._logo_ids = None
        self._oa_group_name = None
        self.discriminator = None

        self.id = id
        self.title = title
        self.description = description
        self.emoji = emoji
        self.labels = labels
        self.url = url
        if maximum_uptime_minutes is not None:
            self.maximum_uptime_minutes = maximum_uptime_minutes
        self.logo_ids = logo_ids
        if oa_group_name is not None:
            self.oa_group_name = oa_group_name

    @property
    def id(self):
        """Gets the id of this WorkspaceTemplate.  # noqa: E501

        The id of the workspace template.  # noqa: E501

        :return: The id of this WorkspaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this WorkspaceTemplate.

        The id of the workspace template.  # noqa: E501

        :param id: The id of this WorkspaceTemplate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def title(self):
        """Gets the title of this WorkspaceTemplate.  # noqa: E501

        The title of the workspace template  # noqa: E501

        :return: The title of this WorkspaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._title

    @title.setter
    def title(self, title):
        """Sets the title of this WorkspaceTemplate.

        The title of the workspace template  # noqa: E501

        :param title: The title of this WorkspaceTemplate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and title is None:  # noqa: E501
            raise ValueError("Invalid value for `title`, must not be `None`")  # noqa: E501

        self._title = title

    @property
    def description(self):
        """Gets the description of this WorkspaceTemplate.  # noqa: E501

        The description of the workspace template  # noqa: E501

        :return: The description of this WorkspaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this WorkspaceTemplate.

        The description of the workspace template  # noqa: E501

        :param description: The description of this WorkspaceTemplate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and description is None:  # noqa: E501
            raise ValueError("Invalid value for `description`, must not be `None`")  # noqa: E501

        self._description = description

    @property
    def emoji(self):
        """Gets the emoji of this WorkspaceTemplate.  # noqa: E501

        The emoji of the workspace template  # noqa: E501

        :return: The emoji of this WorkspaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._emoji

    @emoji.setter
    def emoji(self, emoji):
        """Sets the emoji of this WorkspaceTemplate.

        The emoji of the workspace template  # noqa: E501

        :param emoji: The emoji of this WorkspaceTemplate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and emoji is None:  # noqa: E501
            raise ValueError("Invalid value for `emoji`, must not be `None`")  # noqa: E501

        self._emoji = emoji

    @property
    def labels(self):
        """Gets the labels of this WorkspaceTemplate.  # noqa: E501

        The labels of the workspace template  # noqa: E501

        :return: The labels of this WorkspaceTemplate.  # noqa: E501
        :rtype: list[str]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """Sets the labels of this WorkspaceTemplate.

        The labels of the workspace template  # noqa: E501

        :param labels: The labels of this WorkspaceTemplate.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and labels is None:  # noqa: E501
            raise ValueError("Invalid value for `labels`, must not be `None`")  # noqa: E501

        self._labels = labels

    @property
    def url(self):
        """Gets the url of this WorkspaceTemplate.  # noqa: E501

        The url of the workspace template  # noqa: E501

        :return: The url of this WorkspaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this WorkspaceTemplate.

        The url of the workspace template  # noqa: E501

        :param url: The url of this WorkspaceTemplate.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and url is None:  # noqa: E501
            raise ValueError("Invalid value for `url`, must not be `None`")  # noqa: E501

        self._url = url

    @property
    def maximum_uptime_minutes(self):
        """Gets the maximum_uptime_minutes of this WorkspaceTemplate.  # noqa: E501

        The maximum uptime of the workspace in minutes. The workspace will force terminate after this time.  # noqa: E501

        :return: The maximum_uptime_minutes of this WorkspaceTemplate.  # noqa: E501
        :rtype: int
        """
        return self._maximum_uptime_minutes

    @maximum_uptime_minutes.setter
    def maximum_uptime_minutes(self, maximum_uptime_minutes):
        """Sets the maximum_uptime_minutes of this WorkspaceTemplate.

        The maximum uptime of the workspace in minutes. The workspace will force terminate after this time.  # noqa: E501

        :param maximum_uptime_minutes: The maximum_uptime_minutes of this WorkspaceTemplate.  # noqa: E501
        :type: int
        """

        self._maximum_uptime_minutes = maximum_uptime_minutes

    @property
    def logo_ids(self):
        """Gets the logo_ids of this WorkspaceTemplate.  # noqa: E501

        The ids for the workspace template logos that we show on the FE  # noqa: E501

        :return: The logo_ids of this WorkspaceTemplate.  # noqa: E501
        :rtype: list[str]
        """
        return self._logo_ids

    @logo_ids.setter
    def logo_ids(self, logo_ids):
        """Sets the logo_ids of this WorkspaceTemplate.

        The ids for the workspace template logos that we show on the FE  # noqa: E501

        :param logo_ids: The logo_ids of this WorkspaceTemplate.  # noqa: E501
        :type: list[str]
        """
        if self.local_vars_configuration.client_side_validation and logo_ids is None:  # noqa: E501
            raise ValueError("Invalid value for `logo_ids`, must not be `None`")  # noqa: E501

        self._logo_ids = logo_ids

    @property
    def oa_group_name(self):
        """Gets the oa_group_name of this WorkspaceTemplate.  # noqa: E501

        The name of the OA group for the workspace template  # noqa: E501

        :return: The oa_group_name of this WorkspaceTemplate.  # noqa: E501
        :rtype: str
        """
        return self._oa_group_name

    @oa_group_name.setter
    def oa_group_name(self, oa_group_name):
        """Sets the oa_group_name of this WorkspaceTemplate.

        The name of the OA group for the workspace template  # noqa: E501

        :param oa_group_name: The oa_group_name of this WorkspaceTemplate.  # noqa: E501
        :type: str
        """

        self._oa_group_name = oa_group_name

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
        if not isinstance(other, WorkspaceTemplate):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WorkspaceTemplate):
            return True

        return self.to_dict() != other.to_dict()
