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


class BuildRegistration(object):
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
        'aws': 'NodeRegistrationAWS',
        'gcp': 'NodeRegistrationGCP',
        'provisioned': 'NodeRegistrationProvisioned',
        'k8s': 'NodeRegistrationK8S',
        'provider': 'CloudProvider',
        'cloud_id': 'str',
        'build_id': 'str'
    }

    attribute_map = {
        'aws': 'aws',
        'gcp': 'gcp',
        'provisioned': 'provisioned',
        'k8s': 'k8s',
        'provider': 'provider',
        'cloud_id': 'cloud_id',
        'build_id': 'build_id'
    }

    def __init__(self, aws=None, gcp=None, provisioned=None, k8s=None, provider=None, cloud_id=None, build_id=None, local_vars_configuration=None):  # noqa: E501
        """BuildRegistration - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._aws = None
        self._gcp = None
        self._provisioned = None
        self._k8s = None
        self._provider = None
        self._cloud_id = None
        self._build_id = None
        self.discriminator = None

        if aws is not None:
            self.aws = aws
        if gcp is not None:
            self.gcp = gcp
        if provisioned is not None:
            self.provisioned = provisioned
        if k8s is not None:
            self.k8s = k8s
        self.provider = provider
        self.cloud_id = cloud_id
        self.build_id = build_id

    @property
    def aws(self):
        """Gets the aws of this BuildRegistration.  # noqa: E501


        :return: The aws of this BuildRegistration.  # noqa: E501
        :rtype: NodeRegistrationAWS
        """
        return self._aws

    @aws.setter
    def aws(self, aws):
        """Sets the aws of this BuildRegistration.


        :param aws: The aws of this BuildRegistration.  # noqa: E501
        :type: NodeRegistrationAWS
        """

        self._aws = aws

    @property
    def gcp(self):
        """Gets the gcp of this BuildRegistration.  # noqa: E501


        :return: The gcp of this BuildRegistration.  # noqa: E501
        :rtype: NodeRegistrationGCP
        """
        return self._gcp

    @gcp.setter
    def gcp(self, gcp):
        """Sets the gcp of this BuildRegistration.


        :param gcp: The gcp of this BuildRegistration.  # noqa: E501
        :type: NodeRegistrationGCP
        """

        self._gcp = gcp

    @property
    def provisioned(self):
        """Gets the provisioned of this BuildRegistration.  # noqa: E501


        :return: The provisioned of this BuildRegistration.  # noqa: E501
        :rtype: NodeRegistrationProvisioned
        """
        return self._provisioned

    @provisioned.setter
    def provisioned(self, provisioned):
        """Sets the provisioned of this BuildRegistration.


        :param provisioned: The provisioned of this BuildRegistration.  # noqa: E501
        :type: NodeRegistrationProvisioned
        """

        self._provisioned = provisioned

    @property
    def k8s(self):
        """Gets the k8s of this BuildRegistration.  # noqa: E501


        :return: The k8s of this BuildRegistration.  # noqa: E501
        :rtype: NodeRegistrationK8S
        """
        return self._k8s

    @k8s.setter
    def k8s(self, k8s):
        """Sets the k8s of this BuildRegistration.


        :param k8s: The k8s of this BuildRegistration.  # noqa: E501
        :type: NodeRegistrationK8S
        """

        self._k8s = k8s

    @property
    def provider(self):
        """Gets the provider of this BuildRegistration.  # noqa: E501

        Which provider this registration is for.  # noqa: E501

        :return: The provider of this BuildRegistration.  # noqa: E501
        :rtype: CloudProvider
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """Sets the provider of this BuildRegistration.

        Which provider this registration is for.  # noqa: E501

        :param provider: The provider of this BuildRegistration.  # noqa: E501
        :type: CloudProvider
        """
        if self.local_vars_configuration.client_side_validation and provider is None:  # noqa: E501
            raise ValueError("Invalid value for `provider`, must not be `None`")  # noqa: E501

        self._provider = provider

    @property
    def cloud_id(self):
        """Gets the cloud_id of this BuildRegistration.  # noqa: E501

        Cloud ID of the build node.  # noqa: E501

        :return: The cloud_id of this BuildRegistration.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this BuildRegistration.

        Cloud ID of the build node.  # noqa: E501

        :param cloud_id: The cloud_id of this BuildRegistration.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def build_id(self):
        """Gets the build_id of this BuildRegistration.  # noqa: E501

        Build ID of the build node.  # noqa: E501

        :return: The build_id of this BuildRegistration.  # noqa: E501
        :rtype: str
        """
        return self._build_id

    @build_id.setter
    def build_id(self, build_id):
        """Sets the build_id of this BuildRegistration.

        Build ID of the build node.  # noqa: E501

        :param build_id: The build_id of this BuildRegistration.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and build_id is None:  # noqa: E501
            raise ValueError("Invalid value for `build_id`, must not be `None`")  # noqa: E501

        self._build_id = build_id

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
        if not isinstance(other, BuildRegistration):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, BuildRegistration):
            return True

        return self.to_dict() != other.to_dict()
