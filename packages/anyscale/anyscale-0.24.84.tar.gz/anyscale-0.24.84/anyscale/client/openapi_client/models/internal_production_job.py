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


class InternalProductionJob(object):
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
        'description': 'str',
        'created_at': 'datetime',
        'creator_id': 'str',
        'config': 'ProductionJobConfig',
        'job_queue_config': 'JobQueueConfig',
        'state': 'ProductionJobStateTransition',
        'project_id': 'str',
        'last_job_run_id': 'str',
        'schedule_id': 'str',
        'job_queue_id': 'str',
        'is_service': 'bool',
        'cost_dollars': 'float',
        'url': 'str',
        'token': 'str',
        'access': 'UserServiceAccessTypes',
        'healthcheck_url': 'str',
        'archived_at': 'datetime',
        'cloud_id': 'str'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'created_at': 'created_at',
        'creator_id': 'creator_id',
        'config': 'config',
        'job_queue_config': 'job_queue_config',
        'state': 'state',
        'project_id': 'project_id',
        'last_job_run_id': 'last_job_run_id',
        'schedule_id': 'schedule_id',
        'job_queue_id': 'job_queue_id',
        'is_service': 'is_service',
        'cost_dollars': 'cost_dollars',
        'url': 'url',
        'token': 'token',
        'access': 'access',
        'healthcheck_url': 'healthcheck_url',
        'archived_at': 'archived_at',
        'cloud_id': 'cloud_id'
    }

    def __init__(self, id=None, name=None, description=None, created_at=None, creator_id=None, config=None, job_queue_config=None, state=None, project_id=None, last_job_run_id=None, schedule_id=None, job_queue_id=None, is_service=None, cost_dollars=None, url=None, token=None, access=None, healthcheck_url=None, archived_at=None, cloud_id=None, local_vars_configuration=None):  # noqa: E501
        """InternalProductionJob - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._name = None
        self._description = None
        self._created_at = None
        self._creator_id = None
        self._config = None
        self._job_queue_config = None
        self._state = None
        self._project_id = None
        self._last_job_run_id = None
        self._schedule_id = None
        self._job_queue_id = None
        self._is_service = None
        self._cost_dollars = None
        self._url = None
        self._token = None
        self._access = None
        self._healthcheck_url = None
        self._archived_at = None
        self._cloud_id = None
        self.discriminator = None

        self.id = id
        self.name = name
        if description is not None:
            self.description = description
        self.created_at = created_at
        self.creator_id = creator_id
        self.config = config
        if job_queue_config is not None:
            self.job_queue_config = job_queue_config
        self.state = state
        self.project_id = project_id
        if last_job_run_id is not None:
            self.last_job_run_id = last_job_run_id
        if schedule_id is not None:
            self.schedule_id = schedule_id
        if job_queue_id is not None:
            self.job_queue_id = job_queue_id
        self.is_service = is_service
        if cost_dollars is not None:
            self.cost_dollars = cost_dollars
        if url is not None:
            self.url = url
        if token is not None:
            self.token = token
        if access is not None:
            self.access = access
        if healthcheck_url is not None:
            self.healthcheck_url = healthcheck_url
        if archived_at is not None:
            self.archived_at = archived_at
        self.cloud_id = cloud_id

    @property
    def id(self):
        """Gets the id of this InternalProductionJob.  # noqa: E501

        The id of this job  # noqa: E501

        :return: The id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this InternalProductionJob.

        The id of this job  # noqa: E501

        :param id: The id of this InternalProductionJob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def name(self):
        """Gets the name of this InternalProductionJob.  # noqa: E501

        Name of the job  # noqa: E501

        :return: The name of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this InternalProductionJob.

        Name of the job  # noqa: E501

        :param name: The name of this InternalProductionJob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this InternalProductionJob.  # noqa: E501

        Description of the job  # noqa: E501

        :return: The description of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this InternalProductionJob.

        Description of the job  # noqa: E501

        :param description: The description of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def created_at(self):
        """Gets the created_at of this InternalProductionJob.  # noqa: E501

        The time this job was created  # noqa: E501

        :return: The created_at of this InternalProductionJob.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this InternalProductionJob.

        The time this job was created  # noqa: E501

        :param created_at: The created_at of this InternalProductionJob.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def creator_id(self):
        """Gets the creator_id of this InternalProductionJob.  # noqa: E501

        The id of the user who created this job  # noqa: E501

        :return: The creator_id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this InternalProductionJob.

        The id of the user who created this job  # noqa: E501

        :param creator_id: The creator_id of this InternalProductionJob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def config(self):
        """Gets the config of this InternalProductionJob.  # noqa: E501

        The config that was used to create this job  # noqa: E501

        :return: The config of this InternalProductionJob.  # noqa: E501
        :rtype: ProductionJobConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this InternalProductionJob.

        The config that was used to create this job  # noqa: E501

        :param config: The config of this InternalProductionJob.  # noqa: E501
        :type: ProductionJobConfig
        """
        if self.local_vars_configuration.client_side_validation and config is None:  # noqa: E501
            raise ValueError("Invalid value for `config`, must not be `None`")  # noqa: E501

        self._config = config

    @property
    def job_queue_config(self):
        """Gets the job_queue_config of this InternalProductionJob.  # noqa: E501

        Job Queue configuration of this job (if applicable)  # noqa: E501

        :return: The job_queue_config of this InternalProductionJob.  # noqa: E501
        :rtype: JobQueueConfig
        """
        return self._job_queue_config

    @job_queue_config.setter
    def job_queue_config(self, job_queue_config):
        """Sets the job_queue_config of this InternalProductionJob.

        Job Queue configuration of this job (if applicable)  # noqa: E501

        :param job_queue_config: The job_queue_config of this InternalProductionJob.  # noqa: E501
        :type: JobQueueConfig
        """

        self._job_queue_config = job_queue_config

    @property
    def state(self):
        """Gets the state of this InternalProductionJob.  # noqa: E501

        The current state of this job  # noqa: E501

        :return: The state of this InternalProductionJob.  # noqa: E501
        :rtype: ProductionJobStateTransition
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this InternalProductionJob.

        The current state of this job  # noqa: E501

        :param state: The state of this InternalProductionJob.  # noqa: E501
        :type: ProductionJobStateTransition
        """
        if self.local_vars_configuration.client_side_validation and state is None:  # noqa: E501
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

    @property
    def project_id(self):
        """Gets the project_id of this InternalProductionJob.  # noqa: E501

        Id of the project this job will start clusters in  # noqa: E501

        :return: The project_id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this InternalProductionJob.

        Id of the project this job will start clusters in  # noqa: E501

        :param project_id: The project_id of this InternalProductionJob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def last_job_run_id(self):
        """Gets the last_job_run_id of this InternalProductionJob.  # noqa: E501

        The id of the last job run  # noqa: E501

        :return: The last_job_run_id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._last_job_run_id

    @last_job_run_id.setter
    def last_job_run_id(self, last_job_run_id):
        """Sets the last_job_run_id of this InternalProductionJob.

        The id of the last job run  # noqa: E501

        :param last_job_run_id: The last_job_run_id of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._last_job_run_id = last_job_run_id

    @property
    def schedule_id(self):
        """Gets the schedule_id of this InternalProductionJob.  # noqa: E501

        If the job was launched via Scheduled job, this will contain the id of that schedule.  # noqa: E501

        :return: The schedule_id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._schedule_id

    @schedule_id.setter
    def schedule_id(self, schedule_id):
        """Sets the schedule_id of this InternalProductionJob.

        If the job was launched via Scheduled job, this will contain the id of that schedule.  # noqa: E501

        :param schedule_id: The schedule_id of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._schedule_id = schedule_id

    @property
    def job_queue_id(self):
        """Gets the job_queue_id of this InternalProductionJob.  # noqa: E501

        Id of the job queue this job is being enqueued to  # noqa: E501

        :return: The job_queue_id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._job_queue_id

    @job_queue_id.setter
    def job_queue_id(self, job_queue_id):
        """Sets the job_queue_id of this InternalProductionJob.

        Id of the job queue this job is being enqueued to  # noqa: E501

        :param job_queue_id: The job_queue_id of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._job_queue_id = job_queue_id

    @property
    def is_service(self):
        """Gets the is_service of this InternalProductionJob.  # noqa: E501

        Indicates if this job is runs with indefinitely with HA  # noqa: E501

        :return: The is_service of this InternalProductionJob.  # noqa: E501
        :rtype: bool
        """
        return self._is_service

    @is_service.setter
    def is_service(self, is_service):
        """Sets the is_service of this InternalProductionJob.

        Indicates if this job is runs with indefinitely with HA  # noqa: E501

        :param is_service: The is_service of this InternalProductionJob.  # noqa: E501
        :type: bool
        """
        if self.local_vars_configuration.client_side_validation and is_service is None:  # noqa: E501
            raise ValueError("Invalid value for `is_service`, must not be `None`")  # noqa: E501

        self._is_service = is_service

    @property
    def cost_dollars(self):
        """Gets the cost_dollars of this InternalProductionJob.  # noqa: E501

        The total cost, in dollars, of the ha job. This is the sum of all job runs   # noqa: E501

        :return: The cost_dollars of this InternalProductionJob.  # noqa: E501
        :rtype: float
        """
        return self._cost_dollars

    @cost_dollars.setter
    def cost_dollars(self, cost_dollars):
        """Sets the cost_dollars of this InternalProductionJob.

        The total cost, in dollars, of the ha job. This is the sum of all job runs   # noqa: E501

        :param cost_dollars: The cost_dollars of this InternalProductionJob.  # noqa: E501
        :type: float
        """

        self._cost_dollars = cost_dollars

    @property
    def url(self):
        """Gets the url of this InternalProductionJob.  # noqa: E501

        URL to access deployment running in service  # noqa: E501

        :return: The url of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url):
        """Sets the url of this InternalProductionJob.

        URL to access deployment running in service  # noqa: E501

        :param url: The url of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._url = url

    @property
    def token(self):
        """Gets the token of this InternalProductionJob.  # noqa: E501

        Token used to authenticate user service if it is accessible to public internet. This field will beempty if user service is not publically accessible.  # noqa: E501

        :return: The token of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this InternalProductionJob.

        Token used to authenticate user service if it is accessible to public internet. This field will beempty if user service is not publically accessible.  # noqa: E501

        :param token: The token of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._token = token

    @property
    def access(self):
        """Gets the access of this InternalProductionJob.  # noqa: E501

        Whether service can be accessed by public internet traffic.  # noqa: E501

        :return: The access of this InternalProductionJob.  # noqa: E501
        :rtype: UserServiceAccessTypes
        """
        return self._access

    @access.setter
    def access(self, access):
        """Sets the access of this InternalProductionJob.

        Whether service can be accessed by public internet traffic.  # noqa: E501

        :param access: The access of this InternalProductionJob.  # noqa: E501
        :type: UserServiceAccessTypes
        """

        self._access = access

    @property
    def healthcheck_url(self):
        """Gets the healthcheck_url of this InternalProductionJob.  # noqa: E501

        The healthcheck url. Anyscale will poll this url to determine whether the service is healthy or not. Only present for services  # noqa: E501

        :return: The healthcheck_url of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._healthcheck_url

    @healthcheck_url.setter
    def healthcheck_url(self, healthcheck_url):
        """Sets the healthcheck_url of this InternalProductionJob.

        The healthcheck url. Anyscale will poll this url to determine whether the service is healthy or not. Only present for services  # noqa: E501

        :param healthcheck_url: The healthcheck_url of this InternalProductionJob.  # noqa: E501
        :type: str
        """

        self._healthcheck_url = healthcheck_url

    @property
    def archived_at(self):
        """Gets the archived_at of this InternalProductionJob.  # noqa: E501

        The time in which this instance is archived.  # noqa: E501

        :return: The archived_at of this InternalProductionJob.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this InternalProductionJob.

        The time in which this instance is archived.  # noqa: E501

        :param archived_at: The archived_at of this InternalProductionJob.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def cloud_id(self):
        """Gets the cloud_id of this InternalProductionJob.  # noqa: E501

        The id of the cloud to which the job belongs.  # noqa: E501

        :return: The cloud_id of this InternalProductionJob.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this InternalProductionJob.

        The id of the cloud to which the job belongs.  # noqa: E501

        :param cloud_id: The cloud_id of this InternalProductionJob.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

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
        if not isinstance(other, InternalProductionJob):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, InternalProductionJob):
            return True

        return self.to_dict() != other.to_dict()
