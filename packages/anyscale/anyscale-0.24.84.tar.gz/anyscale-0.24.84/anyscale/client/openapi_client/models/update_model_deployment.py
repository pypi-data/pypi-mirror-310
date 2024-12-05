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


class UpdateModelDeployment(object):
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
        'model_id': 'str',
        'config': 'object'
    }

    attribute_map = {
        'model_id': 'model_id',
        'config': 'config'
    }

    def __init__(self, model_id=None, config=None, local_vars_configuration=None):  # noqa: E501
        """UpdateModelDeployment - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._model_id = None
        self._config = None
        self.discriminator = None

        self.model_id = model_id
        self.config = config

    @property
    def model_id(self):
        """Gets the model_id of this UpdateModelDeployment.  # noqa: E501

        Id of the model to be updated.  # noqa: E501

        :return: The model_id of this UpdateModelDeployment.  # noqa: E501
        :rtype: str
        """
        return self._model_id

    @model_id.setter
    def model_id(self, model_id):
        """Sets the model_id of this UpdateModelDeployment.

        Id of the model to be updated.  # noqa: E501

        :param model_id: The model_id of this UpdateModelDeployment.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and model_id is None:  # noqa: E501
            raise ValueError("Invalid value for `model_id`, must not be `None`")  # noqa: E501

        self._model_id = model_id

    @property
    def config(self):
        """Gets the config of this UpdateModelDeployment.  # noqa: E501

        The configuration for the endpoints model.  # noqa: E501

        :return: The config of this UpdateModelDeployment.  # noqa: E501
        :rtype: object
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this UpdateModelDeployment.

        The configuration for the endpoints model.  # noqa: E501

        :param config: The config of this UpdateModelDeployment.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and config is None:  # noqa: E501
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

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
        if not isinstance(other, UpdateModelDeployment):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, UpdateModelDeployment):
            return True

        return self.to_dict() != other.to_dict()
