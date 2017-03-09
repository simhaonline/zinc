from unittest import mock

# from django_dynamic_fixture import G
import pytest

from zinc import ns_check, models
from tests.fixtures import zone, boto_client, Moto  # noqa: F401


@pytest.mark.parametrize("boto_client", [Moto], ids=['fake_boto'], indirect=True)
@pytest.mark.django_db
def test_is_ns_propagated(zone):
    resolver = mock.Mock()
    resolver.query.return_value = ["test_ns.presslabs.net"]
    with mock.patch('zinc.ns_check.get_resolver', lambda: resolver):
        assert ns_check.is_ns_propagated(zone)


@pytest.mark.parametrize("boto_client", [Moto], ids=['fake_boto'], indirect=True)
@pytest.mark.django_db
def test_is_ns_propagated_false(zone):
    resolver = mock.Mock()
    resolver.query.return_value = ["some_other_ns.example.com"]
    with mock.patch('zinc.ns_check.get_resolver', lambda: resolver):
        assert ns_check.is_ns_propagated(zone) is False


@pytest.mark.parametrize("boto_client", [Moto], ids=['fake_boto'], indirect=True)
@pytest.mark.django_db
def test_update_ns_propagated(zone):
    assert zone.ns_propagated is False
    resolver = mock.Mock()
    resolver.query.return_value = ["test_ns.presslabs.net"]
    with mock.patch('zinc.ns_check.get_resolver', lambda: resolver):
        models.Zone.update_ns_propagated()
    zone.refresh_from_db()
    assert zone.ns_propagated


@pytest.mark.parametrize("boto_client", [Moto], ids=['fake_boto'], indirect=True)
@pytest.mark.django_db
def test_update_ns_propagated_false(zone):
    assert zone.ns_propagated is False
    resolver = mock.Mock()
    resolver.query.return_value = ["some_other_ns.example.com"]
    with mock.patch('zinc.ns_check.get_resolver', lambda: resolver):
        models.Zone.update_ns_propagated()
    zone.refresh_from_db()
    assert zone.ns_propagated is False