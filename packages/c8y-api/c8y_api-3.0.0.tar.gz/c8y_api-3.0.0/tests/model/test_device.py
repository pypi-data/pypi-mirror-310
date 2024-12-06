# Copyright (c) 2020 Software AG,
# Darmstadt, Germany and/or Software AG USA Inc., Reston, VA, USA,
# and/or its subsidiaries and/or its affiliates and/or their licensors.
# Use, reproduction, transfer, publication or disclosure is prohibited except
# as specifically provided for in your License Agreement with Software AG.

# pylint: disable=redefined-outer-name

import json
import os
from unittest.mock import patch, Mock

import pytest

from c8y_api._base_api import CumulocityRestApi
from c8y_api.model import Device

from tests.utils import isolate_last_call_arg


@pytest.fixture(scope='function')
def sample_device() -> Device:
    """Provide a sample object for various tests."""
    return Device(name='name', type='type', owner='owner',
                  simple_string='string',
                  simple_int=123,
                  simple_float=123.4,
                  simple_true=True,
                  simple_false=False,
                  complex_1={'level0': 'value'},
                  complex_2={'string': 'value', 'level0': {'level1': 'value'}})


@pytest.fixture(scope='session')
def sample_json() -> dict:
    """Provide sample device JSON."""
    path = os.path.dirname(__file__) + '/device.json'
    with open(path, encoding='utf-8', mode='rt') as f:
        return json.load(f)


def test_formatting(sample_device: Device):
    """Verify that JSON formatting works."""
    sample_device.id = 'id'
    object_json = sample_device.to_full_json()

    assert 'id' not in object_json
    assert object_json['name'] == sample_device.name
    assert object_json['type'] == sample_device.type
    assert object_json['owner'] == sample_device.owner
    assert 'c8y_IsDevice' in object_json

    assert object_json['simple_string'] == sample_device.simple_string
    assert object_json['simple_int'] == sample_device.simple_int
    assert object_json['simple_float'] == sample_device.simple_float
    assert object_json['simple_true'] is True
    assert object_json['simple_false'] is False
    assert object_json['complex_1']['level0'] == 'value'
    assert object_json['complex_2']['level0']['level1'] == 'value'

    expected_keys = {'name', 'type', 'owner', 'c8y_IsDevice',
                     'simple_string', 'simple_int', 'simple_float', 'simple_true', 'simple_false',
                     'complex_1', 'complex_2'}
    assert set(object_json.keys()) == expected_keys


def test_parsing(sample_json):
    """Verify that parsing a Device from JSON works."""

    d = Device.from_json(sample_json)

    # 2) assert parsed data
    assert d.id == sample_json['id']
    assert d.type == sample_json['type']
    assert d.name == sample_json['name']
    assert d.creation_time == sample_json['creationTime']
    assert d.is_device
    assert d.creation_datetime

    # 3) custom fragments
    assert d.c8y_SupportedOperations == sample_json['c8y_SupportedOperations']
    test_fragment = d.c8y_DataPoint.test
    test_json = sample_json['c8y_DataPoint']['test']
    assert test_fragment.string == test_json['string']
    assert test_fragment.int == test_json['int']
    assert test_fragment.float == test_json['float']
    assert test_fragment.true == test_json['true']
    assert test_fragment.false == test_json['false']


def get_json_arg_keys(mock: Mock) -> set:
    """Get keys from 'json' arguments."""

    def get_json_arg(m: Mock) -> dict:
        return isolate_last_call_arg(m, name='json', pos=1)

    return set(get_json_arg(mock).keys())


def test_create(sample_device: Device, sample_json: dict):
    """Verify that the .create() function will result in the correct POST
    request."""

    # 1) test unchanged
    with patch('c8y_api._base_api.CumulocityRestApi') as api_mock:
        api_mock.post = Mock(return_value=sample_json)
        sample_device.c8y = api_mock
        sample_device.create()

    # -> accept header should be customized
    accept_arg = isolate_last_call_arg(api_mock.post, name='accept')
    assert accept_arg == CumulocityRestApi.ACCEPT_MANAGED_OBJECT

    # -> posted JSON should contain all the fields
    expected_keys = {'name', 'type', 'owner', 'c8y_IsDevice', *sample_device.fragments.keys()}
    actual_keys = get_json_arg_keys(api_mock.post)
    assert actual_keys == expected_keys


def test_create_after_change(sample_device: Device, sample_json: dict):
    """Verify that the .create() function will result in the correct POST
    request after an object change."""

    # 1) apply a couple of changes to readonly attributes
    sample_device.id = 'new id'
    sample_device.creation_time = 'new time'
    sample_device.update_time = 'new time'
    sample_device.is_device = False

    with patch('c8y_api._base_api.CumulocityRestApi') as api_mock:
        api_mock.post = Mock(return_value=sample_json)
        sample_device.c8y = api_mock
        sample_device.create()

    # -> posted JSON should not contain the above changes
    expected_keys = {'name', 'type', 'owner', 'c8y_IsDevice', *sample_device.fragments.keys()}
    actual_keys = get_json_arg_keys(api_mock.post)
    assert actual_keys == expected_keys


def test_update(sample_device: Device, sample_json: dict):
    """Verify that the .update() function will result in the correct PUT
    request."""

    # standard updatable attributes
    sample_device.name = 'new_name'
    sample_device.type = 'new_type'
    sample_device.owner = 'new_owner'
    # not updatable attributes
    sample_device.id = 'not allowed'
    sample_device.creation_time = 'not allowed'
    sample_device.update_time = 'not allowed'
    sample_device.is_device = False
    # simple fragments
    sample_device['simple_fragment'] = 'value'
    sample_device['complex_fragment'] = {'level0': 'value'}

    with patch('c8y_api._base_api.CumulocityRestApi') as api_mock:
        api_mock.put = Mock(return_value=sample_json)
        sample_device.c8y = api_mock
        sample_device.update()

    assert isolate_last_call_arg(api_mock.put, name='accept') == CumulocityRestApi.ACCEPT_MANAGED_OBJECT

    expected_keys = {'name', 'type', 'owner', 'simple_fragment', 'complex_fragment'}
    actual_keys = get_json_arg_keys(api_mock.put)
    assert actual_keys == expected_keys
