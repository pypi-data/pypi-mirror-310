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


class AicaEndpoint(object):
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
        'aviary_version': 'str',
        'service_id': 'str',
        'model_config': 'object',
        'id': 'str',
        'created_at': 'datetime',
        'creator_id': 'str',
        'creator_email': 'str',
        'creator_deleted_at': 'datetime',
        'archived_at': 'datetime',
        'cloud_id': 'str',
        'project_id': 'str',
        'organization_id': 'str',
        'aica_observability_urls': 'AicaObservabilityUrls',
        'state': 'ServiceEventCurrentState'
    }

    attribute_map = {
        'name': 'name',
        'aviary_version': 'aviary_version',
        'service_id': 'service_id',
        'model_config': 'model_config',
        'id': 'id',
        'created_at': 'created_at',
        'creator_id': 'creator_id',
        'creator_email': 'creator_email',
        'creator_deleted_at': 'creator_deleted_at',
        'archived_at': 'archived_at',
        'cloud_id': 'cloud_id',
        'project_id': 'project_id',
        'organization_id': 'organization_id',
        'aica_observability_urls': 'aica_observability_urls',
        'state': 'state'
    }

    def __init__(self, name=None, aviary_version=None, service_id=None, model_config=None, id=None, created_at=None, creator_id=None, creator_email=None, creator_deleted_at=None, archived_at=None, cloud_id=None, project_id=None, organization_id=None, aica_observability_urls=None, state=None, local_vars_configuration=None):  # noqa: E501
        """AicaEndpoint - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._aviary_version = None
        self._service_id = None
        self._model_config = None
        self._id = None
        self._created_at = None
        self._creator_id = None
        self._creator_email = None
        self._creator_deleted_at = None
        self._archived_at = None
        self._cloud_id = None
        self._project_id = None
        self._organization_id = None
        self._aica_observability_urls = None
        self._state = None
        self.discriminator = None

        self.name = name
        self.aviary_version = aviary_version
        self.service_id = service_id
        self.model_config = model_config
        self.id = id
        self.created_at = created_at
        self.creator_id = creator_id
        self.creator_email = creator_email
        if creator_deleted_at is not None:
            self.creator_deleted_at = creator_deleted_at
        if archived_at is not None:
            self.archived_at = archived_at
        self.cloud_id = cloud_id
        self.project_id = project_id
        self.organization_id = organization_id
        self.aica_observability_urls = aica_observability_urls
        self.state = state

    @property
    def name(self):
        """Gets the name of this AicaEndpoint.  # noqa: E501

        Name of the endpoint to be created.  # noqa: E501

        :return: The name of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this AicaEndpoint.

        Name of the endpoint to be created.  # noqa: E501

        :param name: The name of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def aviary_version(self):
        """Gets the aviary_version of this AicaEndpoint.  # noqa: E501

        The version of aviary that this endpoint is running.  # noqa: E501

        :return: The aviary_version of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._aviary_version

    @aviary_version.setter
    def aviary_version(self, aviary_version):
        """Sets the aviary_version of this AicaEndpoint.

        The version of aviary that this endpoint is running.  # noqa: E501

        :param aviary_version: The aviary_version of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and aviary_version is None:  # noqa: E501
            raise ValueError("Invalid value for `aviary_version`, must not be `None`")  # noqa: E501

        self._aviary_version = aviary_version

    @property
    def service_id(self):
        """Gets the service_id of this AicaEndpoint.  # noqa: E501

        Id of the associated service.  # noqa: E501

        :return: The service_id of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._service_id

    @service_id.setter
    def service_id(self, service_id):
        """Sets the service_id of this AicaEndpoint.

        Id of the associated service.  # noqa: E501

        :param service_id: The service_id of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and service_id is None:  # noqa: E501
            raise ValueError("Invalid value for `service_id`, must not be `None`")  # noqa: E501

        self._service_id = service_id

    @property
    def model_config(self):
        """Gets the model_config of this AicaEndpoint.  # noqa: E501

        The configuration for the endpoints models. Key is the model id.  # noqa: E501

        :return: The model_config of this AicaEndpoint.  # noqa: E501
        :rtype: object
        """
        return self._model_config

    @model_config.setter
    def model_config(self, model_config):
        """Sets the model_config of this AicaEndpoint.

        The configuration for the endpoints models. Key is the model id.  # noqa: E501

        :param model_config: The model_config of this AicaEndpoint.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and model_config is None:  # noqa: E501
            raise ValueError("Invalid value for `model_config`, must not be `None`")  # noqa: E501

        self._model_config = model_config

    @property
    def id(self):
        """Gets the id of this AicaEndpoint.  # noqa: E501

        Server assigned unique identifier of the endpoint.  # noqa: E501

        :return: The id of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this AicaEndpoint.

        Server assigned unique identifier of the endpoint.  # noqa: E501

        :param id: The id of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def created_at(self):
        """Gets the created_at of this AicaEndpoint.  # noqa: E501

        Time at which endpoint was created.  # noqa: E501

        :return: The created_at of this AicaEndpoint.  # noqa: E501
        :rtype: datetime
        """
        return self._created_at

    @created_at.setter
    def created_at(self, created_at):
        """Sets the created_at of this AicaEndpoint.

        Time at which endpoint was created.  # noqa: E501

        :param created_at: The created_at of this AicaEndpoint.  # noqa: E501
        :type: datetime
        """
        if self.local_vars_configuration.client_side_validation and created_at is None:  # noqa: E501
            raise ValueError("Invalid value for `created_at`, must not be `None`")  # noqa: E501

        self._created_at = created_at

    @property
    def creator_id(self):
        """Gets the creator_id of this AicaEndpoint.  # noqa: E501

        Identifier of user who created the endpoint.  # noqa: E501

        :return: The creator_id of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._creator_id

    @creator_id.setter
    def creator_id(self, creator_id):
        """Sets the creator_id of this AicaEndpoint.

        Identifier of user who created the endpoint.  # noqa: E501

        :param creator_id: The creator_id of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_id is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_id`, must not be `None`")  # noqa: E501

        self._creator_id = creator_id

    @property
    def creator_email(self):
        """Gets the creator_email of this AicaEndpoint.  # noqa: E501

        Email of user who created the endpoint.  # noqa: E501

        :return: The creator_email of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._creator_email

    @creator_email.setter
    def creator_email(self, creator_email):
        """Sets the creator_email of this AicaEndpoint.

        Email of user who created the endpoint.  # noqa: E501

        :param creator_email: The creator_email of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and creator_email is None:  # noqa: E501
            raise ValueError("Invalid value for `creator_email`, must not be `None`")  # noqa: E501

        self._creator_email = creator_email

    @property
    def creator_deleted_at(self):
        """Gets the creator_deleted_at of this AicaEndpoint.  # noqa: E501

        Timestamp of when the user who created the endpoint was deleted.  # noqa: E501

        :return: The creator_deleted_at of this AicaEndpoint.  # noqa: E501
        :rtype: datetime
        """
        return self._creator_deleted_at

    @creator_deleted_at.setter
    def creator_deleted_at(self, creator_deleted_at):
        """Sets the creator_deleted_at of this AicaEndpoint.

        Timestamp of when the user who created the endpoint was deleted.  # noqa: E501

        :param creator_deleted_at: The creator_deleted_at of this AicaEndpoint.  # noqa: E501
        :type: datetime
        """

        self._creator_deleted_at = creator_deleted_at

    @property
    def archived_at(self):
        """Gets the archived_at of this AicaEndpoint.  # noqa: E501

        The time in which this instance is archived.  # noqa: E501

        :return: The archived_at of this AicaEndpoint.  # noqa: E501
        :rtype: datetime
        """
        return self._archived_at

    @archived_at.setter
    def archived_at(self, archived_at):
        """Sets the archived_at of this AicaEndpoint.

        The time in which this instance is archived.  # noqa: E501

        :param archived_at: The archived_at of this AicaEndpoint.  # noqa: E501
        :type: datetime
        """

        self._archived_at = archived_at

    @property
    def cloud_id(self):
        """Gets the cloud_id of this AicaEndpoint.  # noqa: E501

        The cloud id for the endpoint.  # noqa: E501

        :return: The cloud_id of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._cloud_id

    @cloud_id.setter
    def cloud_id(self, cloud_id):
        """Sets the cloud_id of this AicaEndpoint.

        The cloud id for the endpoint.  # noqa: E501

        :param cloud_id: The cloud_id of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and cloud_id is None:  # noqa: E501
            raise ValueError("Invalid value for `cloud_id`, must not be `None`")  # noqa: E501

        self._cloud_id = cloud_id

    @property
    def project_id(self):
        """Gets the project_id of this AicaEndpoint.  # noqa: E501

        Id of the project that this endpoint belongs to.  # noqa: E501

        :return: The project_id of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this AicaEndpoint.

        Id of the project that this endpoint belongs to.  # noqa: E501

        :param project_id: The project_id of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and project_id is None:  # noqa: E501
            raise ValueError("Invalid value for `project_id`, must not be `None`")  # noqa: E501

        self._project_id = project_id

    @property
    def organization_id(self):
        """Gets the organization_id of this AicaEndpoint.  # noqa: E501

        Id of the organization that this endpoint belongs to  # noqa: E501

        :return: The organization_id of this AicaEndpoint.  # noqa: E501
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id):
        """Sets the organization_id of this AicaEndpoint.

        Id of the organization that this endpoint belongs to  # noqa: E501

        :param organization_id: The organization_id of this AicaEndpoint.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and organization_id is None:  # noqa: E501
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def aica_observability_urls(self):
        """Gets the aica_observability_urls of this AicaEndpoint.  # noqa: E501

        A JSON object with useful urls pointing to Grafana dashboards.  # noqa: E501

        :return: The aica_observability_urls of this AicaEndpoint.  # noqa: E501
        :rtype: AicaObservabilityUrls
        """
        return self._aica_observability_urls

    @aica_observability_urls.setter
    def aica_observability_urls(self, aica_observability_urls):
        """Sets the aica_observability_urls of this AicaEndpoint.

        A JSON object with useful urls pointing to Grafana dashboards.  # noqa: E501

        :param aica_observability_urls: The aica_observability_urls of this AicaEndpoint.  # noqa: E501
        :type: AicaObservabilityUrls
        """
        if self.local_vars_configuration.client_side_validation and aica_observability_urls is None:  # noqa: E501
            raise ValueError("Invalid value for `aica_observability_urls`, must not be `None`")  # noqa: E501

        self._aica_observability_urls = aica_observability_urls

    @property
    def state(self):
        """Gets the state of this AicaEndpoint.  # noqa: E501

        The status of the endpoint.  # noqa: E501

        :return: The state of this AicaEndpoint.  # noqa: E501
        :rtype: ServiceEventCurrentState
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this AicaEndpoint.

        The status of the endpoint.  # noqa: E501

        :param state: The state of this AicaEndpoint.  # noqa: E501
        :type: ServiceEventCurrentState
        """
        if self.local_vars_configuration.client_side_validation and state is None:  # noqa: E501
            raise ValueError("Invalid value for `state`, must not be `None`")  # noqa: E501

        self._state = state

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
        if not isinstance(other, AicaEndpoint):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, AicaEndpoint):
            return True

        return self.to_dict() != other.to_dict()
