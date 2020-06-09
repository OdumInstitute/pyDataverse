# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dataverse data model tests."""
import json
import jsonschema
import os
from pyDataverse.models import Dataverse
from pyDataverse.models import DVObject
import pytest


TEST_DIR = os.path.dirname(os.path.realpath(__file__))


def read_file(filename, mode='r'):
    """Read in a file.

    Parameters
    ----------
    filename : string
        Filename with full path.
    mode : string
        Read mode of file. Defaults to `r`. See more at
        https://docs.python.org/3.5/library/functions.html#open

    Returns
    -------
    string
        Returns data as string.

    """
    try:
        with open(filename, mode) as f:
            data = f.read()
        return data
    except IOError:
        print('An error occured trying to read the file {}.'.format(filename))
    except Exception as e:
        raise e


def read_json(filename, mode='r', encoding='utf-8'):
    """Read in a json file.

    See more about the json module at
    https://docs.python.org/3.5/library/json.html

    Parameters
    ----------
    filename : string
        Filename with full path.

    Returns
    -------
    dict
        Data as a json-formatted string.

    """
    try:
        with open(filename, mode=mode, encoding=encoding) as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise e


def write_json(filename, data, mode='w', encoding='utf-8'):
    """Write data to a json file.

    Parameters
    ----------
    filename : string
        Filename with full path.
    data : dict
        Data to be written in the json file.
    mode : string
        Write mode of file. Defaults to `w`. See more at
        https://docs.python.org/3/library/functions.html#open

    """
    try:
        with open(filename, mode, encoding=encoding) as f:
            json.dump(data, f, indent=2)
    except IOError:
        print('An error occured trying to write the file {}.'.format(filename))
    except Exception as e:
        raise e


def object_init():
    """Import minimum Dataverse dict.

    Returns
    -------
    dict
        Minimum Dataverse metadata.

    """
    dv = Dataverse()
    dv.default_validate_format = 'dataverse_upload'
    dv.default_validate_schema_filename = 'schemas/json/dataverse_upload_schema.json'
    dv.attr_dv_up_values = attr_dv_up_values()
    return dv


def object_min():
    """Import minimum Dataverse dict.

    Returns
    -------
    dict
        Minimum Dataverse metadata.

    """
    dv = object_init()
    dv.alias = 'test-pyDataverse'
    dv.name = 'Test pyDataverse'
    dv.dataverseContacts = [{'contactEmail': 'info@aussda.at'}]
    return dv


def object_full():
    """Import minimum Dataverse dict.

    Returns
    -------
    dict
        Minimum Dataverse metadata.

    """
    dv = object_init()
    dv.alias = 'science'
    dv.name = 'Scientific Research'
    dv.dataverseContacts = [{'contactEmail': 'pi@example.edu'},{'contactEmail': 'student@example.edu'}]
    dv.affiliation = 'Scientific Research University'
    dv.description = 'We do all the science.'
    dv.dataverseType = 'LABORATORY'
    return dv


def dict_flat_set_min():
    """Import minimum Dataverse dict.

    Returns
    -------
    dict
        Minimum Dataverse metadata.

    """
    data = {
        'alias': 'test-pyDataverse',
        'name': 'Test pyDataverse',
        'dataverseContacts': [
            {'contactEmail': 'info@aussda.at'}
        ]
    }
    return data


def dict_flat_set_full():
    """Import full Dataverse dict.

    Returns
    -------
    dict
        Full Dataverse metadata.

    """
    data = {
        'name': 'Scientific Research',
        'alias': 'science',
        'dataverseContacts': [
            {'contactEmail': 'pi@example.edu'},
            {'contactEmail': 'student@example.edu'}
        ],
        'affiliation': 'Scientific Research University',
        'description': 'We do all the science.',
        'dataverseType': 'LABORATORY'
    }
    return data


def dict_flat_dict_min():
    """Import minimum Dataverse dict.

    Returns
    -------
    dict
        Minimum Dataverse metadata.

    """
    data = {
        'alias': 'test-pyDataverse',
        'name': 'Test pyDataverse',
        'dataverseContacts': [
            {'contactEmail': 'info@aussda.at'}
        ],
        'default_validate_format': 'dataverse_upload',
        'default_validate_schema_filename': 'schemas/json/dataverse_upload_schema.json',
        'attr_dv_up_values': attr_dv_up_values()
    }
    return data


def dict_flat_dict_full():
    """Import full Dataverse dict.

    Returns
    -------
    dict
        Full Dataverse metadata.

    """
    data = {
        'name': 'Scientific Research',
        'alias': 'science',
        'dataverseContacts': [
            {'contactEmail': 'pi@example.edu'},
            {'contactEmail': 'student@example.edu'}
        ],
        'affiliation': 'Scientific Research University',
        'description': 'We do all the science.',
        'dataverseType': 'LABORATORY',
        'default_validate_format': 'dataverse_upload',
        'default_validate_schema_filename': 'schemas/json/dataverse_upload_schema.json',
        'attr_dv_up_values': attr_dv_up_values()
    }
    return data


def json_upload_min():
    """Import minimum Dataverse dict.

    Returns
    -------
    dict
        Minimum Dataverse metadata.

    """
    data = read_file('tests/data/dataverse_upload_min.json')
    return data


def json_upload_full():
    """Import full Dataverse dict.

    Returns
    -------
    dict
        Full Dataverse metadata.

    """
    data = read_file('tests/data/dataverse_upload_full.json')
    return data


def attr_dv_up_values():
    data = [
        'affiliation',
        'alias',
        'dataverseContacts',
        'dataverseType',
        'description',
        'name'
    ]
    return data


class TestDataverse(object):
    """Tests for Dataverse()."""

    def test_dataverse_init(self):
        """Test Dataverse.__init__()."""
        obj_assert = object_init()
        obj = Dataverse()

        assert obj.__dict__ == obj_assert.__dict__

    def test_dataverse_set_valid(self):
        """Test Dataverse.set() with format=`dv_up`.

        Parameters
        ----------
        dict_flat_min : dict
            Fixture, which returns a flat dataset dict() coming from
            `tests/data/dataverse_min.json`.

        """
        obj_assert = object_min()
        obj = Dataverse()
        obj.set(dict_flat_set_min())

        assert obj.__dict__ == obj_assert.__dict__

        obj_assert = object_full()
        obj = Dataverse()
        obj.set(dict_flat_set_full())

        assert obj.__dict__ == obj_assert.__dict__

    def test_dataverse_dict_valid(self):
        """Test Dataverse.dict() with format=`all` and valid data.

        Parameters
        ----------
        object_min : dict
            Fixture, which returns a flat dataset dict() coming from
            `tests/data/dataverse_min.json`.

        """

        dict_assert = dict_flat_dict_min()
        obj = object_min()
        dict_flat = obj.dict()

        assert dict_flat == dict_assert

        dict_assert = dict_flat_dict_full()
        obj = object_full()
        dict_flat = obj.dict()

        assert dict_flat == dict_assert

    def test_dataverse_from_json_dv_up_valid(self):
        """Test Dataverse.import_data() with format=`dv_up`."""
        obj_assert = object_min()
        obj = Dataverse()
        obj.from_json('tests/data/dataverse_upload_min.json', validate=False)

        assert obj_assert.__dict__ == obj.__dict__

        obj_assert = object_full()
        obj = Dataverse()
        obj.from_json('tests/data/dataverse_upload_full.json', validate=False)

        assert obj_assert.__dict__ == obj.__dict__

    def test_dataverse_from_json_format_invalid(self):
        """Test Dataverse.import_data() with non-valid format."""
        obj_assert = object_init()
        obj = Dataverse()
        obj.from_json(os.path.join(TEST_DIR, '/data/dataverse_upload_min.json'), format='wrong', validate=False)

        assert obj
        assert obj.__dict__
        assert obj_assert.__dict__ is not obj.__dict__
        assert len(obj.__dict__.keys()) == len(obj_assert.__dict__.keys())

    def test_dataverse_to_json_dv_up_valid(self):
        """Test Dataverse.json() with format=`dv_up` and valid data.

        Parameters
        ----------
        object_min : dict
            Fixture, which returns a flat dataset dict() coming from
            `tests/data/dataverse_min.json`.

        TODO: Assert content
        """
        dict_assert = json.loads(json_upload_min())
        obj = object_min()

        assert isinstance(obj.to_json(validate=False), str)
        assert json.loads(obj.to_json(validate=False)) == dict_assert

        dict_assert = json.loads(json_upload_full())
        obj = object_full()

        assert isinstance(obj.to_json(validate=False), str)
        assert json.loads(obj.to_json(validate=False)) == dict_assert

    def test_dataverse_to_json_dv_up_invalid(self):
        """Test Dataverse.json() with format=`dv_up` and non-valid data.

        Parameters
        ----------
        object_min : dict
            Fixture, which returns a flat dataset dict() coming from
            `tests/data/dataverse_min.json`.

        """
        obj = object_min()
        with pytest.raises(TypeError):
            json_dict = json.loads(obj.to_json(format='wrong', validate=False))

    def test_dataverse_to_json_format_invalid(self):
        """Test Dataverse.json() with non-valid format and valid data.

        Parameters
        ----------

        """
        obj = object_min()

        with pytest.raises(TypeError):
            json_dict = json.loads(obj.to_json(format='wrong', validate=False))

    def test_validate(self):
        obj = object_init()
        assert obj.from_json(os.path.join(TEST_DIR + '/data/dataverse_upload_min.json'))

        obj = object_init()
        assert obj.from_json(os.path.join(TEST_DIR + '/data/dataverse_upload_min.json'), validate=True)

        obj = object_init()
        assert obj.from_json(os.path.join(TEST_DIR + '/data/dataverse_upload_min.json'), validate=True, filename_schema='schemas/json/dataverse_upload_schema.json')

        obj = object_init()
        assert obj.from_json(os.path.join(TEST_DIR + '/data/dataverse_upload_min.json'), filename_schema='schemas/json/dataverse_upload_schema.json')

        # wrong
        obj = object_init()
        with pytest.raises(jsonschema.exceptions.ValidationError):
            obj.to_json()
        assert not obj.to_json(format='wrong')
        with pytest.raises(jsonschema.exceptions.ValidationError):
            assert obj.to_json(filename_schema='schemas/json/datafile_upload_schema.json')
        with pytest.raises(jsonschema.exceptions.ValidationError):
            assert obj.validate_json()
        with pytest.raises(TypeError):
            assert obj.validate_json(format='wrong')
        with pytest.raises(jsonschema.exceptions.ValidationError):
            assert obj.validate_json(filename_schema='schemas/json/datafile_upload_schema.json')

    def test_dataverse_from_json_to_json(self):
        """Test Dataverse pipeline from import to export with format=`dv_up`."""
        if not os.environ.get('TRAVIS'):
            dict_assert = json.loads(json_upload_min())
            obj = Dataverse()
            obj.from_json(os.path.join(TEST_DIR + '/data/dataverse_upload_min.json'), validate=False)
            json_str = obj.to_json(validate=False)

            assert json.loads(json_str) == dict_assert

            dict_assert = json.loads(json_upload_full())
            obj = Dataverse()
            obj.from_json(os.path.join(TEST_DIR + '/data/dataverse_upload_full.json'), validate=False)
            json_str = obj.to_json(validate=False)

            assert json.loads(json_str) == dict_assert
