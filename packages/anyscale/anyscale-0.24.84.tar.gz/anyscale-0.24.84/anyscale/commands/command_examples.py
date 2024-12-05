JOB_SUBMIT_EXAMPLE = """\
$ anyscale job submit --name my-job --wait -- python main.py
Output
(anyscale +1.0s) Submitting job with config JobConfig(name='my-job', image_uri=None, compute_config=None, env_vars=None, py_modules=None, cloud=None, project=None, ray_version=None, job_queue_config=None).
(anyscale +1.7s) Uploading local dir '.' to cloud storage.
(anyscale +2.6s) Including workspace-managed pip dependencies.
(anyscale +3.2s) Job 'my-job' submitted, ID: 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe'.
(anyscale +3.2s) View the job in the UI: https://console.anyscale.com/jobs/prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe
(anyscale +3.2s) Waiting for the job to run. Interrupting this command will not cancel the job.
(anyscale +3.5s) Waiting for job 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe' to reach target state SUCCEEDED, currently in state: STARTING
(anyscale +1m19.7s) Job 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe' transitioned from STARTING to SUCCEEDED
(anyscale +1m19.7s) Job 'prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe' reached target state, exiting
"""

JOB_STATUS_EXAMPLE = """\
$ anyscale job status -n my-job
id: prodjob_6ntzknwk1i9b1uw1zk1gp9dbhe
name: my-job
state: STARTING
runs:
- name: raysubmit_ynxBVGT1SmzndiXL
  state: SUCCEEDED
"""

JOB_TERMINATE_EXAMPLE = """\
$ anyscale job terminate -n my-job
(anyscale +5.4s) Marked job 'my-job' for termination
(anyscale +5.4s) Query the status of the job with `anyscale job status --name my-job`.
"""

JOB_ARCHIVE_EXAMPLE = """\
$ anyscale job archive -n my-job
(anyscale +8.5s) Job prodjob_vzq2pvkzyz3c1jw55kl76h4dk1 is successfully archived.
"""

JOB_LOGS_EXAMPLE = """\
$ anyscale job logs -n my-job
2024-08-23 20:31:10,913 INFO job_manager.py:531 -- Runtime env is setting up.
hello world
"""

JOB_WAIT_EXAMPLE = """\
$ anyscale job wait -n my-job
(anyscale +5.7s) Waiting for job 'my-job' to reach target state SUCCEEDED, currently in state: STARTING
(anyscale +1m34.2s) Job 'my-job' transitioned from STARTING to SUCCEEDED
(anyscale +1m34.2s) Job 'my-job' reached target state, exiting
"""

JOB_LIST_EXAMPLE = """\
$ anyscale job list -n my-job
Output
View your Jobs in the UI at https://console.anyscale.com/jobs
JOBS:
NAME    ID                                    COST  PROJECT NAME    CLUSTER NAME                                    CURRENT STATE           CREATOR           ENTRYPOINT
my-job  prodjob_s9x4uzc5jnkt5z53g4tujb3y2e       0  default         cluster_for_prodjob_s9x4uzc5jnkt5z53g4tujb3y2e  SUCCESS                 doc@anyscale.com  python main.py
"""

SCHEDULE_APPLY_EXAMPLE = """\
$ anyscale schedule apply -n my-schedule -f my-schedule.yaml
(anyscale +0.5s) Applying schedule with config ScheduleConfig(job_config=JobConfig(name='my-schedule', image_uri=None, compute_config=None, env_vars=None, py_modules=None, cloud=None, project=None, ray_version=None, job_queue_config=None), cron_expression='0 0 * * * *', timezone='UTC').
(anyscale +2.3s) Uploading local dir '.' to cloud storage.
(anyscale +3.7s) Including workspace-managed pip dependencies.
(anyscale +4.9s) Schedule 'my-schedule' submitted, ID: 'cronjob_vrjrbwcnfjjid7fsld3sfkn8jz'.

$ cat my-schedule.yaml
timezone: local
cron_expression: 0 0 * * * *
job_config:
    name: my-job
    entrypoint: python main.py
    max_retries: 5
"""

SCHEDULE_LIST_EXAMPLE = """\
$ anyscale schedule list -n my-schedule
Output
+------------------------------------+-------------+---------------+-----------+-------------+------------------+------------+------------------+-----------------------+
| ID                                 | NAME        | DESCRIPTION   | PROJECT   | CRON        | NEXT TRIGGER     | TIMEZONE   | CREATOR          | LATEST EXECUTION ID   |
|------------------------------------+-------------+---------------+-----------+-------------+------------------+------------+------------------+-----------------------|
| cronjob_vrjrbwcnfjjid7fsld3sfkn8jz | my-schedule |               | default   | 0 0 * * * * | 2 hours from now | UTC        | doc@anyscale.com |                       |
+------------------------------------+-------------+---------------+-----------+-------------+------------------+------------+------------------+-----------------------+
"""

SCHEDULE_PAUSE_EXAMPLE = """\
$ anyscale schedule pause -n my-schedule
(anyscale +3.6s) Set schedule 'my-schedule' to state DISABLED
"""

SCHEDULE_RESUME_EXAMPLE = """\
$ anyscale schedule resume -n my-schedule
(anyscale +4.1s) Set schedule 'my-schedule' to state ENABLED
"""

SCHEDULE_STATUS_EXAMPLE = """\
$ anyscale schedule status -n my-schedule
id: cronjob_vrjrbwcnfjjid7fsld3sfkn8jz
name: my-schedule
state: ENABLED
"""

SCHEDULE_RUN_EXAMPLE = """\
$ anyscale schedule run -n my-schedule
(anyscale +2.5s) Triggered job for schedule 'my-schedule'.
"""

SCHEDULE_URL_EXAMPLE = """\
$ anyscale schedule url -n my-schedule
Output
(anyscale +2.3s) View your schedule at https://console.anyscale.com/scheduled-jobs/cronjob_7zj
"""

WORKSPACE_CREATE_EXAMPLE = """\
$ anyscale workspace_v2 create -f config.yml
(anyscale +2.7s) Workspace created successfully id: expwrk_jstjkv15a1vmle2j1t59s4bm35
(anyscale +3.9s) Applied dynamic requirements to workspace id: my-workspace
(anyscale +4.8s) Applied environment variables to workspace id: my-workspace

$ cat config.yml
name: my-workspace
idle_termination_minutes: 10
env_vars:
    HUMPDAY: WEDS
requirements: requirements.txt
"""

WORKSPACE_START_EXAMPLE = """\
$ anyscale workspace_v2 start --name my-workspace
(anyscale +5.8s) Starting workspace 'my-workspace'
"""

WORKSPACE_TERMINATE_EXAMPLE = """\
$ anyscale workspace_v2 terminate --name my-workspace
(anyscale +2.5s) Terminating workspace 'my-workspace'
"""

WORKSPACE_STATUS_EXAMPLE = """\
$ anyscale workspace_v2 status --name my-workspace
(anyscale +2.3s) STARTING
"""

WORKSPACE_WAIT_EXAMPLE = """\
$ anyscale workspace_v2 wait --name my-workspace --state RUNNING
(anyscale +2.5s) Waiting for workspace 'expwrk_jstjkv15a1vmle2j1t59s4bm35' to reach target state RUNNING, currently in state: RUNNING
(anyscale +2.8s) Workspace 'expwrk_jstjkv15a1vmle2j1t59s4bm35' reached target state, exiting
"""

WORKSPACE_SSH_EXAMPLE = """\
$ anyscale workspace_v2 ssh --name my-workspace
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
(base) ray@ip-10-0-24-60:~/default$
"""

WORKSPACE_RUN_COMMAND_EXAMPLE = """\
$ anyscale workspace_v2 run_command --name my-workspace "echo hello world"
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
hello world
"""

WORKSPACE_PULL_EXAMPLE = """\
$ anyscale workspace_v2 pull --name my-workspace --local-dir my-local
Warning: Permanently added '54.212.209.253' (ED25519) to the list of known hosts.
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
receiving incremental file list
created directory my-local
./
my-local/
my-local/main.py

sent 118 bytes  received 141 bytes  172.67 bytes/sec
total size is 0  speedup is 0.00
"""

WORKSPACE_PUSH_EXAMPLE = """\
$ anyscale workspace_v2 push --name my-workspace --local-dir my-local
Warning: Permanently added '52.10.22.124' (ED25519) to the list of known hosts.
Authorized uses only. All activity may be monitored and reported.
Warning: Permanently added '[0.0.0.0]:5020' (ED25519) to the list of known hosts.
sending incremental file list
my-local/
my-local/main.py

sent 188 bytes  received 39 bytes  151.33 bytes/sec
total size is 0  speedup is 0.00
"""

MACHINE_POOL_CREATE_EXAMPLE = """\
$ anyscale machine-pool create --name can-testing
Machine pool can-testing has been created successfully (ID mp_8ogdz85mdwxb8a92yo44nn84ox).
"""

MACHINE_POOL_DELETE_EXAMPLE = """\
$ anyscale machine-pool delete --name can-testing
Deleted machine pool 'can-testing'.
"""

MACHINE_POOL_LIST_EXAMPLE = """\
$ anyscale machine-pool list
MACHINE POOL       ID                             Clouds
can-testing        mp_8ogdz85mdwxb8a92yo44nn84ox
"""

LLM_MODELS_GET_EXAMPLE = """
$ anyscale llm model get --model-id my-model-id
Output
{
    'id': 'my-model-id',
    'base_model_id': 'meta-llama/Meta-Llama-3-8B',
    'storage_uri': 'gs://my_bucket/my_folder',
    'ft_type': 'LORA',
    'cloud_id': 'cld_tffbxe9ia5phqr1unxhz4f7e1e',
    'project_id': 'prj_dqb6ha67zubz3gdlvn2tmmglb8',
    'created_at': 1725563985,
    'creator': 'test@anyscale.com',
    'job_id': 'N/A',
    'workspace_id': 'expwrk_yje3t8twim18iuta9r45gwcgcn',
    'generation_config': {
        'prompt_format': {
            'system': '<|start_header_id|>system<|end_header_id|>\\n\\n{instruction}<|eot_id|>',
            'assistant': '<|start_header_id|>assistant<|end_header_id|>\\n\\n{instruction}<|eot_id|>',
            'trailing_assistant': '<|start_header_id|>assistant<|end_header_id|>\\n\\n',
            'user': '<|start_header_id|>user<|end_header_id|>\\n\\n{instruction}<|eot_id|>',
            'bos': '<|begin_of_text|>',
            'default_system_message': '',
            'add_system_tags_even_if_message_is_empty': False,
            'system_in_user': False,
            'system_in_last_user': False,
            'strip_whitespace': True
        },
        'stopping_sequences': None
    }
}
"""

LLM_MODELS_LIST_EXAMPLE = """
$ anyscale llm model list --cloud-id cld_1j41ls4gwkga4pwp8nbql6f239 --project_id prj_i4wy1t442cbe2sthxp61dmtkbh --max-items 2
Output
[
    {
        'id': 'meta-llama/Meta-Llama-3-8B-Instruct:test:bnkve',
        'base_model_id': 'meta-llama/Meta-Llama-3-8B-Instruct',
        'storage_uri': 's3://anyscale-production-data-cld-1j41ls4gwkga4pwp...',
        'ft_type': 'LORA',
        'cloud_id': 'cld_1j41ls4gwkga4pwp8nbql6f239',
        'project_id': 'prj_i4wy1t442cbe2sthxp61dmtkbh',
        'created_at': 1725572462,
        'creator': 'test@anyscale.com',
        'job_id': 'N/A',
        'workspace_id': 'expwrk_bqld1y579g3clukr49rsnd7i5m',
        'generation_config': '{"prompt_format": {"system": "<|start_header_id|>s...'
    },
    {
        'id': 'neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8:test:czcal',
        'base_model_id': 'neuralmagic/Meta-Llama-3.1-8B-Instruct-FP8',
        'storage_uri': 'gs://storage-bucket-cld-tffbxe9ia5phqr1unxhz4f7e1e...',
        'ft_type': 'LORA',
        'cloud_id': 'cld_1j41ls4gwkga4pwp8nbql6f239',
        'project_id': 'prj_i4wy1t442cbe2sthxp61dmtkbh',
        'created_at': 1725563985,
        'creator': 'test@anyscale.com',
        'job_id': 'N/A',
        'workspace_id': 'expwrk_yje3t8twim18iuta9r45gwcgcn',
        'generation_config': '{"prompt_format": {"system": "<|start_header_id|>s...'
    }
]
"""

LLM_MODELS_DELETE_EXAMPLE = """
$ anyscale llm model delete --model-id my-model-id
Output
{'id': 'my-model-id', 'deleted_at': 1725572462}
"""

LLM_DATASET_GET_EXAMPLE = """
$ anyscale llm dataset get john_doe/viggo/train.jsonl
Dataset(
    id='dataset_123',
    name='john_doe/viggo/train.jsonl',
    filename='train.jsonl',
    storage_uri='s3://anyscale-test-data-cld-123/org_123/cld_123/datasets/dataset_123/3/john_doe/viggo/train.jsonl',
    version=3,
    num_versions=3,
    created_at=datetime.datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
    creator_id='usr_123',
    project_id='prj_123',
    cloud_id='cld_123',
    description=None
)
"""

LLM_DATASET_UPLOAD_EXAMPLE = """
$ anyscale llm dataset upload path/to/my_dataset.jsonl -n my_first_dataset

0:00:00 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.1 MB / 5.1 MB Uploading '/path/to/my_dataset.jsonl'

Upload complete!

Dataset(
    id='dataset_123',
    name='my_first_dataset',
    filename='my_dataset.jsonl',
    storage_uri='s3://anyscale-test-data-cld-123/org_123/cld_123/datasets/dataset_123/1/my_dataset.jsonl',
    version=1,
    num_versions=1,
    created_at=datetime.datetime(2024, 1, 1, 0, 0, tzinfo=tzutc()),
    creator_id='usr_123',
    project_id='prj_123',
    cloud_id='cld_123',
    description=None
)
"""

LLM_DATASET_DOWNLOAD_EXAMPLE = """
$ anyscale llm dataset download train.jsonl
0:00:00 100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 711.0 kB / 711.0 kB Downloading 'train.jsonl'

Download complete!

{"messages":[{"content":"hi","role":"user"},{"content":"Hi! How can I help?","role":"assistant"}]}
...
{"messages":[{"content":"bye","role":"user"},{"content":"Goodbye!","role":"assistant"}]}
"""

LLM_DATASET_LIST_EXAMPLE = """
$ anyscale llm dataset list
ID         Name                   Description                       Created At             Num Versions
---------  ---------------------  --------------------------------  -------------------  --------------
dataset_2  second                 second upload                     1/2/2024 12:00 PM              23
dataset_1  first                  first upload                      1/1/2024 12:00 PM              13
"""

RESOURCE_QUOTAS_CREATE_EXAMPLE = """
$ anyscale resource-quota create -n my-resource-quota --cloud my-cloud --project my-project --user-email someone@myorg.com --num-instances 100 --num-cpus 1000 --num-gpus 50 --num-accelerators A10G 10 --num-accelerators A100-80G 0
(anyscale +2.5s) Name: my-resource-quota
Cloud name: my-cloud
Project name: my-project
User email: someone@myorg.com
Number of CPUs: 1000
Number of instances: 100
Number of GPUs: 50
Number of accelerators: {'A10G': 10, 'A100-80G': 0}
(anyscale +2.5s) Resource quota created successfully ID: rsq_abcdef
"""

RESOURCE_QUOTAS_LIST_EXAMPLE = """
$ anyscale resource-quota list --cloud my-cloud
Resource quotas:
ID       NAME               CLOUD ID    PROJECT ID  USER ID     IS ENABLED    CREATED AT    DELETED AT    QUOTA
rsq_123  resource-quota-1   cld_abcdef  prj_abcdef  usr_abcdef  True          09/11/2024                  {'num_accelerators': {'A100-80G': 0, 'A10G': 10},
                                                                                                           'num_cpus': 1000,
                                                                                                           'num_gpus': 50,
                                                                                                           'num_instances': 100}
rsq_456  resource-quota-2   cld_abcdef              usr_abcdef  True          09/10/2024                  {'num_accelerators': {}, 'num_cpus': None, 'num_gpus': None, 'num_instances': 2}
rsq_789  resource-quota-3   cld_abcdef                          False         09/05/2024                  {'num_accelerators': {'A10G': 1},
                                                                                                            'num_cpus': None,
                                                                                                            'num_gpus': None,
                                                                                                            'num_instances': None}
"""

RESOURCE_QUOTAS_ENABLE_EXAMPLE = """
$ anyscale resource-quota enable --id rsq_abcdef
(anyscale +1.2s) Enabled resource quota with ID rsq_abcdef successfully.
"""

RESOURCE_QUOTAS_DISABLE_EXAMPLE = """
$ anyscale resource-quota disable --id rsq_abcdef
(anyscale +1.4s) Disabled resource quota with ID rsq_abcdef successfully.
"""

RESOURCE_QUOTAS_DELETE_EXAMPLE = """
$ anyscale resource-quota delete --id rsq_abcdef
(anyscale +1.0s) Resource quota with ID rsq_abcdef deleted successfully.
"""

COMPUTE_CONFIG_CREATE_EXAMPLE = """
$ anyscale compute-config create -n my-compute-config -f compute_config.yaml
(anyscale +3.7s) Created compute config: 'my-compute-config:1'
(anyscale +3.7s) View the compute config in the UI: 'https://console.anyscale.com/v2/...'

$cat compute_config.yaml
head_node:
  instance_type: m5.8xlarge
worker_nodes:
- instance_type: m5.8xlarge
  min_nodes: 5
  max_nodes: 5
  market_type: ON_DEMAND # (Optional) Defaults to ON_DEMAND
- instance_type: g4dn.xlarge
  min_nodes: 1
  max_nodes: 10
  market_type: PREFER_SPOT # (Optional) Defaults to ON_DEMAND
min_resources: # (Optional) Defaults to no minimum.
  CPU: 1
  GPU: 1
max_resources: # (Optional) Defaults to no maximum.
  CPU: 6
  GPU: 1
"""

COMPUTE_CONFIG_GET_EXAMPLE = """
$ anyscale compute-config get -n my-compute-config
name: my-compute-config:1
id: cpt_buthu4glxj3azv4e287jad3ya3
config:
  cloud: aviary-prod-us-east-1
  head_node:
    instance_type: m5.8xlarge
    resources:
      CPU: 0
      GPU: 0
  worker_nodes:
  - instance_type: m5.8xlarge
    name: m5.8xlarge
    min_nodes: 5
    max_nodes: 5
    market_type: ON_DEMAND
  - instance_type: g4dn.xlarge
    name: g4dn.xlarge
    min_nodes: 1
    max_nodes: 10
    market_type: PREFER_SPOT
  min_resources:
    CPU: 1
    GPU: 1
  max_resources:
    CPU: 6
    GPU: 1
  enable_cross_zone_scaling: false
  flags: {}
"""

COMPUTE_CONFIG_ARCHIVE_EXAMPLE = """
$ anyscale compute-config archive -n my-compute-config
(anyscale +2.3s) Compute config is successfully archived.
"""

IMAGE_BUILD_EXAMPLE = """
$ anyscale image build -f my.Dockerfile -n my-image --ray-version 2.21.0
(anyscale +2.8s) Building image. View it in the UI: https://console.anyscale.com/v2/...
(anyscale +1m53.0s) Waiting for image build to complete. Elapsed time: 102 seconds.
(anyscale +1m53.0s) Image build succeeded.
Image built successfully with URI: anyscale/image/my-image:1

$ cat my.Dockerfile
FROM anyscale/ray:2.21.0-py39
RUN pip install --no-cache-dir pandas
"""

IMAGE_GET_EXAMPLE = """
$ anyscale image get -n my-image
uri: anyscale/image/my-image:1
status: SUCCEEDED
ray_version: 2.21.0
"""

IMAGE_REGISTER_EXAMPLE = """
$ anyscale image register --image-uri docker.io/myrepo/image:v2 --name mycoolimage --ray-version 2.30.0
Image registered successfully with URI: anyscale/image/mycoolimage:1
"""
