"""The Floci endpoint rule: set locally, unset in real AWS."""

import pytest

from tournament.config import Settings


def test_aws_endpoint_defaults_to_none_for_real_aws() -> None:
    settings = Settings(_env_file=None)

    assert settings.aws_endpoint_url is None


def test_aws_endpoint_is_read_from_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AWS_ENDPOINT_URL", "http://floci:4566")

    settings = Settings(_env_file=None)

    assert settings.aws_endpoint_url == "http://floci:4566"
