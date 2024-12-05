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


class WorkspaceTemplateClusterEnvironmentMetadata(object):
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
        'cluster_env_build_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'cluster_env_build_id': 'cluster_env_build_id'
    }

    def __init__(self, id=None, name=None, cluster_env_build_id=None, local_vars_configuration=None):  # noqa: E501
        """WorkspaceTemplateClusterEnvironmentMetadata - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._cluster_env_build_id = None
        self.discriminator = None

        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if cluster_env_build_id is not None:
            self.cluster_env_build_id = cluster_env_build_id

    @property
    def id(self):
        """Gets the id of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501

        Server generated ID of the cluster environment.  # noqa: E501

        :return: The id of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this WorkspaceTemplateClusterEnvironmentMetadata.

        Server generated ID of the cluster environment.  # noqa: E501

        :param id: The id of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501

        Name of the cluster environment.  # noqa: E501

        :return: The name of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this WorkspaceTemplateClusterEnvironmentMetadata.

        Name of the cluster environment.  # noqa: E501

        :param name: The name of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def cluster_env_build_id(self):
        """Gets the cluster_env_build_id of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501

        Build ID of the cluster environment.  # noqa: E501

        :return: The cluster_env_build_id of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501
        :rtype: str
        """
        return self._cluster_env_build_id

    @cluster_env_build_id.setter
    def cluster_env_build_id(self, cluster_env_build_id):
        """Sets the cluster_env_build_id of this WorkspaceTemplateClusterEnvironmentMetadata.

        Build ID of the cluster environment.  # noqa: E501

        :param cluster_env_build_id: The cluster_env_build_id of this WorkspaceTemplateClusterEnvironmentMetadata.  # noqa: E501
        :type: str
        """

        self._cluster_env_build_id = cluster_env_build_id

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
        if not isinstance(other, WorkspaceTemplateClusterEnvironmentMetadata):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WorkspaceTemplateClusterEnvironmentMetadata):
            return True

        return self.to_dict() != other.to_dict()
