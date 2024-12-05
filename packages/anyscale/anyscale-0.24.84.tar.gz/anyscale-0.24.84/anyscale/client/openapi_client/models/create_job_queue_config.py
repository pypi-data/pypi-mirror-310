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


class CreateJobQueueConfig(object):
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
        'priority': 'int',
        'target_job_queue_id': 'str',
        'target_job_queue_name': 'str',
        'job_queue_spec': 'JobQueueSpec'
    }

    attribute_map = {
        'priority': 'priority',
        'target_job_queue_id': 'target_job_queue_id',
        'target_job_queue_name': 'target_job_queue_name',
        'job_queue_spec': 'job_queue_spec'
    }

    def __init__(self, priority=None, target_job_queue_id=None, target_job_queue_name=None, job_queue_spec=None, local_vars_configuration=None):  # noqa: E501
        """CreateJobQueueConfig - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._priority = None
        self._target_job_queue_id = None
        self._target_job_queue_name = None
        self._job_queue_spec = None
        self.discriminator = None

        if priority is not None:
            self.priority = priority
        if target_job_queue_id is not None:
            self.target_job_queue_id = target_job_queue_id
        if target_job_queue_name is not None:
            self.target_job_queue_name = target_job_queue_name
        if job_queue_spec is not None:
            self.job_queue_spec = job_queue_spec

    @property
    def priority(self):
        """Gets the priority of this CreateJobQueueConfig.  # noqa: E501

        Job's relative priority (only relevant for Job Queues of type PRIORITY). Valid values range from 0 (highest) to +inf (lowest). Default value is None  # noqa: E501

        :return: The priority of this CreateJobQueueConfig.  # noqa: E501
        :rtype: int
        """
        return self._priority

    @priority.setter
    def priority(self, priority):
        """Sets the priority of this CreateJobQueueConfig.

        Job's relative priority (only relevant for Job Queues of type PRIORITY). Valid values range from 0 (highest) to +inf (lowest). Default value is None  # noqa: E501

        :param priority: The priority of this CreateJobQueueConfig.  # noqa: E501
        :type: int
        """

        self._priority = priority

    @property
    def target_job_queue_id(self):
        """Gets the target_job_queue_id of this CreateJobQueueConfig.  # noqa: E501

        Identifier of the existing Job Queue this job should be added to. Note, only one of `target_job_queue_id`, `target_job_queue_name` or `job_queue_spec` could be provided  # noqa: E501

        :return: The target_job_queue_id of this CreateJobQueueConfig.  # noqa: E501
        :rtype: str
        """
        return self._target_job_queue_id

    @target_job_queue_id.setter
    def target_job_queue_id(self, target_job_queue_id):
        """Sets the target_job_queue_id of this CreateJobQueueConfig.

        Identifier of the existing Job Queue this job should be added to. Note, only one of `target_job_queue_id`, `target_job_queue_name` or `job_queue_spec` could be provided  # noqa: E501

        :param target_job_queue_id: The target_job_queue_id of this CreateJobQueueConfig.  # noqa: E501
        :type: str
        """

        self._target_job_queue_id = target_job_queue_id

    @property
    def target_job_queue_name(self):
        """Gets the target_job_queue_name of this CreateJobQueueConfig.  # noqa: E501

        Existing Job Queue user-provided name (identifier), this job should be added to. Note, only one of `target_job_queue_id`, `target_job_queue_name` or `job_queue_spec` could be provided  # noqa: E501

        :return: The target_job_queue_name of this CreateJobQueueConfig.  # noqa: E501
        :rtype: str
        """
        return self._target_job_queue_name

    @target_job_queue_name.setter
    def target_job_queue_name(self, target_job_queue_name):
        """Sets the target_job_queue_name of this CreateJobQueueConfig.

        Existing Job Queue user-provided name (identifier), this job should be added to. Note, only one of `target_job_queue_id`, `target_job_queue_name` or `job_queue_spec` could be provided  # noqa: E501

        :param target_job_queue_name: The target_job_queue_name of this CreateJobQueueConfig.  # noqa: E501
        :type: str
        """

        self._target_job_queue_name = target_job_queue_name

    @property
    def job_queue_spec(self):
        """Gets the job_queue_spec of this CreateJobQueueConfig.  # noqa: E501

        Spec of the Job Queue definition that should be created and associated with this job. Note, only one of `target_job_queue_id`, `target_job_queue_name` or `job_queue_spec` could be provided  # noqa: E501

        :return: The job_queue_spec of this CreateJobQueueConfig.  # noqa: E501
        :rtype: JobQueueSpec
        """
        return self._job_queue_spec

    @job_queue_spec.setter
    def job_queue_spec(self, job_queue_spec):
        """Sets the job_queue_spec of this CreateJobQueueConfig.

        Spec of the Job Queue definition that should be created and associated with this job. Note, only one of `target_job_queue_id`, `target_job_queue_name` or `job_queue_spec` could be provided  # noqa: E501

        :param job_queue_spec: The job_queue_spec of this CreateJobQueueConfig.  # noqa: E501
        :type: JobQueueSpec
        """

        self._job_queue_spec = job_queue_spec

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
        if not isinstance(other, CreateJobQueueConfig):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateJobQueueConfig):
            return True

        return self.to_dict() != other.to_dict()
