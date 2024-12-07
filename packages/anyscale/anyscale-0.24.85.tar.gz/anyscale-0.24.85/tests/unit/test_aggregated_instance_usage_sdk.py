from typing import Tuple

from common import TestLogger
import pytest

from anyscale import Anyscale
from anyscale._private.anyscale_client import FakeAnyscaleClient
from anyscale._private.sdk.timer import FakeTimer
from anyscale.aggregated_instance_usage import AggregatedInstanceUsageSDK
from anyscale.aggregated_instance_usage.models import DownloadCSVFilters


@pytest.fixture()
def aggregated_instance_usage_sdk_with_fakes(
    sdk_with_fakes: Tuple[Anyscale, FakeAnyscaleClient, TestLogger, FakeTimer]
) -> Tuple[AggregatedInstanceUsageSDK, FakeAnyscaleClient, TestLogger, FakeTimer]:
    sdk, client, logger, timer = sdk_with_fakes
    return sdk.aggregated_instance_usage, client, logger, timer


class TestDownloadCSV:
    def test_basic(
        self,
        aggregated_instance_usage_sdk_with_fakes: Tuple[
            AggregatedInstanceUsageSDK, FakeAnyscaleClient, TestLogger, FakeTimer
        ],
    ):
        sdk, fake_client, _, _ = aggregated_instance_usage_sdk_with_fakes

        project_name = "test-project-name"
        fake_client.register_project_by_name(project_name)

        filters = DownloadCSVFilters(
            start_date="2024-11-01",
            end_date="2024-11-02",
            cloud=fake_client.DEFAULT_CLOUD_NAME,
            project=project_name,
            directory="/",
        )
        filepath = sdk.download_csv(filters)

        assert filepath == "/aggregated_instance_usage_2024-11-01_2024-11-02.zip"
