import os
from subprocess import list2cmdline
from typing import Generator, List, Optional, Union
from unittest.mock import Mock, patch
import uuid

import click
from click.testing import CliRunner
import pytest

from anyscale._private.models.image_uri import ANYSCALE_CLUSTER_ENV_PREFIX
from anyscale._private.sdk import _LAZY_SDK_SINGLETONS
from anyscale.commands.job_commands import logs, status, submit, wait
from anyscale.job.commands import _JOB_SDK_SINGLETON_KEY
from anyscale.job.models import (
    JobConfig,
    JobLogMode,
    JobRunState,
    JobRunStatus,
    JobState,
    JobStatus,
)


def _get_test_file_path(subpath: str) -> str:
    return os.path.join(os.path.dirname(__file__), "test_files/", subpath)


EMPTY_CONFIG_PATH = _get_test_file_path("job_config_files/empty.yaml")
MINIMAL_CONFIG_PATH = _get_test_file_path("job_config_files/minimal.yaml")
NON_YAML_CONFIG_PATH = _get_test_file_path("job_config_files/minimal_job_config")
NONEXISTENT_CONFIG_PATH = _get_test_file_path("job_config_files/nonexistent.yaml")
FULL_CONFIG_PATH = _get_test_file_path("job_config_files/full.yaml")
POINTS_TO_REQUIREMENTS_FILE_PATH = _get_test_file_path(
    "job_config_files/points_to_requirements_file.yaml"
)
UNRECOGNIZED_OPTION_CONFIG_PATH = _get_test_file_path(
    "job_config_files/unrecognized_option.yaml"
)

COMMENTS_REQ_PATH = _get_test_file_path("requirements_files/comments.txt")
EMPTY_REQ_PATH = _get_test_file_path("requirements_files/empty.txt")
MULIT_LINE_WITH_WHITESPACE__REQ_PATH = _get_test_file_path(
    "requirements_files/multi_line_with_whitespace.txt"
)
MULTI_LINE_REQ_PATH = _get_test_file_path("requirements_files/multi_line.txt")
SINGLE_LINE_REQ_PATH = _get_test_file_path("requirements_files/single_line.txt")
WORKSPACE_REQUIREMENTS_REQ_PATH = _get_test_file_path(
    "requirements_files/test_workspace_requirements.txt"
)

SINGLE_EXCLUDE_LIST = ["torch"]
MULTIPLE_EXCLUDE_LIST = ["numpy", "pandas", "scipy"]

DEFAULT_JOB_ID = "default-fake-job-id"


class FakeJobSDK:
    DEFAULT_JOB_NAME = "default-fake-job-name"
    DEFAULT_JOB_CONFIG = JobConfig(entrypoint="python hello.py")

    def __init__(self):
        self.submitted_config: Optional[JobConfig] = None
        self.submitted_id: Optional[str] = None
        self.submitted_name: Optional[str] = None
        self.fetched_name: Optional[str] = None
        self.waited_id: Optional[str] = None
        self.waited_name: Optional[str] = None
        self.waited_state: Optional[Union[str, JobState]] = None
        self.waited_timeout_s: Optional[float] = None
        self._job_runs: List[JobRunStatus] = []

        self.get_logs_id: Optional[str] = None
        self.get_logs_name: Optional[str] = None
        self.get_logs_run: Optional[str] = None
        self.get_logs_mode: Union[str, JobLogMode] = None
        self.get_logs_max_lines: Optional[int] = None

    def submit(self, config: JobConfig):
        assert isinstance(config, JobConfig)
        self.submitted_config = config
        self.submitted_id = str(uuid.uuid4())
        self.submitted_name = (
            self.submitted_config.name
            if self.submitted_config.name is not None
            else self.DEFAULT_JOB_NAME
        )
        return self.submitted_id

    def wait(
        self,
        *,
        name: Optional[str] = None,
        job_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        state: Union[str, JobState] = JobState.SUCCEEDED,
        timeout_s: int = 1800,
    ) -> str:
        self.waited_id = job_id or str(uuid.uuid4())
        self.waited_name = name
        self.waited_state = state
        self.waited_timeout_s = timeout_s
        return self.waited_id

    def status(
        self,
        *,
        name: Optional[str] = None,
        job_id: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ):
        self.fetched_name = name
        if (
            self.submitted_config is not None
            and self.submitted_name is not None
            and (name == self.submitted_name or job_id == self.submitted_id)
        ):
            return JobStatus(
                id=self.submitted_id if self.submitted_id else "",
                name=self.submitted_name,
                state=JobState.SUCCEEDED,
                config=self.submitted_config,
                runs=self._job_runs,
            )
        raise RuntimeError("Job was not found.")

    def get_logs(
        self,
        *,
        job_id: Optional[str] = None,
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        run: Optional[str] = None,
        mode: Union[str, JobLogMode] = JobLogMode.TAIL,
        max_lines: Optional[int] = None,
    ) -> str:
        self.get_logs_id = job_id or str(uuid.uuid4())
        self.get_logs_name = name
        self.get_logs_run = run
        self.get_logs_mode = mode
        self.get_logs_max_lines = max_lines
        return ""


@pytest.fixture()
def mock_job_controller() -> Generator[Mock, None, None]:
    mock_job_controller = Mock(submit=Mock(return_value=DEFAULT_JOB_ID))
    mock_job_controller_cls = Mock(return_value=mock_job_controller)
    with patch(
        "anyscale.commands.job_commands.JobController", new=mock_job_controller_cls,
    ):
        yield mock_job_controller


@pytest.fixture()
def fake_job_sdk() -> Generator[FakeJobSDK, None, None]:
    fake_job_sdk = FakeJobSDK()
    _LAZY_SDK_SINGLETONS[_JOB_SDK_SINGLETON_KEY] = fake_job_sdk
    try:
        yield fake_job_sdk
    finally:
        del _LAZY_SDK_SINGLETONS[_JOB_SDK_SINGLETON_KEY]


def _assert_error_message(result: click.testing.Result, *, message: str):
    assert result.exit_code != 0
    assert message in result.stdout


class TestSubmit:
    def test_missing_arg(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        result = runner.invoke(submit)
        _assert_error_message(
            result,
            message="Either a config file or an inlined entrypoint must be provided.",
        )

    def test_config_file_not_found(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        result = runner.invoke(submit, ["missing_config.yaml"])
        _assert_error_message(
            result, message="Job config file 'missing_config.yaml' not found.",
        )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_basic(self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool):
        runner = CliRunner()
        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, [*entrypoint_args])
        assert result.exit_code == 0, result.stdout

        if inlined_entrypoint:
            # Passing an inlined entrypoint should go through the new path.
            assert fake_job_sdk.submitted_config == JobConfig(
                entrypoint="python main.py"
            )
            mock_job_controller.submit.assert_not_called()
        else:
            # For now, passing a config file should go through the old path.
            assert fake_job_sdk.submitted_config is None
            mock_job_controller.submit.assert_called_once_with(
                MINIMAL_CONFIG_PATH, name=None
            )

    @pytest.mark.parametrize(
        "config_file_arg",
        [MINIMAL_CONFIG_PATH, NON_YAML_CONFIG_PATH, NONEXISTENT_CONFIG_PATH,],
    )
    def test_inlined_config_file(
        self, fake_job_sdk, mock_job_controller, config_file_arg
    ):
        runner = CliRunner()
        result = runner.invoke(submit, [config_file_arg])

        if config_file_arg == NONEXISTENT_CONFIG_PATH:
            assert result.exit_code == 1
            error_msg = f"Job config file '{config_file_arg}' not found"
            assert error_msg in result.stdout
        else:
            assert result.exit_code == 0, result.stdout

            mock_job_controller.submit.assert_called_once_with(
                config_file_arg, name=None
            )
        assert fake_job_sdk.submitted_config is None

    @pytest.mark.parametrize(
        "config_file",
        [
            EMPTY_CONFIG_PATH,
            MINIMAL_CONFIG_PATH,
            FULL_CONFIG_PATH,
            POINTS_TO_REQUIREMENTS_FILE_PATH,
            UNRECOGNIZED_OPTION_CONFIG_PATH,
        ],
    )
    @pytest.mark.parametrize(
        "override",
        [
            [],
            ["--name", "test-name"],
            ["--image-uri", "user_name/repository"],
            [
                "--registry-login-secret",
                "secret-name",
                "--image-uri",
                "user_name/repository",
            ],
            ["--containerfile", "somefile"],
            ["--working-dir", "."],
            ["--", "python", "main.py"],
        ],
    )
    def test_config_file(
        self, fake_job_sdk, mock_job_controller, config_file: str, override: List[str],
    ):
        runner = CliRunner()
        command = ["--config-file", config_file, *override]
        result = runner.invoke(submit, command)

        if config_file == UNRECOGNIZED_OPTION_CONFIG_PATH:
            assert result.exit_code != 0
            return

        if config_file == EMPTY_CONFIG_PATH and "--" not in override:
            # When the config file doesn't have the entrypoint,
            # entrypoint must be provided as a CLI argument.
            assert result.exit_code != 0
            return

        assert result.exit_code == 0, result.stdout

        if config_file == EMPTY_CONFIG_PATH:
            assert override[0] == "--"
            expected = JobConfig(entrypoint=list2cmdline(override[1:]))
        else:
            expected = JobConfig.from_yaml(config_file)

        if override:
            if override[0] == "--name":
                expected = expected.options(name=override[1])
            elif override[0] == "--image-uri":
                expected = expected.options(image_uri=override[1])
            elif override[0] == "--registry-login-secret":
                expected = expected.options(registry_login_secret=override[1])
                expected = expected.options(image_uri=override[3])
            elif override[0] == "--containerfile":
                expected = expected.options(containerfile=override[1])
            elif override[0] == "--working-dir":
                expected = expected.options(working_dir=override[1])
            elif override[0] == "--":
                expected = expected.options(entrypoint=list2cmdline(override[1:]))

        assert fake_job_sdk.submitted_config == expected
        mock_job_controller.submit.assert_not_called()

    def test_submit_both_image_uri_and_containerfile(
        self, fake_job_sdk, mock_job_controller
    ):
        runner = CliRunner()
        result = runner.invoke(
            submit,
            [
                "--config-file",
                FULL_CONFIG_PATH,
                "--image-uri",
                "image",
                "--containerfile",
                "file",
            ],
        )
        _assert_error_message(
            result,
            message="Only one of '--containerfile' and '--image-uri' can be provided.",
        )

    def test_submit_registry_login_secret_without_custom_image_uri(
        self, fake_job_sdk, mock_job_controller
    ):
        runner = CliRunner()

        # No image uri provided
        result = runner.invoke(
            submit,
            ["--config-file", FULL_CONFIG_PATH, "--registry-login-secret", "secret",],
        )
        _assert_error_message(
            result,
            message="Registry login secret can only be used with an image that is not hosted on Anyscale.",
        )

        # Anyscale image uri provided
        result = runner.invoke(
            submit,
            [
                "--config-file",
                FULL_CONFIG_PATH,
                "--registry-login-secret",
                "secret",
                "--image-uri",
                f"{ANYSCALE_CLUSTER_ENV_PREFIX}some-image",
            ],
        )
        _assert_error_message(
            result,
            message="Registry login secret can only be used with an image that is not hosted on Anyscale.",
        )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_override_name(
        self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool
    ):
        runner = CliRunner()
        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, ["--name", "test-name", *entrypoint_args])
        assert result.exit_code == 0

        if inlined_entrypoint:
            assert fake_job_sdk.submitted_config == JobConfig(
                entrypoint="python main.py", name="test-name"
            )
            mock_job_controller.submit.assert_not_called()
        else:
            assert fake_job_sdk.submitted_config is None
            mock_job_controller.submit.assert_called_once_with(
                MINIMAL_CONFIG_PATH, name="test-name"
            )

    def test_override_env_vars(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()

        expected_base_job_config = JobConfig(
            name="test-name-from-file",
            entrypoint="python test.py",
            image_uri="docker.io/library/test:latest",
            compute_config="test-compute-config",
            working_dir="test-working-dir",
            env_vars={"ENV_KEY": "ENV_VAL"},
            excludes=["test"],
            requirements=["pip-install-test"],
            max_retries=5,
            timeout_s=60,
        )

        # No overrides.
        result = runner.invoke(submit, ["-f", FULL_CONFIG_PATH])
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config == expected_base_job_config

        # Override existing env var.
        result = runner.invoke(
            submit, ["-f", FULL_CONFIG_PATH, "--env", "ENV_KEY=UPDATED_ENV_VAL"]
        )
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config == expected_base_job_config.options(
            env_vars={"ENV_KEY": "UPDATED_ENV_VAL"},
        )

        # Add new env var (existing shouldn't be touched).
        result = runner.invoke(
            submit, ["-f", FULL_CONFIG_PATH, "--env", "NEW_ENV_KEY=NEW_ENV_VAL"]
        )
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config == expected_base_job_config.options(
            env_vars={"ENV_KEY": "ENV_VAL", "NEW_ENV_KEY": "NEW_ENV_VAL"},
        )

        # Set env var in a config that doesn't have any.
        result = runner.invoke(
            submit, ["-f", MINIMAL_CONFIG_PATH, "--env", "ENV_KEY=ENV_VAL"]
        )
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config == JobConfig(
            entrypoint="python test.py", env_vars={"ENV_KEY": "ENV_VAL"},
        )

        # Set env var in an inlined entrypoint.
        result = runner.invoke(
            submit, ["--env", "ENV_KEY=ENV_VAL", "--", "python", "main.py"]
        )
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config == JobConfig(
            entrypoint="python main.py", env_vars={"ENV_KEY": "ENV_VAL"},
        )

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_no_wait_by_default(
        self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool
    ):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, [*entrypoint_args])
        assert result.exit_code == 0

        assert fake_job_sdk.waited_id is None

    @pytest.mark.parametrize("inlined_entrypoint", [False, True])
    def test_wait(self, fake_job_sdk, mock_job_controller, inlined_entrypoint: bool):
        runner = CliRunner()

        entrypoint_args = (
            ["--", "python", "main.py"] if inlined_entrypoint else [MINIMAL_CONFIG_PATH]
        )
        result = runner.invoke(submit, ["--wait", *entrypoint_args])
        assert result.exit_code == 0
        print(result.stdout)

        if inlined_entrypoint:
            assert (
                fake_job_sdk.waited_id is not None
                and fake_job_sdk.waited_id == fake_job_sdk.submitted_id
            )
        else:
            assert (
                fake_job_sdk.waited_id is not None
                and fake_job_sdk.waited_id == DEFAULT_JOB_ID
            )

    def test_missing_requirements(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        entrypoint_args = ["--", "python", "main.py"]
        missing_req_file = "not-real-req.txt"
        result = runner.invoke(submit, ["-r", missing_req_file, *entrypoint_args])

        assert result.exit_code == 1
        error_msg = f"Requirements file '{missing_req_file}' not found"
        assert error_msg in result.stdout

    @pytest.mark.parametrize(
        "requirement_path",
        [
            COMMENTS_REQ_PATH,
            EMPTY_REQ_PATH,
            MULIT_LINE_WITH_WHITESPACE__REQ_PATH,
            MULTI_LINE_REQ_PATH,
            SINGLE_LINE_REQ_PATH,
            WORKSPACE_REQUIREMENTS_REQ_PATH,
        ],
    )
    def test_requirements(self, fake_job_sdk, mock_job_controller, requirement_path):
        runner = CliRunner()
        entrypoint_args = ["--", "python", "main.py"]
        result = runner.invoke(submit, ["-r", requirement_path, *entrypoint_args])
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config.requirements == requirement_path

    @pytest.mark.parametrize(
        "exclude_list", [SINGLE_EXCLUDE_LIST, MULTIPLE_EXCLUDE_LIST]
    )
    def test_exclude(self, exclude_list, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        entrypoint_args = ["--", "python", "main.py"]
        exclude_args = [i for exclude in exclude_list for i in ("-e", exclude)]
        result = runner.invoke(submit, [*exclude_args, *entrypoint_args])
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config.excludes == exclude_list

    def test_compute_config(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        entrypoint_args = ["--", "python", "main.py"]
        compute_config_name = "override-default-compute-config"
        result = runner.invoke(
            submit, ["--compute-config", compute_config_name, *entrypoint_args]
        )
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config.compute_config == compute_config_name

    def test_job_run_timeout(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        entrypoint_args = ["--", "python", "main.py"]
        result = runner.invoke(submit, ["--timeout-s", str(60), *entrypoint_args])
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_config.timeout_s == 60


class TestStatus:
    def test_no_name(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(status)
        _assert_error_message(
            result, message="One of '--name' and '--id' must be provided."
        )

    def test_name_and_id(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(status, ["-n", "custom-name", "--id", "fake-job-id"])
        _assert_error_message(
            result, message="Only one of '--name' and '--id' can be provided."
        )

    def test_name(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        runner.invoke(submit, ["-n", "custom-name", "--", "python", "main.py"])
        result = runner.invoke(status, ["-n", "custom-name"])
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_id in result.stdout
        assert fake_job_sdk.submitted_name in result.stdout

    def test_id(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        runner.invoke(submit, ["--", "python", "main.py"])
        result = runner.invoke(status, ["--id", fake_job_sdk.submitted_id])
        assert result.exit_code == 0
        assert fake_job_sdk.submitted_id in result.stdout
        assert fake_job_sdk.submitted_name in result.stdout

    def test_verbose_flag(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        runner.invoke(submit, ["-n", "custom-name", "--", "python", "main.py"])

        # No verbose flag -- exclude details
        result = runner.invoke(status, ["-n", "custom-name"])
        assert result.exit_code == 0
        assert "id" in result.stdout
        assert "name" in result.stdout
        assert "state" in result.stdout
        assert "config" not in result.stdout

        # Verbose flag -- include details
        result = runner.invoke(status, ["-n", "custom-name", "-v"])
        assert result.exit_code == 0
        assert "id" in result.stdout
        assert "name" in result.stdout
        assert "state" in result.stdout
        assert "config" in result.stdout

    def test_job_runs(self, fake_job_sdk, mock_job_controller):
        runner = CliRunner()
        runner.invoke(submit, ["--", "python", "main.py"])
        fake_job_sdk._job_runs = [
            JobRunStatus(name="failed-job-run", state=JobRunState.FAILED),
            JobRunStatus(name="succeeded-job-run", state=JobRunState.SUCCEEDED),
        ]
        result = runner.invoke(status, ["--id", fake_job_sdk.submitted_id])
        assert result.exit_code == 0
        assert (
            "runs:\n- name: failed-job-run\n  state: FAILED\n- name: succeeded-job-run\n  state: SUCCEEDED"
            in result.stdout
        )


class TestWait:
    def test_name(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(wait, ["-n", "custom-name"])
        assert result.exit_code == 0
        assert fake_job_sdk.waited_name == "custom-name"

    def test_id(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(wait, ["--id", "test-job-id"])
        assert result.exit_code == 0
        assert fake_job_sdk.waited_id == "test-job-id"

    def test_state(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(wait, ["-n", "custom-name", "--state", "FAILED"])
        assert result.exit_code == 0
        assert fake_job_sdk.waited_name == "custom-name"
        assert fake_job_sdk.waited_state == JobState.FAILED

    def test_bad_state(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(wait, ["-n", "custom-name", "--state", "FOOBAR"])
        assert result.exit_code == 1
        assert "'FOOBAR' is not a valid JobState" in str(result.stdout)

    def test_timeout(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(wait, ["-n", "custom-name", "--timeout-s=30"])
        assert result.exit_code == 0
        assert fake_job_sdk.waited_timeout_s == 30


class TestLogs:
    def test_name(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(logs, ["-n", "custom-name"])
        assert result.exit_code == 0
        assert fake_job_sdk.get_logs_name == "custom-name"

    def test_id(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(logs, ["--id", "test-job-id"])
        assert result.exit_code == 0
        assert fake_job_sdk.get_logs_id == "test-job-id"

    def test_run(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(
            logs, ["--name", "test-job-name", "--run", "test-job-run"]
        )
        assert result.exit_code == 0
        assert fake_job_sdk.get_logs_run == "test-job-run"

    def test_mode(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(logs, ["-n", "custom-name", "--head"])
        assert result.exit_code == 0
        assert fake_job_sdk.get_logs_name == "custom-name"
        assert fake_job_sdk.get_logs_mode == JobLogMode.HEAD

        result = runner.invoke(logs, ["-n", "custom-name", "--tail"])
        assert result.exit_code == 0
        assert fake_job_sdk.get_logs_name == "custom-name"
        assert fake_job_sdk.get_logs_mode == JobLogMode.TAIL

    def test_max_lines_without_head_and_tail(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(logs, ["-n", "custom-name", "--max-lines=10"])
        assert result.exit_code == 1
        assert "'--max-lines' must be used with either '--head' or '--tail'" in str(
            result.stdout
        )

    def test_max_lines_(self, fake_job_sdk):
        runner = CliRunner()
        result = runner.invoke(logs, ["-n", "custom-name", "--head", "--max-lines=10"])
        assert result.exit_code == 0
        assert fake_job_sdk.get_logs_max_lines == 10
