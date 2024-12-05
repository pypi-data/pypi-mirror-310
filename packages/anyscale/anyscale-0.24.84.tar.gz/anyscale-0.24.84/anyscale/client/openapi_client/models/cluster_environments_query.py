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


class ClusterEnvironmentsQuery(object):
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
        'project_id': 'str',
        'creator_id': 'str',
        'name': 'TextQuery',
        'image_name': 'TextQuery',
        'paging': 'PageQuery',
        'include_archived': 'bool',
        'include_anonymous': 'bool'
    }

    attribute_map = {
        'project_id': 'project_id',
        'creator_id': 'creator_id',
        'name': 'name',
        'image_name': 'image_name',
        'paging': 'paging',
        'include_archived': 'include_archived',
        'include_anonymous': 'include_anonymous'
    }

    def __init__(self, project_id=None, creator_id=None, name=None, image_name=None, paging=None, include_archived=False, include_anonymous=False, local_vars_configuration=None):  # noqa: E501
        """ClusterEnvironmentsQuery - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._project_id = None
        self._creator_id = None
        self._name = None
        self._image_name = None
        self._paging = None
        self._include_archived = None
        self._include_anonymous = None
        self.discriminator = None

        if project_id is not None:
            self.project_id = project_id
        if creator_id is not None:
            self.creator_id = creator_id
        if name is not None:
            self.name = name
        if image_name is not None:
            self.image_name = image_name
        if paging is not None:
            self.paging = paging
        if include_archived is not None:
            self.include_archived = include_archived
        if include_anonymous is not None:
            self.include_anonymous = include_anonymous

    @property
    def project_id(self):
        """Gets the project_id of this ClusterEnvironmentsQuery.  # noqa: E501

        Filters Cluster Environments by project id. If absent, no filtering is done.  # noqa: E501

        :return: The project_id of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ClusterEnvironmentsQuery.

        Filters Cluster Environments by project id. If absent, no filtering is done.  # noqa: E501

        :param project_id: The project_id of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def creator_id(self):
        """Gets the creator_id of this ClusterEnvironmentsQuery.  # noqa: E501

        Filters Cluster Environments by creator id. If absent, no filtering is done.  # noqa: E501

        :return: The creator_id of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this ClusterEnvironmentsQuery.

        Filters Cluster Environments by creator id. If absent, no filtering is done.  # noqa: E501

        :param creator_id: The creator_id of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: str
        """

        self._creator_id = creator_id

    @property
    def name(self):
        """Gets the name of this ClusterEnvironmentsQuery.  # noqa: E501

        Filters Cluster Environments by name. Currently only contains is supported.If absent, no filtering is done.  # noqa: E501

        :return: The name of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: TextQuery
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ClusterEnvironmentsQuery.

        Filters Cluster Environments by name. Currently only contains is supported.If absent, no filtering is done.  # noqa: E501

        :param name: The name of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: TextQuery
        """

        self._name = name

    @property
    def image_name(self):
        """Gets the image_name of this ClusterEnvironmentsQuery.  # noqa: E501

        Filters Cluster Environments by image name. Image name is a virtual concept. It starts with 'anyscale/image' (for customer-built images) or 'anyscale/ray' (default images).Currently only contains is supported. If absent, no filtering is done.  # noqa: E501

        :return: The image_name of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: TextQuery
        """
        return self._image_name

    @image_name.setter
    def image_name(self, image_name):
        """Sets the image_name of this ClusterEnvironmentsQuery.

        Filters Cluster Environments by image name. Image name is a virtual concept. It starts with 'anyscale/image' (for customer-built images) or 'anyscale/ray' (default images).Currently only contains is supported. If absent, no filtering is done.  # noqa: E501

        :param image_name: The image_name of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: TextQuery
        """

        self._image_name = image_name

    @property
    def paging(self):
        """Gets the paging of this ClusterEnvironmentsQuery.  # noqa: E501

        Pagination information.  # noqa: E501

        :return: The paging of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: PageQuery
        """
        return self._paging

    @paging.setter
    def paging(self, paging):
        """Sets the paging of this ClusterEnvironmentsQuery.

        Pagination information.  # noqa: E501

        :param paging: The paging of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: PageQuery
        """

        self._paging = paging

    @property
    def include_archived(self):
        """Gets the include_archived of this ClusterEnvironmentsQuery.  # noqa: E501

        Whether to include archived Cluster Environments in the results.  # noqa: E501

        :return: The include_archived of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: bool
        """
        return self._include_archived

    @include_archived.setter
    def include_archived(self, include_archived):
        """Sets the include_archived of this ClusterEnvironmentsQuery.

        Whether to include archived Cluster Environments in the results.  # noqa: E501

        :param include_archived: The include_archived of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: bool
        """

        self._include_archived = include_archived

    @property
    def include_anonymous(self):
        """Gets the include_anonymous of this ClusterEnvironmentsQuery.  # noqa: E501

        Whether to include anonymous Cluster Environments in the results.  # noqa: E501

        :return: The include_anonymous of this ClusterEnvironmentsQuery.  # noqa: E501
        :rtype: bool
        """
        return self._include_anonymous

    @include_anonymous.setter
    def include_anonymous(self, include_anonymous):
        """Sets the include_anonymous of this ClusterEnvironmentsQuery.

        Whether to include anonymous Cluster Environments in the results.  # noqa: E501

        :param include_anonymous: The include_anonymous of this ClusterEnvironmentsQuery.  # noqa: E501
        :type: bool
        """

        self._include_anonymous = include_anonymous

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
        if not isinstance(other, ClusterEnvironmentsQuery):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ClusterEnvironmentsQuery):
            return True

        return self.to_dict() != other.to_dict()
