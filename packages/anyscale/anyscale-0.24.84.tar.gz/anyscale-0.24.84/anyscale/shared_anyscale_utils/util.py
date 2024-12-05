# AUTOGENERATED - modify shared_anyscale_util in root directory to make changes
import base64
import re
from typing import Any, Dict
import unicodedata


def execution_log_name(session_command_id: str) -> str:
    # Note: this path is no longer correct. We should remove this once
    # we've cleaned up the logic backing `/api/v2/session_commands/{session_command_id}/execution_logs`
    # and migrate the webterminal to a sidecar/standalone executable.
    return "/tmp/ray_command_output_{session_command_id}".format(
        session_command_id=session_command_id
    )


def startup_log_name(session_id: str) -> str:
    return f"/tmp/session_startup_logs_{session_id}"


def startup_log_name_v2(session_id: str, encoded: bool = False) -> str:
    startup_log_name = "/var/log/anyscale/session_startup_logs_{session_id}".format(
        session_id=session_id
    )

    if encoded:
        # The encoding should be the same as `encodePathToFileName` in go/infra/anyscaled/internal/logcache/utils.go
        return base64.standard_b64encode(f"{startup_log_name}.out".encode()).decode()
    else:
        return startup_log_name


def slugify(value: str) -> str:
    """
    Code adopted from here https://github.com/django/django/blob/master/django/utils/text.py

    Convert  to ASCII. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Also strip leading and trailing whitespace.
    """

    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value).strip()
    return re.sub(r"[-\s]+", "-", value)


def get_container_name(cluster_config: Dict[str, Any]) -> str:
    return str(cluster_config.get("docker", {}).get("container_name", ""))
