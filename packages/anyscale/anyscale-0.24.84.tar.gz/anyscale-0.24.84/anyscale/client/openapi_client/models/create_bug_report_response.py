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


class CreateBugReportResponse(object):
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
        'report_id': 'str',
        'upload_url': 'str'
    }

    attribute_map = {
        'report_id': 'report_id',
        'upload_url': 'upload_url'
    }

    def __init__(self, report_id=None, upload_url=None, local_vars_configuration=None):  # noqa: E501
        """CreateBugReportResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._report_id = None
        self._upload_url = None
        self.discriminator = None

        self.report_id = report_id
        self.upload_url = upload_url

    @property
    def report_id(self):
        """Gets the report_id of this CreateBugReportResponse.  # noqa: E501

        An ID that should be given to the user as a unique identifier for the bug report.  # noqa: E501

        :return: The report_id of this CreateBugReportResponse.  # noqa: E501
        :rtype: str
        """
        return self._report_id

    @report_id.setter
    def report_id(self, report_id):
        """Sets the report_id of this CreateBugReportResponse.

        An ID that should be given to the user as a unique identifier for the bug report.  # noqa: E501

        :param report_id: The report_id of this CreateBugReportResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and report_id is None:  # noqa: E501
            raise ValueError("Invalid value for `report_id`, must not be `None`")  # noqa: E501

        self._report_id = report_id

    @property
    def upload_url(self):
        """Gets the upload_url of this CreateBugReportResponse.  # noqa: E501

        A URL that the contents of a bug report may be uploaded to.  # noqa: E501

        :return: The upload_url of this CreateBugReportResponse.  # noqa: E501
        :rtype: str
        """
        return self._upload_url

    @upload_url.setter
    def upload_url(self, upload_url):
        """Sets the upload_url of this CreateBugReportResponse.

        A URL that the contents of a bug report may be uploaded to.  # noqa: E501

        :param upload_url: The upload_url of this CreateBugReportResponse.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and upload_url is None:  # noqa: E501
            raise ValueError("Invalid value for `upload_url`, must not be `None`")  # noqa: E501

        self._upload_url = upload_url

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
        if not isinstance(other, CreateBugReportResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateBugReportResponse):
            return True

        return self.to_dict() != other.to_dict()
