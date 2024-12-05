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


class CreateSession(object):
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
        'name': 'str',
        'project_id': 'str',
        'cloud_id': 'str',
        'cluster_config': 'str',
        'build_id': 'str',
        'compute_template_id': 'str',
        'idle_timeout': 'int',
        'uses_app_config': 'bool',
        'allow_public_internet_traffic': 'bool',
        'user_service_access': 'UserServiceAccessTypes',
        'user_service_token': 'str',
        'ha_job_id': 'str'
    }

    attribute_map = {
        'name': 'name',
        'project_id': 'project_id',
        'cloud_id': 'cloud_id',
        'cluster_config': 'cluster_config',
        'build_id': 'build_id',
        'compute_template_id': 'compute_template_id',
        'idle_timeout': 'idle_timeout',
        'uses_app_config': 'uses_app_config',
        'allow_public_internet_traffic': 'allow_public_internet_traffic',
        'user_service_access': 'user_service_access',
        'user_service_token': 'user_service_token',
        'ha_job_id': 'ha_job_id'
    }

    def __init__(self, name=None, project_id=None, cloud_id=None, cluster_config=None, build_id=None, compute_template_id=None, idle_timeout=None, uses_app_config=False, allow_public_internet_traffic=False, user_service_access=None, user_service_token=None, ha_job_id=None, local_vars_configuration=None):  # noqa: E501
        """CreateSession - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._project_id = None
        self._cloud_id = None
        self._cluster_config = None
        self._build_id = None
        self._compute_template_id = None
        self._idle_timeout = None
        self._uses_app_config = None
        self._allow_public_internet_traffic = None
        self._user_service_access = None
        self._user_service_token = None
        self._ha_job_id = None
        self.discriminator = None

        self.name = name
        self.project_id = project_id
        if cloud_id is not None:
            self.cloud_id = cloud_id
        if cluster_config is not None:
            self.cluster_config = cluster_config
        if build_id is not None:
            self.build_id = build_id
        if compute_template_id is not None:
            self.compute_template_id = compute_template_id
        if idle_timeout is not None:
            self.idle_timeout = idle_timeout
        if uses_app_config is not None:
            self.uses_app_config = uses_app_config
        if allow_public_internet_traffic is not None:
            self.allow_public_internet_traffic = allow_public_internet_traffic
        if user_service_access is not None:
            self.user_service_access = user_service_access
        if user_service_token is not None:
            self.user_service_token = user_service_token
        if ha_job_id is not None:
            self.ha_job_id = ha_job_id

    @property
    def name(self):
        """Gets the name of this CreateSession.  # noqa: E501

        Name of the session to be created.  # noqa: E501

        :return: The name of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this CreateSession.

        Name of the session to be created.  # noqa: E501

        :param name: The name of this CreateSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def project_id(self):
        """Gets the project_id of this CreateSession.  # noqa: E501

        Project that the session will be created in.  # noqa: E501

        :return: The project_id of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this CreateSession.

        Project that the session will be created in.  # noqa: E501

        :param project_id: The project_id of this CreateSession.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def cloud_id(self):
        """Gets the cloud_id of this CreateSession.  # noqa: E501

        Cloud that the session will use.  # noqa: E501

        :return: The cloud_id of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this CreateSession.

        Cloud that the session will use.  # noqa: E501

        :param cloud_id: The cloud_id of this CreateSession.  # noqa: E501
        :type: str
        """

        self._cloud_id = cloud_id

    @property
    def cluster_config(self):
        """Gets the cluster_config of this CreateSession.  # noqa: E501

        Cluster config that the session can later be started with.  # noqa: E501

        :return: The cluster_config of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._cluster_config

    @cluster_config.setter
    def cluster_config(self, cluster_config):
        """Sets the cluster_config of this CreateSession.

        Cluster config that the session can later be started with.  # noqa: E501

        :param cluster_config: The cluster_config of this CreateSession.  # noqa: E501
        :type: str
        """

        self._cluster_config = cluster_config

    @property
    def build_id(self):
        """Gets the build_id of this CreateSession.  # noqa: E501

        ID of the Build that this session was started with.  # noqa: E501

        :return: The build_id of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._build_id

    @build_id.setter
    def build_id(self, build_id):
        """Sets the build_id of this CreateSession.

        ID of the Build that this session was started with.  # noqa: E501

        :param build_id: The build_id of this CreateSession.  # noqa: E501
        :type: str
        """

        self._build_id = build_id

    @property
    def compute_template_id(self):
        """Gets the compute_template_id of this CreateSession.  # noqa: E501

        ID of the compute template that this session was started with.  # noqa: E501

        :return: The compute_template_id of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._compute_template_id

    @compute_template_id.setter
    def compute_template_id(self, compute_template_id):
        """Sets the compute_template_id of this CreateSession.

        ID of the compute template that this session was started with.  # noqa: E501

        :param compute_template_id: The compute_template_id of this CreateSession.  # noqa: E501
        :type: str
        """

        self._compute_template_id = compute_template_id

    @property
    def idle_timeout(self):
        """Gets the idle_timeout of this CreateSession.  # noqa: E501

        Idle timeout (in minutes), after which the session is stopped. Idle time is defined as the time during which a session is not running a user command (through 'anyscale exec' or the Web UI), and does not have an attached driver. Time spent running Jupyter commands, or commands run through ssh, is still considered 'idle'.  # noqa: E501

        :return: The idle_timeout of this CreateSession.  # noqa: E501
        :rtype: int
        """
        return self._idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, idle_timeout):
        """Sets the idle_timeout of this CreateSession.

        Idle timeout (in minutes), after which the session is stopped. Idle time is defined as the time during which a session is not running a user command (through 'anyscale exec' or the Web UI), and does not have an attached driver. Time spent running Jupyter commands, or commands run through ssh, is still considered 'idle'.  # noqa: E501

        :param idle_timeout: The idle_timeout of this CreateSession.  # noqa: E501
        :type: int
        """

        self._idle_timeout = idle_timeout

    @property
    def uses_app_config(self):
        """Gets the uses_app_config of this CreateSession.  # noqa: E501

        Whether or not the session uses app config. If true, it means this is not a legacy session started with cluster yaml.  # noqa: E501

        :return: The uses_app_config of this CreateSession.  # noqa: E501
        :rtype: bool
        """
        return self._uses_app_config

    @uses_app_config.setter
    def uses_app_config(self, uses_app_config):
        """Sets the uses_app_config of this CreateSession.

        Whether or not the session uses app config. If true, it means this is not a legacy session started with cluster yaml.  # noqa: E501

        :param uses_app_config: The uses_app_config of this CreateSession.  # noqa: E501
        :type: bool
        """

        self._uses_app_config = uses_app_config

    @property
    def allow_public_internet_traffic(self):
        """Gets the allow_public_internet_traffic of this CreateSession.  # noqa: E501

        Whether public internet traffic can access Serve endpoints or if an authentication token is required.  # noqa: E501

        :return: The allow_public_internet_traffic of this CreateSession.  # noqa: E501
        :rtype: bool
        """
        return self._allow_public_internet_traffic

    @allow_public_internet_traffic.setter
    def allow_public_internet_traffic(self, allow_public_internet_traffic):
        """Sets the allow_public_internet_traffic of this CreateSession.

        Whether public internet traffic can access Serve endpoints or if an authentication token is required.  # noqa: E501

        :param allow_public_internet_traffic: The allow_public_internet_traffic of this CreateSession.  # noqa: E501
        :type: bool
        """

        self._allow_public_internet_traffic = allow_public_internet_traffic

    @property
    def user_service_access(self):
        """Gets the user_service_access of this CreateSession.  # noqa: E501

        Whether user service can be accessed by public internet traffic.  # noqa: E501

        :return: The user_service_access of this CreateSession.  # noqa: E501
        :rtype: UserServiceAccessTypes
        """
        return self._user_service_access

    @user_service_access.setter
    def user_service_access(self, user_service_access):
        """Sets the user_service_access of this CreateSession.

        Whether user service can be accessed by public internet traffic.  # noqa: E501

        :param user_service_access: The user_service_access of this CreateSession.  # noqa: E501
        :type: UserServiceAccessTypes
        """

        self._user_service_access = user_service_access

    @property
    def user_service_token(self):
        """Gets the user_service_token of this CreateSession.  # noqa: E501

        User service token that is used to authenticate access to public user services. This must be a valid 32 byte URL safe string and can be generated by calling `secrets.token_urlsafe(32))`. This is ignored if the user service has private access. If not specified for a public user service, a token is autogenerated.  # noqa: E501

        :return: The user_service_token of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._user_service_token

    @user_service_token.setter
    def user_service_token(self, user_service_token):
        """Sets the user_service_token of this CreateSession.

        User service token that is used to authenticate access to public user services. This must be a valid 32 byte URL safe string and can be generated by calling `secrets.token_urlsafe(32))`. This is ignored if the user service has private access. If not specified for a public user service, a token is autogenerated.  # noqa: E501

        :param user_service_token: The user_service_token of this CreateSession.  # noqa: E501
        :type: str
        """

        self._user_service_token = user_service_token

    @property
    def ha_job_id(self):
        """Gets the ha_job_id of this CreateSession.  # noqa: E501

        This is used internally by Anyscale to associate clusters to a job. It is set automatically and should *not* be used directly.  # noqa: E501

        :return: The ha_job_id of this CreateSession.  # noqa: E501
        :rtype: str
        """
        return self._ha_job_id

    @ha_job_id.setter
    def ha_job_id(self, ha_job_id):
        """Sets the ha_job_id of this CreateSession.

        This is used internally by Anyscale to associate clusters to a job. It is set automatically and should *not* be used directly.  # noqa: E501

        :param ha_job_id: The ha_job_id of this CreateSession.  # noqa: E501
        :type: str
        """

        self._ha_job_id = ha_job_id

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
        if not isinstance(other, CreateSession):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, CreateSession):
            return True

        return self.to_dict() != other.to_dict()
