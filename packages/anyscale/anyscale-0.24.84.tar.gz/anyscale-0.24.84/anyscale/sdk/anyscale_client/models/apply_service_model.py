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


class ApplyServiceModel(object):
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
        'description': 'str',
        'project_id': 'str',
        'version': 'str',
        'canary_percent': 'int',
        'ray_serve_config': 'object',
        'build_id': 'str',
        'compute_config_id': 'str',
        'config': 'ServiceConfig',
        'rollout_strategy': 'RolloutStrategy',
        'ray_gcs_external_storage_config': 'RayGCSExternalStorageConfig',
        'tracing_config': 'TracingConfig',
        'auto_complete_rollout': 'bool',
        'max_surge_percent': 'int'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'project_id': 'project_id',
        'version': 'version',
        'canary_percent': 'canary_percent',
        'ray_serve_config': 'ray_serve_config',
        'build_id': 'build_id',
        'compute_config_id': 'compute_config_id',
        'config': 'config',
        'rollout_strategy': 'rollout_strategy',
        'ray_gcs_external_storage_config': 'ray_gcs_external_storage_config',
        'tracing_config': 'tracing_config',
        'auto_complete_rollout': 'auto_complete_rollout',
        'max_surge_percent': 'max_surge_percent'
    }

    def __init__(self, name=None, description=None, project_id=None, version=None, canary_percent=None, ray_serve_config=None, build_id=None, compute_config_id=None, config=None, rollout_strategy=None, ray_gcs_external_storage_config=None, tracing_config=None, auto_complete_rollout=True, max_surge_percent=None, local_vars_configuration=None):  # noqa: E501
        """ApplyServiceModel - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._name = None
        self._description = None
        self._project_id = None
        self._version = None
        self._canary_percent = None
        self._ray_serve_config = None
        self._build_id = None
        self._compute_config_id = None
        self._config = None
        self._rollout_strategy = None
        self._ray_gcs_external_storage_config = None
        self._tracing_config = None
        self._auto_complete_rollout = None
        self._max_surge_percent = None
        self.discriminator = None

        self.name = name
        if description is not None:
            self.description = description
        if project_id is not None:
            self.project_id = project_id
        if version is not None:
            self.version = version
        if canary_percent is not None:
            self.canary_percent = canary_percent
        self.ray_serve_config = ray_serve_config
        self.build_id = build_id
        self.compute_config_id = compute_config_id
        if config is not None:
            self.config = config
        if rollout_strategy is not None:
            self.rollout_strategy = rollout_strategy
        if ray_gcs_external_storage_config is not None:
            self.ray_gcs_external_storage_config = ray_gcs_external_storage_config
        if tracing_config is not None:
            self.tracing_config = tracing_config
        if auto_complete_rollout is not None:
            self.auto_complete_rollout = auto_complete_rollout
        if max_surge_percent is not None:
            self.max_surge_percent = max_surge_percent

    @property
    def name(self):
        """Gets the name of this ApplyServiceModel.  # noqa: E501

        Name of the Service  # noqa: E501

        :return: The name of this ApplyServiceModel.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ApplyServiceModel.

        Name of the Service  # noqa: E501

        :param name: The name of this ApplyServiceModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and name is None:  # noqa: E501
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def description(self):
        """Gets the description of this ApplyServiceModel.  # noqa: E501

        Description of the Service  # noqa: E501

        :return: The description of this ApplyServiceModel.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this ApplyServiceModel.

        Description of the Service  # noqa: E501

        :param description: The description of this ApplyServiceModel.  # noqa: E501
        :type: str
        """

        self._description = description

    @property
    def project_id(self):
        """Gets the project_id of this ApplyServiceModel.  # noqa: E501

        Id of the project this Service will start clusters in  # noqa: E501

        :return: The project_id of this ApplyServiceModel.  # noqa: E501
        :rtype: str
        """
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        """Sets the project_id of this ApplyServiceModel.

        Id of the project this Service will start clusters in  # noqa: E501

        :param project_id: The project_id of this ApplyServiceModel.  # noqa: E501
        :type: str
        """

        self._project_id = project_id

    @property
    def version(self):
        """Gets the version of this ApplyServiceModel.  # noqa: E501

        A version string that represents the version for this service. Will be populated with the hash of the config if not specified.  # noqa: E501

        :return: The version of this ApplyServiceModel.  # noqa: E501
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this ApplyServiceModel.

        A version string that represents the version for this service. Will be populated with the hash of the config if not specified.  # noqa: E501

        :param version: The version of this ApplyServiceModel.  # noqa: E501
        :type: str
        """

        self._version = version

    @property
    def canary_percent(self):
        """Gets the canary_percent of this ApplyServiceModel.  # noqa: E501

        A manual target percent for this service. If this field is not set, the service will automatically roll out. If set, this should be a number between 0 and 100. The newly created version will have weight `canary_percent` and the existing version will have `100 - canary_percent`.  # noqa: E501

        :return: The canary_percent of this ApplyServiceModel.  # noqa: E501
        :rtype: int
        """
        return self._canary_percent

    @canary_percent.setter
    def canary_percent(self, canary_percent):
        """Sets the canary_percent of this ApplyServiceModel.

        A manual target percent for this service. If this field is not set, the service will automatically roll out. If set, this should be a number between 0 and 100. The newly created version will have weight `canary_percent` and the existing version will have `100 - canary_percent`.  # noqa: E501

        :param canary_percent: The canary_percent of this ApplyServiceModel.  # noqa: E501
        :type: int
        """

        self._canary_percent = canary_percent

    @property
    def ray_serve_config(self):
        """Gets the ray_serve_config of this ApplyServiceModel.  # noqa: E501

        The Ray Serve config to use for this service. This config defines your Ray Serve application, and will be passed directly to Ray Serve. You can learn more about Ray Serve config files here: https://docs.ray.io/en/latest/serve/production-guide/config.html  # noqa: E501

        :return: The ray_serve_config of this ApplyServiceModel.  # noqa: E501
        :rtype: object
        """
        return self._ray_serve_config

    @ray_serve_config.setter
    def ray_serve_config(self, ray_serve_config):
        """Sets the ray_serve_config of this ApplyServiceModel.

        The Ray Serve config to use for this service. This config defines your Ray Serve application, and will be passed directly to Ray Serve. You can learn more about Ray Serve config files here: https://docs.ray.io/en/latest/serve/production-guide/config.html  # noqa: E501

        :param ray_serve_config: The ray_serve_config of this ApplyServiceModel.  # noqa: E501
        :type: object
        """
        if self.local_vars_configuration.client_side_validation and ray_serve_config is None:  # noqa: E501
            raise ValueError("Invalid value for `ray_serve_config`, must not be `None`")  # noqa: E501

        self._ray_serve_config = ray_serve_config

    @property
    def build_id(self):
        """Gets the build_id of this ApplyServiceModel.  # noqa: E501

        The id of the cluster env build. This id will determine the docker image your Service is run using.  # noqa: E501

        :return: The build_id of this ApplyServiceModel.  # noqa: E501
        :rtype: str
        """
        return self._build_id

    @build_id.setter
    def build_id(self, build_id):
        """Sets the build_id of this ApplyServiceModel.

        The id of the cluster env build. This id will determine the docker image your Service is run using.  # noqa: E501

        :param build_id: The build_id of this ApplyServiceModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and build_id is None:  # noqa: E501
            raise ValueError("Invalid value for `build_id`, must not be `None`")  # noqa: E501

        self._build_id = build_id

    @property
    def compute_config_id(self):
        """Gets the compute_config_id of this ApplyServiceModel.  # noqa: E501

        The id of the compute configuration that you want to use. This id will specify the resources required for your ServiceThe compute template includes a `cloud_id` that must be fixed for each service.  # noqa: E501

        :return: The compute_config_id of this ApplyServiceModel.  # noqa: E501
        :rtype: str
        """
        return self._compute_config_id

    @compute_config_id.setter
    def compute_config_id(self, compute_config_id):
        """Sets the compute_config_id of this ApplyServiceModel.

        The id of the compute configuration that you want to use. This id will specify the resources required for your ServiceThe compute template includes a `cloud_id` that must be fixed for each service.  # noqa: E501

        :param compute_config_id: The compute_config_id of this ApplyServiceModel.  # noqa: E501
        :type: str
        """
        if self.local_vars_configuration.client_side_validation and compute_config_id is None:  # noqa: E501
            raise ValueError("Invalid value for `compute_config_id`, must not be `None`")  # noqa: E501

        self._compute_config_id = compute_config_id

    @property
    def config(self):
        """Gets the config of this ApplyServiceModel.  # noqa: E501

        Target Service's configuration  # noqa: E501

        :return: The config of this ApplyServiceModel.  # noqa: E501
        :rtype: ServiceConfig
        """
        return self._config

    @config.setter
    def config(self, config):
        """Sets the config of this ApplyServiceModel.

        Target Service's configuration  # noqa: E501

        :param config: The config of this ApplyServiceModel.  # noqa: E501
        :type: ServiceConfig
        """

        self._config = config

    @property
    def rollout_strategy(self):
        """Gets the rollout_strategy of this ApplyServiceModel.  # noqa: E501

        Strategy for rollout. The ROLLOUT strategy will deploy your Ray Serve configuration onto a newly started cluster, and then shift traffic over to the new cluster. You can manually control the speed of the rollout using the canary_percent configuration. The IN_PLACE strategy will use Ray Serve in place upgrade to update your existing cluster in place. When using this rollout strategy, you may only change the ray_serve_config field. You cannot partially shift traffic or rollback an in place upgrade. In place upgrades are faster and riskier than rollouts, and we recommend only using them for relatively safe changes (for example, increasing the number of replicas on a Ray Serve deployment). Default strategy is ROLLOUT.  # noqa: E501

        :return: The rollout_strategy of this ApplyServiceModel.  # noqa: E501
        :rtype: RolloutStrategy
        """
        return self._rollout_strategy

    @rollout_strategy.setter
    def rollout_strategy(self, rollout_strategy):
        """Sets the rollout_strategy of this ApplyServiceModel.

        Strategy for rollout. The ROLLOUT strategy will deploy your Ray Serve configuration onto a newly started cluster, and then shift traffic over to the new cluster. You can manually control the speed of the rollout using the canary_percent configuration. The IN_PLACE strategy will use Ray Serve in place upgrade to update your existing cluster in place. When using this rollout strategy, you may only change the ray_serve_config field. You cannot partially shift traffic or rollback an in place upgrade. In place upgrades are faster and riskier than rollouts, and we recommend only using them for relatively safe changes (for example, increasing the number of replicas on a Ray Serve deployment). Default strategy is ROLLOUT.  # noqa: E501

        :param rollout_strategy: The rollout_strategy of this ApplyServiceModel.  # noqa: E501
        :type: RolloutStrategy
        """

        self._rollout_strategy = rollout_strategy

    @property
    def ray_gcs_external_storage_config(self):
        """Gets the ray_gcs_external_storage_config of this ApplyServiceModel.  # noqa: E501

        Config for the Ray GCS to connect to external storage. If populated, head node fault tolerance will be enabled for this service.  # noqa: E501

        :return: The ray_gcs_external_storage_config of this ApplyServiceModel.  # noqa: E501
        :rtype: RayGCSExternalStorageConfig
        """
        return self._ray_gcs_external_storage_config

    @ray_gcs_external_storage_config.setter
    def ray_gcs_external_storage_config(self, ray_gcs_external_storage_config):
        """Sets the ray_gcs_external_storage_config of this ApplyServiceModel.

        Config for the Ray GCS to connect to external storage. If populated, head node fault tolerance will be enabled for this service.  # noqa: E501

        :param ray_gcs_external_storage_config: The ray_gcs_external_storage_config of this ApplyServiceModel.  # noqa: E501
        :type: RayGCSExternalStorageConfig
        """

        self._ray_gcs_external_storage_config = ray_gcs_external_storage_config

    @property
    def tracing_config(self):
        """Gets the tracing_config of this ApplyServiceModel.  # noqa: E501

        Config for initializing tracing within Anyscale runtime.  # noqa: E501

        :return: The tracing_config of this ApplyServiceModel.  # noqa: E501
        :rtype: TracingConfig
        """
        return self._tracing_config

    @tracing_config.setter
    def tracing_config(self, tracing_config):
        """Sets the tracing_config of this ApplyServiceModel.

        Config for initializing tracing within Anyscale runtime.  # noqa: E501

        :param tracing_config: The tracing_config of this ApplyServiceModel.  # noqa: E501
        :type: TracingConfig
        """

        self._tracing_config = tracing_config

    @property
    def auto_complete_rollout(self):
        """Gets the auto_complete_rollout of this ApplyServiceModel.  # noqa: E501

        Flag to indicate whether or not to complete the rollout after the canary version reaches 100%.  # noqa: E501

        :return: The auto_complete_rollout of this ApplyServiceModel.  # noqa: E501
        :rtype: bool
        """
        return self._auto_complete_rollout

    @auto_complete_rollout.setter
    def auto_complete_rollout(self, auto_complete_rollout):
        """Sets the auto_complete_rollout of this ApplyServiceModel.

        Flag to indicate whether or not to complete the rollout after the canary version reaches 100%.  # noqa: E501

        :param auto_complete_rollout: The auto_complete_rollout of this ApplyServiceModel.  # noqa: E501
        :type: bool
        """

        self._auto_complete_rollout = auto_complete_rollout

    @property
    def max_surge_percent(self):
        """Gets the max_surge_percent of this ApplyServiceModel.  # noqa: E501

        Max amount of excess capacity allocated during the rollout (0-100).  # noqa: E501

        :return: The max_surge_percent of this ApplyServiceModel.  # noqa: E501
        :rtype: int
        """
        return self._max_surge_percent

    @max_surge_percent.setter
    def max_surge_percent(self, max_surge_percent):
        """Sets the max_surge_percent of this ApplyServiceModel.

        Max amount of excess capacity allocated during the rollout (0-100).  # noqa: E501

        :param max_surge_percent: The max_surge_percent of this ApplyServiceModel.  # noqa: E501
        :type: int
        """

        self._max_surge_percent = max_surge_percent

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
        if not isinstance(other, ApplyServiceModel):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ApplyServiceModel):
            return True

        return self.to_dict() != other.to_dict()
