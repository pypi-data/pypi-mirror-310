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


class LogStream(object):
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
        'http_url': 'str',
        'stream_url': 'str'
    }

    attribute_map = {
        'http_url': 'http_url',
        'stream_url': 'stream_url'
    }

    def __init__(self, http_url=None, stream_url=None, local_vars_configuration=None):  # noqa: E501
        """LogStream - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._http_url = None
        self._stream_url = None
        self.discriminator = None

        self.http_url = http_url
        if stream_url is not None:
            self.stream_url = stream_url

    @property
    def http_url(self):
        """Gets the http_url of this LogStream.  # noqa: E501

        HTTP URL for retrieving initial lines.  # noqa: E501

        :return: The http_url of this LogStream.  # noqa: E501
        :rtype: str
        """
        return self._http_url

    @http_url.setter
    def http_url(self, http_url):
        """Sets the http_url of this LogStream.

        HTTP URL for retrieving initial lines.  # noqa: E501

        :param http_url: The http_url of this LogStream.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and http_url is None:  # noqa: E501
            raise ValueError("Invalid value for `http_url`, must not be `None`")  # noqa: E501

        self._http_url = http_url

    @property
    def stream_url(self):
        """Gets the stream_url of this LogStream.  # noqa: E501

        HTTP/WebSocket URL for streaming Ray logs.  # noqa: E501

        :return: The stream_url of this LogStream.  # noqa: E501
        :rtype: str
        """
        return self._stream_url

    @stream_url.setter
    def stream_url(self, stream_url):
        """Sets the stream_url of this LogStream.

        HTTP/WebSocket URL for streaming Ray logs.  # noqa: E501

        :param stream_url: The stream_url of this LogStream.  # noqa: E501
        :type: str
        """

        self._stream_url = stream_url

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
        if not isinstance(other, LogStream):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LogStream):
            return True

        return self.to_dict() != other.to_dict()
