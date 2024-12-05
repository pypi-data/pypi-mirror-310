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


class MiniJobRun(object):
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
        'ray_session_name': 'str',
        'ray_job_id': 'str',
        'name': 'str',
        'status': 'BaseJobStatus',
        'created_at': 'datetime',
        'finished_at': 'datetime',
        'ha_job_id': 'str',
        'ray_job_submission_id': 'str',
        'cluster_id': 'str',
        'namespace_id': 'str',
        'environment_id': 'str',
        'project_id': 'str',
        'creator_id': 'str',
        'integration_execution_details_id': 'str',
        'bucket_log_prefix': 'str',
        'bucket_log_prefix_streaming': 'str',
        'cluster': 'MiniCluster',
        'integration_details': 'IntegrationDetails'
    }

    attribute_map = {
        'id': 'id',
        'ray_session_name': 'ray_session_name',
        'ray_job_id': 'ray_job_id',
        'name': 'name',
        'status': 'status',
        'created_at': 'created_at',
        'finished_at': 'finished_at',
        'ha_job_id': 'ha_job_id',
        'ray_job_submission_id': 'ray_job_submission_id',
        'cluster_id': 'cluster_id',
        'namespace_id': 'namespace_id',
        'environment_id': 'environment_id',
        'project_id': 'project_id',
        'creator_id': 'creator_id',
        'integration_execution_details_id': 'integration_execution_details_id',
        'bucket_log_prefix': 'bucket_log_prefix',
        'bucket_log_prefix_streaming': 'bucket_log_prefix_streaming',
        'cluster': 'cluster',
        'integration_details': 'integration_details'
    }

    def __init__(self, id=None, ray_session_name=None, ray_job_id=None, name=None, status=None, created_at=None, finished_at=None, ha_job_id=None, ray_job_submission_id=None, cluster_id=None, namespace_id='DEPRECATED_NAMESPACE_ID', environment_id=None, project_id=None, creator_id=None, integration_execution_details_id=None, bucket_log_prefix=None, bucket_log_prefix_streaming=None, cluster=None, integration_details=None, local_vars_configuration=None):  # noqa: E501
        """MiniJobRun - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._ray_session_name = None
        self._ray_job_id = None
        self._name = None
        self._status = None
        self._created_at = None
        self._finished_at = None
        self._ha_job_id = None
        self._ray_job_submission_id = None
        self._cluster_id = None
        self._namespace_id = None
        self._environment_id = None
        self._project_id = None
        self._creator_id = None
        self._integration_execution_details_id = None
        self._bucket_log_prefix = None
        self._bucket_log_prefix_streaming = None
        self._cluster = None
        self._integration_details = None
        self.discriminator = None

        self.id = id
        self.ray_session_name = ray_session_name
        self.ray_job_id = ray_job_id
        if name is not None:
            self.name = name
        self.status = status
        self.created_at = created_at
        if finished_at is not None:
            self.finished_at = finished_at
        if ha_job_id is not None:
            self.ha_job_id = ha_job_id
        if ray_job_submission_id is not None:
            self.ray_job_submission_id = ray_job_submission_id
        self.cluster_id = cluster_id
        if namespace_id is not None:
            self.namespace_id = namespace_id
        self.environment_id = environment_id
        if project_id is not None:
            self.project_id = project_id
        self.creator_id = creator_id
        if integration_execution_details_id is not None:
            self.integration_execution_details_id = integration_execution_details_id
        if bucket_log_prefix is not None:
            self.bucket_log_prefix = bucket_log_prefix
        if bucket_log_prefix_streaming is not None:
            self.bucket_log_prefix_streaming = bucket_log_prefix_streaming
        self.cluster = cluster
        if integration_details is not None:
            self.integration_details = integration_details

    @property
    def id(self):
        """Gets the id of this MiniJobRun.  # noqa: E501


        :return: The id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MiniJobRun.


        :param id: The id of this MiniJobRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def ray_session_name(self):
        """Gets the ray_session_name of this MiniJobRun.  # noqa: E501


        :return: The ray_session_name of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._ray_session_name

    @ray_session_name.setter
    def ray_session_name(self, ray_session_name):
        """Sets the ray_session_name of this MiniJobRun.


        :param ray_session_name: The ray_session_name of this MiniJobRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and ray_session_name is None:  # noqa: E501
            raise ValueError("Invalid value for `ray_session_name`, must not be `None`")  # noqa: E501

        self._ray_session_name = ray_session_name

    @property
    def ray_job_id(self):
        """Gets the ray_job_id of this MiniJobRun.  # noqa: E501


        :return: The ray_job_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._ray_job_id

    @ray_job_id.setter
    def ray_job_id(self, ray_job_id):
        """Sets the ray_job_id of this MiniJobRun.


        :param ray_job_id: The ray_job_id of this MiniJobRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and ray_job_id is None:  # noqa: E501
            raise ValueError("Invalid value for `ray_job_id`, must not be `None`")  # noqa: E501

        self._ray_job_id = ray_job_id

    @property
    def name(self):
        """Gets the name of this MiniJobRun.  # noqa: E501


        :return: The name of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MiniJobRun.


        :param name: The name of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def status(self):
        """Gets the status of this MiniJobRun.  # noqa: E501


        :return: The status of this MiniJobRun.  # noqa: E501
        :rtype: BaseJobStatus
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this MiniJobRun.


        :param status: The status of this MiniJobRun.  # noqa: E501
        :type: BaseJobStatus
        """
        if self.local_vars_configuration.client_side_validation and status is None:  # noqa: E501
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def created_at(self):
        """Gets the created_at of this MiniJobRun.  # noqa: E501


        :return: The created_at of this MiniJobRun.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this MiniJobRun.


        :param created_at: The created_at of this MiniJobRun.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def finished_at(self):
        """Gets the finished_at of this MiniJobRun.  # noqa: E501


        :return: The finished_at of this MiniJobRun.  # noqa: E501
        :rtype: datetime
        """
        return self._finished_at

    @finished_at.setter
    def finished_at(self, finished_at):
        """Sets the finished_at of this MiniJobRun.


        :param finished_at: The finished_at of this MiniJobRun.  # noqa: E501
        :type: datetime
        """

        self._finished_at = finished_at

    @property
    def ha_job_id(self):
        """Gets the ha_job_id of this MiniJobRun.  # noqa: E501


        :return: The ha_job_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._ha_job_id

    @ha_job_id.setter
    def ha_job_id(self, ha_job_id):
        """Sets the ha_job_id of this MiniJobRun.


        :param ha_job_id: The ha_job_id of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._ha_job_id = ha_job_id

    @property
    def ray_job_submission_id(self):
        """Gets the ray_job_submission_id of this MiniJobRun.  # noqa: E501


        :return: The ray_job_submission_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._ray_job_submission_id

    @ray_job_submission_id.setter
    def ray_job_submission_id(self, ray_job_submission_id):
        """Sets the ray_job_submission_id of this MiniJobRun.


        :param ray_job_submission_id: The ray_job_submission_id of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._ray_job_submission_id = ray_job_submission_id

    @property
    def cluster_id(self):
        """Gets the cluster_id of this MiniJobRun.  # noqa: E501


        :return: The cluster_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, cluster_id):
        """Sets the cluster_id of this MiniJobRun.


        :param cluster_id: The cluster_id of this MiniJobRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cluster_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster_id`, must not be `None`")  # noqa: E501

        self._cluster_id = cluster_id

    @property
    def namespace_id(self):
        """Gets the namespace_id of this MiniJobRun.  # noqa: E501

        ID of the Anyscale Namespace.  # noqa: E501

        :return: The namespace_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._namespace_id

    @namespace_id.setter
    def namespace_id(self, namespace_id):
        """Sets the namespace_id of this MiniJobRun.

        ID of the Anyscale Namespace.  # noqa: E501

        :param namespace_id: The namespace_id of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._namespace_id = namespace_id

    @property
    def environment_id(self):
        """Gets the environment_id of this MiniJobRun.  # noqa: E501


        :return: The environment_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._environment_id

    @environment_id.setter
    def environment_id(self, environment_id):
        """Sets the environment_id of this MiniJobRun.


        :param environment_id: The environment_id of this MiniJobRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and environment_id is None:  # noqa: E501
            raise ValueError("Invalid value for `environment_id`, must not be `None`")  # noqa: E501

        self._environment_id = environment_id

    @property
    def project_id(self):
        """Gets the project_id of this MiniJobRun.  # noqa: E501


        :return: The project_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this MiniJobRun.


        :param project_id: The project_id of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def creator_id(self):
        """Gets the creator_id of this MiniJobRun.  # noqa: E501


        :return: The creator_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this MiniJobRun.


        :param creator_id: The creator_id of this MiniJobRun.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def integration_execution_details_id(self):
        """Gets the integration_execution_details_id of this MiniJobRun.  # noqa: E501


        :return: The integration_execution_details_id of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._integration_execution_details_id

    @integration_execution_details_id.setter
    def integration_execution_details_id(self, integration_execution_details_id):
        """Sets the integration_execution_details_id of this MiniJobRun.


        :param integration_execution_details_id: The integration_execution_details_id of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._integration_execution_details_id = integration_execution_details_id

    @property
    def bucket_log_prefix(self):
        """Gets the bucket_log_prefix of this MiniJobRun.  # noqa: E501


        :return: The bucket_log_prefix of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._bucket_log_prefix

    @bucket_log_prefix.setter
    def bucket_log_prefix(self, bucket_log_prefix):
        """Sets the bucket_log_prefix of this MiniJobRun.


        :param bucket_log_prefix: The bucket_log_prefix of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._bucket_log_prefix = bucket_log_prefix

    @property
    def bucket_log_prefix_streaming(self):
        """Gets the bucket_log_prefix_streaming of this MiniJobRun.  # noqa: E501


        :return: The bucket_log_prefix_streaming of this MiniJobRun.  # noqa: E501
        :rtype: str
        """
        return self._bucket_log_prefix_streaming

    @bucket_log_prefix_streaming.setter
    def bucket_log_prefix_streaming(self, bucket_log_prefix_streaming):
        """Sets the bucket_log_prefix_streaming of this MiniJobRun.


        :param bucket_log_prefix_streaming: The bucket_log_prefix_streaming of this MiniJobRun.  # noqa: E501
        :type: str
        """

        self._bucket_log_prefix_streaming = bucket_log_prefix_streaming

    @property
    def cluster(self):
        """Gets the cluster of this MiniJobRun.  # noqa: E501


        :return: The cluster of this MiniJobRun.  # noqa: E501
        :rtype: MiniCluster
        """
        return self._cluster

    @cluster.setter
    def cluster(self, cluster):
        """Sets the cluster of this MiniJobRun.


        :param cluster: The cluster of this MiniJobRun.  # noqa: E501
        :type: MiniCluster
        """
        if self.local_vars_configuration.client_side_validation and cluster is None:  # noqa: E501
            raise ValueError("Invalid value for `cluster`, must not be `None`")  # noqa: E501

        self._cluster = cluster

    @property
    def integration_details(self):
        """Gets the integration_details of this MiniJobRun.  # noqa: E501


        :return: The integration_details of this MiniJobRun.  # noqa: E501
        :rtype: IntegrationDetails
        """
        return self._integration_details

    @integration_details.setter
    def integration_details(self, integration_details):
        """Sets the integration_details of this MiniJobRun.


        :param integration_details: The integration_details of this MiniJobRun.  # noqa: E501
        :type: IntegrationDetails
        """

        self._integration_details = integration_details

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
        if not isinstance(other, MiniJobRun):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, MiniJobRun):
            return True

        return self.to_dict() != other.to_dict()
